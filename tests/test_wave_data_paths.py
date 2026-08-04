"""
Tests for US Wave hindcast dataset paths on AWS S3 and HSDS.

S3 tests use anonymous access (no credentials required).
HSDS tests require the HSDS_API_KEY environment variable; they are
skipped automatically if the variable is not set.

Forward tests   – every documented path actually exists.
Reverse tests   – no undocumented path silently appears.  Anything found on
                  S3/HSDS that is not in DOCUMENTED_* must be listed in
                  KNOWN_UNDOCUMENTED (with a reason comment) to keep CI green.
                  New, unexplained data will cause a test failure.
Snapshot tests  – the committed s3-inventory.md matches the live S3 state.
                  On failure, run: python scripts/check_wave_s3.py --update
"""

import difflib
import os
import re
import sys
from pathlib import Path

import boto3
import pytest
import requests
from botocore import UNSIGNED
from botocore.config import Config

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from check_wave_s3 import SNAPSHOT_PATH, build_markdown  # noqa: E402

# ---------------------------------------------------------------------------
# Constants matching docs/wave/hindcast/data-access.md
# ---------------------------------------------------------------------------

S3_BUCKET = "wpto-pds-us-wave"

# (version, domain, expected_file_prefix)
S3_DOMAINS = [
    ("v1.0.1", "West_Coast", "West_Coast_wave_"),
    ("v1.0.1", "Atlantic", "Atlantic_wave_"),
    ("v1.0.1", "Alaska", "Alaska_wave_"),
    ("v1.0.1", "Gulf_of_Mexico_and_Puerto_Rico", "GOM_PR_"),
    ("v1.0.0", "Hawaii", "Hawaii_wave_"),
    ("v1.0.0", "CNMI_and_Guam", "CNMI_and_Guam_wave_"),
    ("v1.0.0", "virtual_buoy/West_Coast", "West_Coast_virtual_buoy_"),
]

EXPECTED_YEAR_RANGE = {
    ("v1.0.1", "West_Coast"): (1979, 2020),
    ("v1.0.1", "Atlantic"): (1979, 2020),
    ("v1.0.1", "Alaska"): (1979, 2020),
    ("v1.0.1", "Gulf_of_Mexico_and_Puerto_Rico"): (1979, 2020),
    ("v1.0.0", "Hawaii"): (1979, 2020),
    ("v1.0.0", "CNMI_and_Guam"): (1979, 2020),
    ("v1.0.0", "virtual_buoy/West_Coast"): (1979, 2010),
}

HSDS_ENDPOINT = "https://developer.nlr.gov/api/hsds"

# (hsds_path, expected_subfolder_or_file_fragment)
# Note: v1.0.1/Atlantic exists in S3 but has not yet been loaded into HSDS.
HSDS_PATHS = [
    ("/nrel/US_wave/West_Coast", "West_Coast_wave_"),
    ("/nrel/US_wave/Atlantic", "Atlantic_wave_"),
    ("/nrel/US_wave/Hawaii", "Hawaii_wave_"),
    ("/nrel/US_wave/Alaska", "Alaska_wave_"),
    ("/nrel/US_wave/v1.0.0/CNMI_and_Guam", "CNMI_and_Guam_wave_"),
    ("/nrel/US_wave/v1.0.0/Gulf_of_Mexico_and_Puerto_Rico", "GOM_PR_"),
    ("/nrel/US_wave/v1.0.1/West_Coast", "West_Coast_wave_"),
    ("/nrel/US_wave/v1.0.1/Alaska", "Alaska_wave_"),
    ("/nrel/US_wave/v1.0.1/Gulf_of_Mexico_and_Puerto_Rico", "GOM_PR_"),
    ("/nrel/US_wave/virtual_buoy/West_Coast", "West_Coast_virtual_buoy_"),
]

# ---------------------------------------------------------------------------
# Documented inventory (used by reverse tests)
# ---------------------------------------------------------------------------

DOCUMENTED_S3_VERSIONS = {"v1.0.0", "v1.0.1"}

DOCUMENTED_S3_DOMAINS: dict[str, set[str]] = {
    "v1.0.0": {
        "Alaska",
        "Atlantic",
        "CNMI_and_Guam",
        "Gulf_of_Mexico_and_Puerto_Rico",
        "Hawaii",
        "West_Coast",
        "virtual_buoy",
    },
    "v1.0.1": {
        "Alaska",
        "Atlantic",
        "Gulf_of_Mexico_and_Puerto_Rico",
        "West_Coast",
    },
}

DOCUMENTED_S3_VIRTUAL_BUOY_DOMAINS = {"West_Coast"}

# Top-level entries directly under /nrel/US_wave/
DOCUMENTED_HSDS_TOP_LEVEL = {
    "Alaska",
    "Atlantic",
    "Hawaii",
    "West_Coast",
    "v1.0.0",
    "v1.0.1",
    "virtual_buoy",
}

DOCUMENTED_HSDS_V100_DOMAINS = {"CNMI_and_Guam", "Gulf_of_Mexico_and_Puerto_Rico"}

# Note: v1.0.1/Atlantic exists in S3 but has not yet been synced to HSDS.
DOCUMENTED_HSDS_V101_DOMAINS = {"Alaska", "Gulf_of_Mexico_and_Puerto_Rico", "West_Coast"}

DOCUMENTED_HSDS_VIRTUAL_BUOY_DOMAINS = {"West_Coast"}

# ---------------------------------------------------------------------------
# Known items that exist but are not yet documented in the wave docs.
# Each entry is (location_description, name, reason).
# Any S3/HSDS item found outside the DOCUMENTED_* sets must appear here,
# otherwise the reverse tests will fail to flag it as truly new.
# ---------------------------------------------------------------------------

KNOWN_UNDOCUMENTED: dict[str, str] = {
    # S3
    "s3:v1.0.0:virtual_buoy/Atlantic_deprecated": (
        "Deprecated Atlantic virtual buoy data superseded by v1.0.0/Atlantic"
    ),
    # HSDS
    "hsds:top_level:maine": (
        "Unrelated regional dataset under /nrel/US_wave/maine; not part of the "
        "national hindcast product"
    ),
    "hsds:virtual_buoy:Alaska": "Empty HSDS placeholder; no files loaded yet",
    "hsds:virtual_buoy:Hawaii": "Empty HSDS placeholder; no files loaded yet",
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def s3_client():
    return boto3.client("s3", config=Config(signature_version=UNSIGNED))


@pytest.fixture(scope="session")
def hsds_api_key():
    key = os.environ.get("HSDS_API_KEY")
    if not key:
        pytest.skip("HSDS_API_KEY not set")
    return key


def _hsds_children(api_key: str, parent_path: str) -> set[str]:
    """Return the set of immediate child folder/file names under parent_path."""
    url = f"{HSDS_ENDPOINT}/domains"
    params = {"domain": parent_path.rstrip("/") + "/", "api_key": api_key}
    for attempt in range(3):
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code != 503:
            break
        if attempt < 2:
            import time
            time.sleep(2 ** attempt)
    resp.raise_for_status()
    return {d["name"].rstrip("/").split("/")[-1] for d in resp.json().get("domains", [])}


def _s3_immediate_prefixes(s3_client, prefix: str) -> set[str]:
    """Return the set of immediate sub-prefixes (folder names) under prefix."""
    resp = s3_client.list_objects_v2(
        Bucket=S3_BUCKET, Prefix=prefix, Delimiter="/"
    )
    return {
        p["Prefix"][len(prefix):].rstrip("/")
        for p in resp.get("CommonPrefixes", [])
    }


# ---------------------------------------------------------------------------
# Forward tests – documented paths exist
# ---------------------------------------------------------------------------


def test_s3_bucket_versions(s3_client):
    """Top-level bucket contains v1.0.0 and v1.0.1 prefixes."""
    actual = _s3_immediate_prefixes(s3_client, "")
    for version in DOCUMENTED_S3_VERSIONS:
        assert version in actual, f"{version}/ missing from bucket root"


@pytest.mark.parametrize("version,domain,file_prefix", S3_DOMAINS)
def test_s3_domain_exists(s3_client, version, domain, file_prefix):
    """Each documented domain directory is non-empty."""
    prefix = f"{version}/{domain}/"
    resp = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix, MaxKeys=5)
    objects = [o for o in resp.get("Contents", []) if o["Size"] > 0]
    assert objects, f"No files found under s3://{S3_BUCKET}/{prefix}"


@pytest.mark.parametrize("version,domain,file_prefix", S3_DOMAINS)
def test_s3_file_naming(s3_client, version, domain, file_prefix):
    """Files in each domain match the expected naming pattern."""
    prefix = f"{version}/{domain}/"
    resp = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix, MaxKeys=5)
    objects = [o for o in resp.get("Contents", []) if o["Size"] > 0]
    assert objects, f"No files to check under {prefix}"
    for obj in objects:
        fname = obj["Key"].split("/")[-1]
        assert fname.startswith(file_prefix), (
            f"File '{fname}' does not start with expected prefix '{file_prefix}'"
        )


@pytest.mark.parametrize("version,domain,file_prefix", [
    (v, d, p) for (v, d, p) in S3_DOMAINS if "virtual_buoy" not in d
])
def test_s3_year_range(s3_client, version, domain, file_prefix):
    """Each domain covers the full documented year range."""
    prefix = f"{version}/{domain}/"
    paginator = s3_client.get_paginator("list_objects_v2")
    years = []
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Size"] == 0:
                continue
            m = re.search(r"(\d{4})\.h5$", obj["Key"])
            if m:
                years.append(int(m.group(1)))

    assert years, f"No year-stamped files found under {prefix}"
    expected_min, expected_max = EXPECTED_YEAR_RANGE[(version, domain)]
    assert min(years) == expected_min, (
        f"{version}/{domain}: expected start year {expected_min}, got {min(years)}"
    )
    assert max(years) == expected_max, (
        f"{version}/{domain}: expected end year {expected_max}, got {max(years)}"
    )


@pytest.mark.parametrize("hsds_path,file_fragment", HSDS_PATHS)
def test_hsds_domain_exists(hsds_api_key, hsds_path, file_fragment):
    """Each documented HSDS path is a non-empty folder."""
    url = f"{HSDS_ENDPOINT}/domains"
    params = {"domain": hsds_path + "/", "api_key": hsds_api_key}
    resp = requests.get(url, params=params, timeout=15)
    assert resp.status_code == 200, (
        f"HSDS returned {resp.status_code} for {hsds_path}"
    )
    domains = resp.json().get("domains", [])
    names = [d["name"] for d in domains]
    assert any(file_fragment in n for n in names), (
        f"No entry matching '{file_fragment}' found under HSDS path {hsds_path}. "
        f"Got: {names[:5]}"
    )


# ---------------------------------------------------------------------------
# Reverse tests – no undocumented data silently appears
# ---------------------------------------------------------------------------


def test_s3_no_undocumented_versions(s3_client):
    """S3 bucket root contains only documented version prefixes."""
    actual = _s3_immediate_prefixes(s3_client, "")
    unknown = actual - DOCUMENTED_S3_VERSIONS
    assert not unknown, (
        f"Undocumented S3 version(s) found: {unknown}. "
        "Add to DOCUMENTED_S3_VERSIONS and update docs/wave/hindcast/data-access.md."
    )


@pytest.mark.parametrize("version", sorted(DOCUMENTED_S3_VERSIONS))
def test_s3_no_undocumented_domains(s3_client, version):
    """Each S3 version contains only documented domain prefixes."""
    actual = _s3_immediate_prefixes(s3_client, f"{version}/")
    documented = DOCUMENTED_S3_DOMAINS.get(version, set())
    unknown = actual - documented
    assert not unknown, (
        f"Undocumented domain(s) in s3://{S3_BUCKET}/{version}/: {unknown}. "
        "Add to DOCUMENTED_S3_DOMAINS and update docs/wave/hindcast/data-access.md."
    )


def test_s3_no_undocumented_virtual_buoy_domains(s3_client):
    """v1.0.0/virtual_buoy/ contains only documented sub-domains."""
    actual = _s3_immediate_prefixes(s3_client, "v1.0.0/virtual_buoy/")
    known_undocumented = {
        name
        for key, _ in KNOWN_UNDOCUMENTED.items()
        if key.startswith("s3:v1.0.0:virtual_buoy/")
        for name in [key.split("virtual_buoy/", 1)[1]]
    }
    unknown = actual - DOCUMENTED_S3_VIRTUAL_BUOY_DOMAINS - known_undocumented
    assert not unknown, (
        f"Undocumented virtual_buoy sub-domain(s) found: {unknown}. "
        "Add to DOCUMENTED_S3_VIRTUAL_BUOY_DOMAINS or KNOWN_UNDOCUMENTED."
    )


def test_hsds_no_undocumented_top_level(hsds_api_key):
    """HSDS /nrel/US_wave/ contains only documented top-level entries."""
    actual = _hsds_children(hsds_api_key, "/nrel/US_wave")
    known_undocumented = {
        name
        for key in KNOWN_UNDOCUMENTED
        if key.startswith("hsds:top_level:")
        for name in [key.split("hsds:top_level:", 1)[1]]
    }
    unknown = actual - DOCUMENTED_HSDS_TOP_LEVEL - known_undocumented
    assert not unknown, (
        f"Undocumented HSDS top-level entry(s) under /nrel/US_wave/: {unknown}. "
        "Add to DOCUMENTED_HSDS_TOP_LEVEL or KNOWN_UNDOCUMENTED."
    )


def test_hsds_no_undocumented_v100_domains(hsds_api_key):
    """HSDS /nrel/US_wave/v1.0.0/ contains only documented domains."""
    actual = _hsds_children(hsds_api_key, "/nrel/US_wave/v1.0.0")
    unknown = actual - DOCUMENTED_HSDS_V100_DOMAINS
    assert not unknown, (
        f"Undocumented HSDS v1.0.0 domain(s): {unknown}. "
        "Add to DOCUMENTED_HSDS_V100_DOMAINS or KNOWN_UNDOCUMENTED."
    )


def test_hsds_no_undocumented_v101_domains(hsds_api_key):
    """HSDS /nrel/US_wave/v1.0.1/ contains only documented domains."""
    actual = _hsds_children(hsds_api_key, "/nrel/US_wave/v1.0.1")
    unknown = actual - DOCUMENTED_HSDS_V101_DOMAINS
    assert not unknown, (
        f"Undocumented HSDS v1.0.1 domain(s): {unknown}. "
        "Add to DOCUMENTED_HSDS_V101_DOMAINS or KNOWN_UNDOCUMENTED."
    )


def test_hsds_no_undocumented_virtual_buoy_domains(hsds_api_key):
    """HSDS /nrel/US_wave/virtual_buoy/ contains only documented domains."""
    actual = _hsds_children(hsds_api_key, "/nrel/US_wave/virtual_buoy")
    known_undocumented = {
        name
        for key in KNOWN_UNDOCUMENTED
        if key.startswith("hsds:virtual_buoy:")
        for name in [key.split("hsds:virtual_buoy:", 1)[1]]
    }
    unknown = actual - DOCUMENTED_HSDS_VIRTUAL_BUOY_DOMAINS - known_undocumented
    assert not unknown, (
        f"Undocumented HSDS virtual_buoy domain(s): {unknown}. "
        "Add to DOCUMENTED_HSDS_VIRTUAL_BUOY_DOMAINS or KNOWN_UNDOCUMENTED."
    )


# ---------------------------------------------------------------------------
# Snapshot test – committed s3-inventory.md matches live S3
# ---------------------------------------------------------------------------


def test_s3_inventory_markdown_snapshot():
    """
    The committed s3-inventory.md matches what the live S3 bucket would produce.

    On failure, regenerate the snapshot and commit it:

        python scripts/check_wave_s3.py --update
        git add docs/wave/hindcast/s3-inventory.md
        git commit -m "chore: update wave S3 inventory snapshot"

    If the change is expected (e.g. a new dataset version was released), update
    and commit.  If it is unexpected, investigate before updating.
    """
    assert SNAPSHOT_PATH.exists(), (
        f"Snapshot file not found: {SNAPSHOT_PATH}\n"
        "Generate it with: python scripts/check_wave_s3.py --update"
    )

    committed = SNAPSHOT_PATH.read_text(encoding="utf-8")
    live = build_markdown(verbose=False)

    if committed == live:
        return

    diff = "\n".join(
        difflib.unified_diff(
            committed.splitlines(),
            live.splitlines(),
            fromfile="committed  docs/wave/hindcast/s3-inventory.md",
            tofile="live       S3 state",
            lineterm="",
        )
    )
    pytest.fail(
        "docs/wave/hindcast/s3-inventory.md is out of date with the live S3 bucket.\n\n"
        f"{diff}\n\n"
        "To update the snapshot and silence this failure, run:\n\n"
        "    python scripts/check_wave_s3.py --update\n"
        "    git add docs/wave/hindcast/s3-inventory.md\n"
        "    git commit -m \"chore: update wave S3 inventory snapshot\"\n\n"
        "If the change is unexpected (e.g. files were removed), investigate before committing."
    )
