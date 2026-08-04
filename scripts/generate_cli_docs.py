#!/usr/bin/env python3
"""Generate CLI reference snippet for docs/tidal/high_resolution_hindcast/data-access.md.

Runs ``us-tidal --help`` and writes the output as a fenced bash code block to
``docs/includes/us-tidal-help.md``.  The MkDocs hook ``hooks/generate_cli_docs.py``
calls this script automatically during ``mkdocs build`` / ``mkdocs serve`` when
the snippet file is missing or the ``REGENERATE_CLI_DOCS=1`` env var is set.

To force regeneration:

    python scripts/generate_cli_docs.py [--docs-dir <path>]

Requirements
------------
The ``us-marine-energy-resource`` package must be installed so that the
``us-tidal`` entry point is available on the PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_DOCS_DIR = _SCRIPT_DIR.parent / "docs"

OUTPUT_FILENAME = "us-tidal-help.md"


def output_path(docs_dir: Path) -> Path:
    return docs_dir / "includes" / OUTPUT_FILENAME


def generate(docs_dir: Path, force: bool = False) -> None:
    out = output_path(docs_dir)

    if not force and out.is_file():
        print("generate_cli_docs: snippet present, skipping.")
        return

    us_tidal = shutil.which("us-tidal")
    if us_tidal is None:
        sys.exit(
            "error: us-tidal not found on PATH. "
            "Install the us-marine-energy-resource package first:\n"
            "  pip install -e ../us-marine-energy-resource-python"
        )

    print(f"generate_cli_docs: running {us_tidal} --help ...")
    result = subprocess.run(
        [us_tidal, "--help"],
        capture_output=True,
        text=True,
    )

    # Strip ANSI escape codes for clean markdown output.
    import re
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    help_text = ansi_escape.sub("", result.stdout).rstrip()

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"```\n{help_text}\n```\n")
    print(f"generate_cli_docs: wrote {out.relative_to(docs_dir.parent)}")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--force", action="store_true", help="Regenerate even if the snippet already exists.")
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
