"""MkDocs hook: auto-generate static plots for docs/tidal/index.md.

During ``mkdocs build`` or ``mkdocs serve`` this hook checks whether the
expected output images already exist under ``docs/assets/tidal/``.

Behaviour
---------
* **Images present** (normal CI/local build after first run): no-op, build
  proceeds immediately.
* **Images missing** (fresh checkout, first run): the hook runs
  ``scripts/generate_tidal_plots.py`` automatically and waits for it to
  finish.  If generation succeeds the build continues; if it fails the build
  is aborted with a clear error message.
* **Force-regenerate**: set the environment variable
  ``REGENERATE_TIDAL_PLOTS=1`` to regenerate every plot regardless of whether
  the files already exist:

      REGENERATE_TIDAL_PLOTS=1 mkdocs build

The hook intentionally delegates all library imports and plot logic to the
standalone script so that:
  - The script can be run and tested independently (``python scripts/generate_tidal_plots.py``).
  - Adding new plots only requires editing the script, not this hook.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.generate_tidal_plots")

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "generate_tidal_plots.py"


def on_pre_build(config, **kwargs) -> None:
    """Check for missing tidal index plots and regenerate if needed."""

    docs_dir = Path(config["docs_dir"]).resolve()

    # Import missing_outputs lazily from the script without executing main().
    # We add the scripts/ directory to sys.path temporarily.
    scripts_dir = str(_REPO_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    try:
        from generate_tidal_plots import missing_outputs  # type: ignore[import]
    except ImportError as exc:
        log.warning("generate_tidal_plots hook: could not import helper — skipping. (%s)", exc)
        return
    finally:
        if scripts_dir in sys.path:
            sys.path.remove(scripts_dir)

    force = os.environ.get("REGENERATE_TIDAL_PLOTS", "").strip() in {"1", "true", "yes"}
    missing = missing_outputs(docs_dir)

    if not force and not missing:
        log.debug("generate_tidal_plots: all tidal index plots present.")
        return

    if force:
        log.info("generate_tidal_plots: REGENERATE_TIDAL_PLOTS=1, regenerating all plots.")
    else:
        log.info(
            "generate_tidal_plots: %d missing plot(s): %s — running generator.",
            len(missing),
            ", ".join(missing),
        )

    cmd = [
        sys.executable,
        str(_SCRIPT),
        "--docs-dir",
        str(docs_dir),
    ]
    if force:
        cmd.append("--force")

    log.info("generate_tidal_plots: running %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode != 0:
        raise SystemExit(
            "\nERROR: generate_tidal_plots.py failed (exit code "
            f"{result.returncode}).\n"
            "Run the script directly for full output:\n"
            f"  python {_SCRIPT}\n"
        )

    log.info("generate_tidal_plots: plots generated successfully.")
