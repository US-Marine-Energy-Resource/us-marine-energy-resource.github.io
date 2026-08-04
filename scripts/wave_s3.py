"""
Shared S3 access for the US wave hindcast bucket (``wpto-pds-us-wave``).

Used by:
  - scripts/check_wave_s3.py            — bucket inventory tables
  - scripts/generate_wave_region_stats.py — per-region doc snippets

Everything here reads the bucket anonymously (no credentials, no NREL API key,
no HSDS). Two levels of access:

  list_domain()  — cheap. Paginated LIST, gives file count, years, sizes.
  read_schema()  — reads the HDF5 header of one object over ranged GETs, so a
                   190 GB file costs a few MB. Gives shapes, dtypes and the
                   per-variable attributes (description / IEC_name / SWAN_name
                   / units) straight from the file rather than a frozen dump.

The bucket is not homogeneous: a domain prefix can hold more than one model
product (Hawaii's v1.0.0 changes grid resolution at 2011). detect_eras() finds
those breaks so callers can report each one separately.
"""

import io
import re
from dataclasses import dataclass, field

import boto3
from botocore import UNSIGNED
from botocore.config import Config

BUCKET = "wpto-pds-us-wave"

DOMAINS = {
    "v1.0.0": [
        "West_Coast",
        "Atlantic",
        "Hawaii",
        "Alaska",
        "CNMI_and_Guam",
        "Gulf_of_Mexico_and_Puerto_Rico",
        "virtual_buoy/West_Coast",
    ],
    "v1.0.1": [
        "West_Coast",
        "Atlantic",
        "Alaska",
        "Gulf_of_Mexico_and_Puerto_Rico",
    ],
}

LATEST_VERSIONS = {
    "West_Coast": "v1.0.1",
    "Atlantic": "v1.0.1",
    "Hawaii": "v1.0.0",
    "Alaska": "v1.0.1",
    "CNMI_and_Guam": "v1.0.0",
    "Gulf_of_Mexico_and_Puerto_Rico": "v1.0.1",
    "virtual_buoy/West_Coast": "v1.0.0",
}

DOMAIN_LABELS = {
    "Alaska": "Alaska",
    "Atlantic": "Atlantic",
    "Gulf_of_Mexico_and_Puerto_Rico": "Gulf of Mexico & Puerto Rico",
    "West_Coast": "West Coast",
    "Hawaii": "Hawaii",
    "CNMI_and_Guam": "CNMI and Guam",
    "virtual_buoy/West_Coast": "Virtual Buoy (West Coast)",
}

# Datasets that describe the file rather than the resource; excluded from the
# spatiotemporal variable tables.
NON_VARIABLE_DATASETS = {"time_index", "meta", "coordinates", "missing_time_index"}

# Map HDF5 dtype codes to human-readable names
_DTYPE_MAP = {
    "<f2": "float16", "<f4": "float32", "<f8": "float64",
    ">f2": "float16", ">f4": "float32", ">f8": "float64",
    "<i1": "int8",  "<i2": "int16",  "<i4": "int32",  "<i8": "int64",
    ">i1": "int8",  ">i2": "int16",  ">i4": "int32",  ">i8": "int64",
    "<u1": "uint8", "<u2": "uint16", "<u4": "uint32", "<u8": "uint64",
}


def decode_dtype(raw) -> str:
    """Convert an HDF5 dtype code to a display string."""
    raw = str(raw).strip()
    if raw in _DTYPE_MAP:
        return _DTYPE_MAP[raw]
    # String types: S8, S24, |S19, etc.
    m = re.match(r"\|?S(\d+)$", raw)
    if m:
        return f"str[{m.group(1)}]"
    return raw


def s3_client():
    """Anonymous S3 client — this is a public open-data bucket."""
    return boto3.client("s3", config=Config(signature_version=UNSIGNED))


# ── Listing ───────────────────────────────────────────────────────────────────

@dataclass
class DomainInfo:
    version: str
    domain: str
    file_count: int
    year_min: int | None
    year_max: int | None
    file_pattern: str
    total_bytes: int
    sizes_by_year: dict
    s3_path: str
    openei_url: str = field(init=False)

    def __post_init__(self):
        prefix = f"{self.version}/{self.domain}/"
        self.openei_url = (
            f"https://data.openei.org/s3_viewer?bucket={BUCKET}"
            f"&prefix={prefix.replace('/', '%2F')}"
        )

    @property
    def total_size_gb(self) -> float:
        """Decimal GB, as reported in the inventory tables."""
        return self.total_bytes / 1e9

    @property
    def total_tib(self) -> float:
        return self.total_bytes / 2 ** 40

    @property
    def years(self) -> list:
        return sorted(self.sizes_by_year)

    @property
    def missing_years(self) -> list:
        """Years absent from an otherwise contiguous range."""
        if not self.sizes_by_year:
            return []
        span = range(self.year_min, self.year_max + 1)
        return sorted(set(span) - set(self.sizes_by_year))


def list_domain(s3_client_, version: str, domain: str) -> DomainInfo:
    prefix = f"{version}/{domain}/"
    paginator = s3_client_.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET, Prefix=prefix)

    files = []
    total_bytes = 0
    sizes_by_year = {}
    for page in pages:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            size = obj["Size"]
            if size == 0:
                continue
            files.append(key)
            total_bytes += size
            m = re.search(r"(\d{4})\.h5$", key)
            if m:
                sizes_by_year[int(m.group(1))] = size

    years = sorted(sizes_by_year)

    pattern = ""
    if files:
        fname = files[0].split("/")[-1]
        pattern = re.sub(r"\d{4}", "{year}", fname)

    return DomainInfo(
        version=version,
        domain=domain,
        file_count=len(files),
        year_min=years[0] if years else None,
        year_max=years[-1] if years else None,
        file_pattern=pattern,
        total_bytes=total_bytes,
        sizes_by_year=sizes_by_year,
        s3_path=f"s3://{BUCKET}/{prefix}",
    )


# ── Ranged reads ──────────────────────────────────────────────────────────────

BLOCK_SIZE = 1 << 20  # 1 MiB


class S3BlockFile(io.RawIOBase):
    """
    Seekable read-only file object backed by ranged S3 GETs, with a block cache.

    Lets h5py open a multi-hundred-GB object and read only its header. The cache
    is the whole point: h5py walks object headers and B-trees by seeking back
    and forth, and ``io.BufferedReader`` drops its buffer on every seek, so
    wrapping a plain ranged reader re-downloads the same regions dozens of times
    over. Caching fixed-size blocks makes each byte range cost one request at
    most; contiguous misses are coalesced into a single GET.

    ``requests`` and ``bytes_fetched`` are exposed so callers can report how
    much a probe actually cost.
    """

    def __init__(self, s3_client_, key: str, bucket: str = BUCKET):
        self._s3 = s3_client_
        self._bucket = bucket
        self._blocks = {}
        self.key = key
        self.pos = 0
        self.requests = 0
        self.bytes_fetched = 0
        self.size = s3_client_.head_object(Bucket=bucket, Key=key)["ContentLength"]

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_END:
            self.pos = self.size + offset
        else:
            raise ValueError(f"invalid whence: {whence}")
        return self.pos

    def tell(self) -> int:
        return self.pos

    def _fetch(self, first: int, last: int) -> None:
        """Fetch block indices first..last inclusive in one request."""
        start = first * BLOCK_SIZE
        end = min((last + 1) * BLOCK_SIZE, self.size) - 1
        body = self._s3.get_object(
            Bucket=self._bucket, Key=self.key, Range=f"bytes={start}-{end}"
        )["Body"].read()
        self.requests += 1
        self.bytes_fetched += len(body)
        for i in range(first, last + 1):
            chunk = body[(i - first) * BLOCK_SIZE : (i - first + 1) * BLOCK_SIZE]
            if chunk:
                self._blocks[i] = chunk

    def _ensure(self, first: int, last: int) -> None:
        """Load any missing blocks in first..last, coalescing runs of misses."""
        run_start = None
        for i in range(first, last + 1):
            if i in self._blocks:
                if run_start is not None:
                    self._fetch(run_start, i - 1)
                    run_start = None
            elif run_start is None:
                run_start = i
        if run_start is not None:
            self._fetch(run_start, last)

    def read(self, n: int = -1) -> bytes:
        if n < 0 or self.pos + n > self.size:
            n = self.size - self.pos
        if n <= 0:
            return b""

        first = self.pos // BLOCK_SIZE
        last = (self.pos + n - 1) // BLOCK_SIZE
        self._ensure(first, last)

        out = bytearray()
        for i in range(first, last + 1):
            block = self._blocks[i]
            lo = self.pos - i * BLOCK_SIZE if i == first else 0
            hi = (self.pos + n) - i * BLOCK_SIZE if i == last else len(block)
            out += block[lo:hi]

        self.pos += len(out)
        return bytes(out)

    def readinto(self, b) -> int:
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)


def open_h5(s3_client_, key: str):
    """Open an S3-hosted HDF5 file for header inspection."""
    import h5py  # imported lazily; only --refresh needs it

    raw = S3BlockFile(s3_client_, key)
    return h5py.File(raw, "r"), raw


def _attr(dset, name: str) -> str:
    """Read one attribute, normalising placeholder values to empty string."""
    val = dset.attrs.get(name, "")
    if isinstance(val, bytes):
        val = val.decode("utf-8", "replace")
    val = str(val).strip()
    if val.lower() in {"n/a", "none", ""}:
        return ""
    return val


def read_schema(s3_client_, key: str) -> dict:
    """
    Read one file's structure from its HDF5 header.

    Returns grid points, time steps, the spatiotemporal variables (with their
    attributes) and the compound meta field list.
    """
    import h5py

    f, raw = open_h5(s3_client_, key)
    file_bytes = raw.size
    with f:
        datasets = []
        for name, obj in f.items():
            if not isinstance(obj, h5py.Dataset):
                continue
            datasets.append(
                {
                    "name": name,
                    "shape": list(obj.shape),
                    "dtype": decode_dtype(obj.dtype),
                    "description": _attr(obj, "description"),
                    "iec_name": _attr(obj, "IEC_name"),
                    "swan_name": _attr(obj, "SWAN_name"),
                    "units": _attr(obj, "units"),
                }
            )

        by_name = {d["name"]: d for d in datasets}

        time_steps = 0
        if "time_index" in by_name:
            time_steps = by_name["time_index"]["shape"][0]
        else:
            # Fall back to the modal first dimension of the 2D datasets.
            first_dims = [d["shape"][0] for d in datasets if len(d["shape"]) == 2]
            if first_dims:
                time_steps = max(set(first_dims), key=first_dims.count)

        # Grid points: prefer meta, then coordinates, then the second dimension
        # of a time-indexed variable. Atlantic 2011+ has no meta dataset.
        grid_points = 0
        if "meta" in by_name and len(by_name["meta"]["shape"]) == 1:
            grid_points = by_name["meta"]["shape"][0]
        elif "coordinates" in by_name and by_name["coordinates"]["shape"]:
            grid_points = by_name["coordinates"]["shape"][0]
        if grid_points == 0 and time_steps:
            for d in datasets:
                if len(d["shape"]) == 2 and d["shape"][0] == time_steps:
                    grid_points = d["shape"][1]
                    break

        meta_fields = []
        if "meta" in f and f["meta"].dtype.names:
            meta_dtype = f["meta"].dtype
            meta_fields = [
                {"name": n, "dtype": decode_dtype(meta_dtype[n].str)}
                for n in meta_dtype.names
            ]

        global_attrs = {k: str(v) for k, v in f.attrs.items()}

    return {
        "key": key,
        "file_bytes": file_bytes,
        "probe_requests": raw.requests,
        "probe_bytes": raw.bytes_fetched,
        "grid_points": grid_points,
        "time_steps": time_steps,
        "global_attrs": global_attrs,
        "datasets": datasets,
        "meta_fields": meta_fields,
    }


# ── Era detection ─────────────────────────────────────────────────────────────

def spatiotemporal(schema: dict) -> list:
    """
    The time-indexed resource variables, sorted by name.

    These are the rows the docs render. Datasets that merely describe the file
    (time index, meta, coordinates) are excluded, as are auxiliary fields whose
    leading dimension is not the time axis — notably `water_depth`, which the
    West Coast archive stores with a different (and inconsistent) shape almost
    every year.
    """
    steps = schema["time_steps"]
    return sorted(
        (
            d
            for d in schema["datasets"]
            if d["name"] not in NON_VARIABLE_DATASETS
            and len(d["shape"]) == 2
            and d["shape"][0] == steps
        ),
        key=lambda d: d["name"],
    )


def schema_signature(schema: dict):
    """
    Identity of a file as the documentation presents it.

    Deliberately built from exactly what a region snippet renders — grid size,
    the spatiotemporal variable rows, and the metadata fields — so every era
    break the reader is shown corresponds to a difference they can actually
    see, and nothing splits on invisible bookkeeping. In particular this is
    insensitive to year length (a 2928-step leap year is the same product as a
    2920-step common year) and to the malformed auxiliary datasets that vary
    file-to-file in the West Coast archive.
    """
    variables = tuple(
        (
            d["name"],
            d["dtype"],
            d["shape"][1],
            d["description"],
            d["iec_name"],
            d["swan_name"],
            d["units"],
        )
        for d in spatiotemporal(schema)
    )
    meta = tuple((m["name"], m["dtype"]) for m in schema["meta_fields"])
    return (schema["grid_points"], variables, meta)


@dataclass
class Era:
    year_start: int
    year_end: int
    schema: dict

    @property
    def num_years(self) -> int:
        return self.year_end - self.year_start + 1


def detect_eras(s3_client_, info: DomainInfo, probe=None, log=None) -> list:
    """
    Split a domain's year range into contiguous eras sharing one schema.

    Probes the first and last year; if their signatures match, that's one era.
    Otherwise binary-searches the transition year and recurses on each side, so
    an N-year domain costs about log2(N) probes per boundary rather than N.
    """
    years = info.years
    if not years:
        return []

    cache = {}

    def _probe(year: int) -> dict:
        if year not in cache:
            key = f"{info.version}/{info.domain}/{info.file_pattern.format(year=year)}"
            if log:
                log(f"      probe {year}")
            cache[year] = (probe or read_schema)(s3_client_, key)
        return cache[year]

    def _split(lo_idx: int, hi_idx: int) -> list:
        lo_year, hi_year = years[lo_idx], years[hi_idx]
        lo, hi = _probe(lo_year), _probe(hi_year)
        if schema_signature(lo) == schema_signature(hi):
            # Characterise the era by its last year: 1979 is a partial year in
            # this hindcast (2,872 steps rather than 2,920), so using the first
            # year would put an unrepresentative time dimension in the docs.
            return [Era(lo_year, hi_year, hi)]

        # Binary search for the first index whose signature differs from lo.
        lo_sig = schema_signature(lo)
        left, right = lo_idx, hi_idx  # left matches lo_sig, right differs
        while right - left > 1:
            mid = (left + right) // 2
            if schema_signature(_probe(years[mid])) == lo_sig:
                left = mid
            else:
                right = mid

        return _split(lo_idx, left) + _split(right, hi_idx)

    eras = _split(0, len(years) - 1)

    # Merge adjacent eras that ended up with the same signature (possible when
    # a domain has three or more breaks and recursion splits either side).
    merged = [eras[0]]
    for era in eras[1:]:
        prev = merged[-1]
        if schema_signature(prev.schema) == schema_signature(era.schema):
            merged[-1] = Era(prev.year_start, era.year_end, era.schema)
        else:
            merged.append(era)
    return merged
