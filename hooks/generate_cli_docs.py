"""MkDocs hook: auto-generate the us-tidal CLI reference snippet.

Runs ``scripts/generate_cli_docs.py`` during ``mkdocs build`` / ``mkdocs serve``
when ``docs/includes/us-tidal-help.md`` is missing or ``REGENERATE_CLI_DOCS=1``
is set.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.generate_cli_docs")

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "generate_cli_docs.py"


def on_pre_build(config, **kwargs) -> None:
    docs_dir = Path(config["docs_dir"]).resolve()
    snippet = docs_dir / "includes" / "us-tidal-help.md"

    force = os.environ.get("REGENERATE_CLI_DOCS", "").strip() in {"1", "true", "yes"}

    if not force and snippet.is_file():
        log.debug("generate_cli_docs: snippet present, skipping.")
        return

    if force:
        log.info("generate_cli_docs: REGENERATE_CLI_DOCS=1, regenerating.")
    else:
        log.info("generate_cli_docs: snippet missing, generating.")

    cmd = [sys.executable, str(_SCRIPT), "--docs-dir", str(docs_dir)]
    if force:
        cmd.append("--force")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        raise SystemExit(
            f"\nERROR: generate_cli_docs.py failed (exit code {result.returncode}).\n"
            f"Run directly for full output:\n  python {_SCRIPT}\n"
        )

    log.info("generate_cli_docs: snippet generated successfully.")
