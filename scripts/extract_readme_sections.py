#!/usr/bin/env python3
"""Extract sections from remote or local READMEs and write them as MkDocs
snippet files under ``docs/includes/readme/``.

Each extracted section is written as a standalone markdown file that can be
included in any docs page with:

    --8<-- "docs/includes/readme/<slug>.md"

Sections are identified by heading text (exact match) and heading level.
Content from that heading to the next heading at the same or higher level
is extracted and written verbatim.

To force regeneration:

    python scripts/extract_readme_sections.py [--force] [--docs-dir <path>]

The MkDocs hook ``hooks/extract_readme_sections.py`` calls this automatically
during build when any snippet file is missing or ``REGENERATE_README_SECTIONS=1``
is set.

Adding a new README source
--------------------------
Add an entry to the ``README_SOURCES`` list below:

    ReadmeSource(
        # GitHub raw URL or absolute local path string
        url="https://raw.githubusercontent.com/org/repo/main/README.md",
        # Optional: local path fallback (used when URL fetch fails or offline)
        local_path=_REPO_ROOT / "some-sibling-repo" / "README.md",
        sections=[
            # (output_slug, heading_text, heading_level)
            ("my-section", "My Section Heading", 2),
        ],
    )

Snippet files are written to ``docs/includes/readme/<slug>.md``.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent
_DEFAULT_DOCS_DIR = _SCRIPT_DIR.parent / "docs"


# ---------------------------------------------------------------------------
# README sources — add new sources here
# ---------------------------------------------------------------------------

@dataclass
class ReadmeSource:
    """A README to extract sections from."""
    # GitHub raw URL or any HTTPS URL to the raw markdown file.
    # Set to "" to skip remote fetch and use local_path only.
    url: str
    # Local path fallback. Used when url is empty or fetch fails.
    local_path: Path | None = None
    # Sections to extract: list of (output_slug, heading_text, heading_level)
    sections: list[tuple[str, str, int]] = field(default_factory=list)


README_SOURCES: list[ReadmeSource] = [
    ReadmeSource(
        url="https://raw.githubusercontent.com/US-Marine-Energy-Resource/us-marine-energy-resource-python/main/README.md",
        local_path=_REPO_ROOT / "us-marine-energy-resource-python" / "README.md",
        sections=[
            ("installation",       "Installation",                                          2),
            ("cli-point-query",    "Point query: nearest grid point",                       3),
            ("cli-area-query",     "Area query: all grid points in a bounding box",         3),
            ("cli-transect-query", "Transect query: grid points along a line",              3),
            ("cli-export-options", "Export options",                                        3),
            ("direct-downloads",   "Direct Downloads using the `tidal_hindcast` API",       2),
            ("ts-variables",       "Dataset Variables",                                     2),
        ],
    ),
    # Add additional README sources here, e.g.:
    # ReadmeSource(
    #     url="https://raw.githubusercontent.com/org/other-repo/main/README.md",
    #     local_path=_REPO_ROOT / "other-repo" / "README.md",
    #     sections=[
    #         ("other-install", "Installation", 2),
    #     ],
    # ),
]

# ---------------------------------------------------------------------------
# Derived helpers
# ---------------------------------------------------------------------------

def _all_output_filenames() -> list[str]:
    return [f"{slug}.md" for src in README_SOURCES for slug, _, _ in src.sections]


def output_dir(docs_dir: Path) -> Path:
    return docs_dir / "includes" / "readme"


def missing_outputs(docs_dir: Path) -> list[str]:
    out = output_dir(docs_dir)
    return [f for f in _all_output_filenames() if not (out / f).is_file()]


# ---------------------------------------------------------------------------
# Core extraction
# ---------------------------------------------------------------------------

def extract_section(lines: list[str], heading_text: str, level: int, strip_heading: bool = True) -> str:
    """Extract the content of a markdown section by heading text and level.

    Parameters
    ----------
    lines:
        Lines of the markdown file (with line endings preserved).
    heading_text:
        The exact heading text to search for (backticks and asterisks are
        stripped before comparison so ``## Direct Downloads using the
        `tidal_hindcast` API`` matches correctly).
    level:
        Heading level (1-6).
    strip_heading:
        When ``True`` (default), the matched heading line itself is excluded
        from the output.  The calling document is expected to provide its own
        heading, avoiding duplicate or mis-levelled headings.

    Raises
    ------
    ValueError
        If no heading matching ``heading_text`` at ``level`` is found.
    """
    marker = "#" * level + " " + heading_text
    marker_stripped = re.sub(r"[`*]", "", marker)
    start = None
    for i, line in enumerate(lines):
        stripped = re.sub(r"[`*]", "", line).rstrip()
        if stripped == marker_stripped:
            start = i
            break

    if start is None:
        raise ValueError(f"Heading not found: {marker!r}")

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^#{1," + str(level) + r"} ", lines[i]):
            end = i
            break

    content_lines = lines[start + 1 : end] if strip_heading else lines[start:end]
    return "".join(content_lines).strip() + "\n"


def _fetch_readme(source: ReadmeSource) -> list[str]:
    """Fetch README content, preferring local path over remote URL."""
    if source.local_path and source.local_path.is_file():
        return source.local_path.read_text(encoding="utf-8").splitlines(keepends=True)
    if source.url:
        print(f"  fetching {source.url} ...")
        with urllib.request.urlopen(source.url, timeout=15) as resp:
            return resp.read().decode("utf-8").splitlines(keepends=True)
    raise FileNotFoundError(
        f"No local path or URL available for README source: {source}"
    )


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def generate(docs_dir: Path, force: bool = False) -> None:
    out = output_dir(docs_dir)
    out.mkdir(parents=True, exist_ok=True)

    missing = missing_outputs(docs_dir)
    if not force and not missing:
        print("extract_readme_sections: all snippets present, skipping.")
        return

    if force:
        print("extract_readme_sections: --force, regenerating all snippets.")
    else:
        print(f"extract_readme_sections: {len(missing)} missing snippet(s), generating.")

    for source in README_SOURCES:
        slugs_needed = {slug for slug, _, _ in source.sections}
        if not force:
            slugs_needed = {s for s in slugs_needed if not (out / f"{s}.md").is_file()}
        if not slugs_needed:
            continue

        try:
            lines = _fetch_readme(source)
            label = source.local_path.name if source.local_path else source.url
            print(f"  source: {label} ({len(lines)} lines)")
        except Exception as e:
            print(f"  ERROR: could not read README ({e}) — skipping source.")
            continue

        for slug, heading, level in source.sections:
            if not force and slug not in slugs_needed:
                continue
            dest = out / f"{slug}.md"
            try:
                content = extract_section(lines, heading, level)
            except ValueError as e:
                print(f"  WARNING: {e} — skipping {slug}.md")
                continue
            dest.write_text(content, encoding="utf-8")
            print(f"  wrote {dest.relative_to(docs_dir.parent)}")

    print("extract_readme_sections: done.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--force", action="store_true", help="Regenerate even if snippets already exist.")
    p.add_argument("--docs-dir", type=Path, default=_DEFAULT_DOCS_DIR, help="Path to the MkDocs docs/ directory.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        sys.exit(f"error: docs directory not found: {docs_dir}")
    generate(docs_dir=docs_dir, force=args.force)


if __name__ == "__main__":
    main()

