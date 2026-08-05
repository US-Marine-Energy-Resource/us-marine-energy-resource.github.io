"""
Generate per-region statistics snippets for the US wave hindcast dataset.

Reads ground truth from the public S3 bucket (see scripts/wave_s3.py) and
produces:

  docs/assets/wave_region_schema.json         — cached S3 probe results
  docs/assets/wave_region_stats.json          — machine-readable stats
  docs/includes/wave/region-stats-*.md        — one snippet per region

A domain prefix can hold more than one model product — Hawaii's v1.0.0 runs on
a 700,414-point grid through 2010 and a 1,696,188-point grid from 2011 — so
each snippet reports the archive totals once and then breaks out grid size,
per-year file size and the variable tables per era.

Usage:
    python scripts/generate_wave_region_stats.py --refresh   # re-probe S3, then render
    python scripts/generate_wave_region_stats.py             # render from cache
    python scripts/generate_wave_region_stats.py --dry-run   # summarise, write nothing
"""

import argparse
import json
import sys
from pathlib import Path

from wave_s3 import (
    NON_VARIABLE_DATASETS,
    detect_eras,
    list_domain,
    s3_client,
    spatiotemporal,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_CACHE = REPO_ROOT / "docs" / "assets" / "wave_region_schema.json"
OUTPUT_JSON = REPO_ROOT / "docs" / "assets" / "wave_region_stats.json"
SNIPPETS_DIR = REPO_ROOT / "docs" / "includes" / "wave"

# ── Region configuration ──────────────────────────────────────────────────────
# Only what S3 cannot tell us. Years, file counts, sizes, grid points, variables
# and metadata fields are all discovered — never hardcode them here again.

REGIONS = {
    "west-coast": {
        "display_name": "West Coast",
        "version": "v1.0.1",
        "domain": "West_Coast",
        "hsds_prefix": "/nrel/US_wave/v1.0.1/West_Coast",
    },
    "atlantic": {
        "display_name": "Atlantic",
        "version": "v1.0.1",
        "domain": "Atlantic",
        # HSDS has no v1.0.1/Atlantic folder even though S3 does; only the
        # unversioned path is populated, and it still serves v1.0.0.
        "hsds_prefix": "/nrel/US_wave/Atlantic",
    },
    "hawaii": {
        "display_name": "Hawaii",
        "version": "v1.0.0",
        "domain": "Hawaii",
        # Hawaii has no versioned folder on HSDS; only the unversioned path is
        # populated. v1.0.0 is Hawaii's latest release and it runs to 2020.
        "hsds_prefix": "/nrel/US_wave/Hawaii",
    },
    "alaska": {
        "display_name": "Alaska",
        "version": "v1.0.1",
        "domain": "Alaska",
        "hsds_prefix": "/nrel/US_wave/v1.0.1/Alaska",
    },
    "cnmi-guam": {
        "display_name": "CNMI and Guam",
        "version": "v1.0.0",
        "domain": "CNMI_and_Guam",
        "hsds_prefix": "/nrel/US_wave/v1.0.0/CNMI_and_Guam",
    },
    "gulf-of-america-and-puerto-rico": {
        "display_name": "Gulf of America and Puerto Rico",
        "version": "v1.0.1",
        "domain": "Gulf_of_Mexico_and_Puerto_Rico",
        "hsds_prefix": "/nrel/US_wave/v1.0.1/Gulf_of_Mexico_and_Puerto_Rico",
    },
}


# ── Probing ───────────────────────────────────────────────────────────────────

def probe_region(s3, key: str, cfg: dict) -> dict:
    """List a region's objects and detect its schema eras."""
    print(f"  {key}: listing s3://{cfg['version']}/{cfg['domain']}/ ...", flush=True)
    info = list_domain(s3, cfg["version"], cfg["domain"])
    if not info.file_count:
        raise RuntimeError(f"no objects under {cfg['version']}/{cfg['domain']}/")

    print(
        f"    {info.file_count} files, {info.year_min}–{info.year_max}, "
        f"{info.total_tib:.1f} TiB",
        flush=True,
    )
    eras = detect_eras(s3, info, log=lambda m: print(m, flush=True))
    print(f"    {len(eras)} era(s): "
          + ", ".join(f"{e.year_start}–{e.year_end}" for e in eras), flush=True)

    return {
        "version": info.version,
        "domain": info.domain,
        "s3_bucket": info.s3_path.split("/")[2],
        "s3_prefix": f"{info.version}/{info.domain}",
        "s3_file_pattern": info.file_pattern,
        "file_count": info.file_count,
        "year_start": info.year_min,
        "year_end": info.year_max,
        "missing_years": info.missing_years,
        "total_bytes": info.total_bytes,
        "sizes_by_year": {str(y): s for y, s in sorted(info.sizes_by_year.items())},
        "eras": [
            {
                "year_start": e.year_start,
                "year_end": e.year_end,
                "num_years": e.num_years,
                "grid_points": e.schema["grid_points"],
                "time_steps": e.schema["time_steps"],
                "global_attrs": e.schema["global_attrs"],
                "datasets": e.schema["datasets"],
                "meta_fields": e.schema["meta_fields"],
                "probed_key": e.schema["key"],
            }
            for e in eras
        ],
    }


def refresh_cache(dry_run: bool = False) -> dict:
    s3 = s3_client()
    cache = {}
    for key, cfg in REGIONS.items():
        cache[key] = probe_region(s3, key, cfg)
    if not dry_run:
        SCHEMA_CACHE.parent.mkdir(parents=True, exist_ok=True)
        SCHEMA_CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")
        print(f"\n  [OK] {SCHEMA_CACHE.relative_to(REPO_ROOT)}")
    return cache


def load_cache() -> dict:
    if not SCHEMA_CACHE.exists():
        sys.exit(
            f"error: schema cache not found at {SCHEMA_CACHE.relative_to(REPO_ROOT)}\n"
            f"       run: python scripts/generate_wave_region_stats.py --refresh"
        )
    cache = json.loads(SCHEMA_CACHE.read_text())
    missing = [k for k in REGIONS if k not in cache]
    if missing:
        sys.exit(
            f"error: schema cache is missing regions: {', '.join(missing)}\n"
            f"       run: python scripts/generate_wave_region_stats.py --refresh"
        )
    return cache


# ── Rendering ─────────────────────────────────────────────────────────────────

def _fmt_int(n: int) -> str:
    return f"{n:,}"


def _fmt_gb(nbytes: int) -> str:
    return f"~{nbytes / 2 ** 30:.1f} GB"


def _fmt_tb(nbytes: int) -> str:
    return f"~{nbytes / 2 ** 40:.1f} TB"


def _era_label(era: dict) -> str:
    return f"{era['year_start']}–{era['year_end']}"


_GREEK = {"theta": r"\theta", "Theta": r"\Theta", "epsilon": r"\epsilon",
          "sigma": r"\sigma", "Sigma": r"\Sigma"}
_IEC_ALIASES = {"epsilon_o": "epsilon_0", "T_Z": "T_z"}  # known typo/casing variants


def _iec_latex(raw: str) -> str:
    """Render a raw HDF5 IEC_name attribute (e.g. `T_e,T_-10`, `theta_J`) as LaTeX."""
    if not raw:
        return ""
    return ", ".join(f"${_iec_symbol(s.strip())}$" for s in raw.split(",") if s.strip())


def _iec_symbol(sym: str) -> str:
    sym = _IEC_ALIASES.get(sym, sym)
    tokens = sym.split("_")
    base = _GREEK.get(tokens[0], tokens[0])
    if len(tokens) == 1:
        return base
    sub = ",".join(_GREEK.get(t, t) for t in tokens[1:])
    return f"{base}_{{{sub}}}"


def _bytes_per_year(region: dict, era: dict) -> int:
    """
    Representative annual file size for an era.

    The median, not the maximum: leap years carry eight extra time steps and
    run a few GB larger, and quoting those would overstate a typical year. The
    archive total is measured separately, so this figure is only illustrative.
    """
    sizes = sorted(
        size
        for year, size in region["sizes_by_year"].items()
        if era["year_start"] <= int(year) <= era["year_end"]
    )
    return sizes[len(sizes) // 2]


def render_snippet(region: dict) -> str:
    """Render a markdown snippet for embedding in a region card."""
    eras = region["eras"]
    multi = len(eras) > 1
    lines = []

    n_files = region["file_count"]
    lines += [
        f"- **Period:** {region['year_start']}–{region['year_end']}"
        f" &nbsp;·&nbsp; {n_files} annual files",
        f"- **Total archive:** {_fmt_tb(region['total_bytes'])}",
        f"- **Version:** `{region['version']}`",
    ]

    if not multi:
        era = eras[0]
        lines.insert(0, f"- **Grid points:** {_fmt_int(era['grid_points'])}")
        lines.insert(1, f"- **File size:** {_fmt_gb(_bytes_per_year(region, era))} per year")

    if region["missing_years"]:
        gaps = ", ".join(str(y) for y in region["missing_years"])
        lines += [
            "",
            '!!! warning "Incomplete archive"',
            f"    Missing year(s) on AWS S3: {gaps}.",
        ]

    # Newest era first — that is the product most users will be reading.
    ordered = sorted(eras, key=lambda e: e["year_start"], reverse=True)

    lines.append("")

    for era in ordered:
        suffix = f" · {_era_label(era)}" if multi else ""
        if multi:
            lines += [
                f"**{_era_label(era)}** ({era['num_years']} files)",
                "",
                f"- Grid points: {_fmt_int(era['grid_points'])}"
                f" &nbsp;·&nbsp; {_fmt_gb(_bytes_per_year(region, era))} per year",
                "",
            ]
        tvars = spatiotemporal(era)
        lines += [
            f'??? note "Variable definitions ({len(tvars)}){suffix}"',
            "",
            "    | Variable | Description | IEC Name | SWAN name | Units |",
            "    |:---|:---|:---|:---|:---|",
        ]
        for v in tvars:
            lines.append(
                f"    | `{v['name']}` | {v['description']} | {_iec_latex(v['iec_name'])}"
                f" | {v['swan_name']} | {v['units']} |"
            )
        lines += [
            "",
            f'??? note "Variable schema ({len(tvars)}){suffix}"',
            "",
            "    | Variable | Units | Dimensions | Type |",
            "    |:---|:---|:---|:---|",
        ]
        for v in tvars:
            dims = f"{_fmt_int(v['shape'][0])} × {_fmt_int(v['shape'][1])}"
            lines.append(
                f"    | `{v['name']}` | {v['units']} | {dims} | `{v['dtype']}` |"
            )
        lines.append("")

        if era["meta_fields"]:
            lines += [
                f'??? note "Metadata ({len(era["meta_fields"])} fields){suffix}"',
                "",
                "    | Field | Type |",
                "    |:---|:---|",
            ]
            for mf in era["meta_fields"]:
                lines.append(f"    | `{mf['name']}` | `{mf['dtype']}` |")
            lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main(refresh: bool = False, dry_run: bool = False) -> None:
    cache = refresh_cache(dry_run=dry_run) if refresh else load_cache()

    SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
    all_stats = {}

    for key, cfg in REGIONS.items():
        region = cache[key]
        snippet = render_snippet(region)
        snippet_path = SNIPPETS_DIR / f"region-stats-{key}.md"

        if dry_run:
            print(f"\n{'=' * 60}")
            print(f"  {key}  →  {snippet_path.relative_to(REPO_ROOT)}")
            print(f"{'=' * 60}")
            print(f"  period={region['year_start']}–{region['year_end']}"
                  f" ({region['file_count']} files)")
            print(f"  total={region['total_bytes'] / 2 ** 40:.1f} TiB")
            for era in region["eras"]:
                print(f"  era {_era_label(era)}: "
                      f"grid={era['grid_points']:,} "
                      f"size={_bytes_per_year(region, era) / 2 ** 30:.1f} GiB/yr "
                      f"vars={len(spatiotemporal(era))} "
                      f"meta={len(era['meta_fields'])}")
        else:
            snippet_path.write_text(snippet)
            print(f"  [OK] {snippet_path.relative_to(REPO_ROOT)}")

        all_stats[key] = {
            "display_name": cfg["display_name"],
            "version": region["version"],
            "year_start": region["year_start"],
            "year_end": region["year_end"],
            "num_years": region["file_count"],
            "missing_years": region["missing_years"],
            "s3_bucket": region["s3_bucket"],
            "s3_prefix": region["s3_prefix"],
            "s3_file_pattern": region["s3_file_pattern"],
            "hsds_prefix": cfg["hsds_prefix"],
            "total_bytes": region["total_bytes"],
            "total_tb": round(region["total_bytes"] / 2 ** 40, 1),
            "eras": [
                {
                    "year_start": e["year_start"],
                    "year_end": e["year_end"],
                    "num_years": e["num_years"],
                    "grid_points": e["grid_points"],
                    "time_steps": e["time_steps"],
                    "file_size_gb": round(_bytes_per_year(region, e) / 2 ** 30, 1),
                    "variables": [
                        {
                            "name": v["name"],
                            "shape": v["shape"],
                            "dtype": v["dtype"],
                            "description": v["description"],
                            "iec_name": v["iec_name"],
                            "swan_name": v["swan_name"],
                            "units": v["units"],
                        }
                        for v in e["datasets"]
                        if v["name"] not in NON_VARIABLE_DATASETS
                    ],
                    "meta_fields": e["meta_fields"],
                }
                for e in region["eras"]
            ],
        }

    if not dry_run:
        OUTPUT_JSON.write_text(json.dumps(all_stats, indent=2) + "\n")
        print(f"  [OK] {OUTPUT_JSON.relative_to(REPO_ROOT)}")

    print("\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-probe S3 and rewrite the schema cache before rendering",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats to stdout without writing snippets",
    )
    args = parser.parse_args()
    main(refresh=args.refresh, dry_run=args.dry_run)
