"""MkDocs hook: extract README sections as snippet files for docs/includes/readme/.

Runs ``scripts/extract_readme_sections.py`` during ``mkdocs build`` / ``mkdocs serve``
when any snippet file is missing or ``REGENERATE_README_SECTIONS=1`` is set.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.extract_readme_sections")

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "extract_readme_sections.py"


def on_pre_build(config, **kwargs) -> None:
    docs_dir = Path(config["docs_dir"]).resolve()

    scripts_dir = str(_REPO_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    try:
        from extract_readme_sections import missing_outputs  # type: ignore[import]
    except ImportError as exc:
        log.warning("extract_readme_sections hook: could not import helper — skipping. (%s)", exc)
        return
    finally:
        if scripts_dir in sys.path:
            sys.path.remove(scripts_dir)

    force = os.environ.get("REGENERATE_README_SECTIONS", "").strip() in {"1", "true", "yes"}
    missing = missing_outputs(docs_dir)

    if not force and not missing:
        log.debug("extract_readme_sections: all snippets present.")
        return

    if force:
        log.info("extract_readme_sections: REGENERATE_README_SECTIONS=1, regenerating.")
    else:
        log.info("extract_readme_sections: %d missing snippet(s) — generating.", len(missing))

    cmd = [sys.executable, str(_SCRIPT), "--docs-dir", str(docs_dir)]
    if force:
        cmd.append("--force")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        raise SystemExit(
            f"\nERROR: extract_readme_sections.py failed (exit code {result.returncode}).\n"
            f"Run directly for full output:\n  python {_SCRIPT}\n"
        )

    log.info("extract_readme_sections: snippets generated successfully.")
