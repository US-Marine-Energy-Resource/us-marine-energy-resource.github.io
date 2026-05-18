#!/usr/bin/env python3
"""Generate static plots embedded in docs/tidal/index.md.

All plots are produced from the WPTO High Resolution Tidal Hindcast dataset
via the ``us-marine-energy-resource`` Python library.  The primary example
site is Upper Cook Inlet, AK (2005).

Output images are written to ``docs/assets/tidal/`` relative to the
documentation root.  The MkDocs hook ``hooks/generate_tidal_plots.py`` calls
this script automatically during ``mkdocs build`` / ``mkdocs serve`` when any
output file is missing.  To force a full regeneration pass ``--force``:

    python scripts/generate_tidal_plots.py [--force] [--docs-dir <path>]

Requirements
------------
The ``us-marine-energy-resource`` package must be installed (editable install
from the local source tree is recommended):

    pip install -e ../us-marine-energy-resource-python

The script downloads data from the public WPTO S3 bucket on first run and
caches it locally under a ``us_tidal_cache/`` sibling directory of the
documentation root.  Subsequent runs reuse the cache.

Plots generated
---------------
1. cook_inlet_sigma_layers_speed_full.png      — full-year sigma layer speed heatmap
2. cook_inlet_sigma_layers_direction_full.png  — full-year sigma layer direction heatmap
3. cook_inlet_sigma_layers_speed_zoom.png      — 3-day zoomed sigma layer speed heatmap
4. cook_inlet_sigma_layers_direction_zoom.png  — 3-day zoomed sigma layer direction heatmap
5. cook_inlet_jpd.png                          — joint probability distribution (layer 4)
6. cook_inlet_exceedance.png                   — velocity exceedance curves (all layers)
7. tidal_asymmetry_jpd.png                     — 3-panel JPD comparison (Tacoma Narrows,
                                                 Admiralty Inlet, Piscataqua River) illustrating
                                                 tidal asymmetry

Planned (pending library refactor of plot_tidal_harmonic_analysis into per-panel functions)
8. cook_inlet_harmonics.png                    — tidal harmonic constituent amplitudes
"""

from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_DOCS_DIR = _SCRIPT_DIR.parent / "docs"

# ---------------------------------------------------------------------------
# Expected output files — checked by the hook to decide whether to regenerate
# ---------------------------------------------------------------------------

OUTPUT_FILENAMES: list[str] = [
    "cook_inlet_sigma_layers_speed_full.png",
    "cook_inlet_sigma_layers_direction_full.png",
    "cook_inlet_sigma_layers_speed_zoom.png",
    "cook_inlet_sigma_layers_direction_zoom.png",
    "cook_inlet_jpd.png",
    "cook_inlet_exceedance.png",
    "tidal_asymmetry_jpd.png",
]


def output_dir(docs_dir: Path) -> Path:
    return docs_dir / "assets" / "tidal"


def missing_outputs(docs_dir: Path) -> list[str]:
    """Return the list of expected output filenames that do not yet exist."""
    out = output_dir(docs_dir)
    return [f for f in OUTPUT_FILENAMES if not (out / f).is_file()]


# ---------------------------------------------------------------------------
# Plot generation
# ---------------------------------------------------------------------------

def generate(docs_dir: Path, force: bool = False) -> None:
    """Generate all tidal index plots and save them to *docs_dir*/assets/tidal/.

    Parameters
    ----------
    docs_dir:
        Absolute path to the MkDocs ``docs/`` directory.
    force:
        When ``True``, regenerate every file even if it already exists.
    """
    out = output_dir(docs_dir)
    out.mkdir(parents=True, exist_ok=True)

    missing = missing_outputs(docs_dir)
    if not force and not missing:
        print("generate_tidal_plots: all outputs present, skipping.")
        return

    if force:
        print("generate_tidal_plots: --force flag set, regenerating all plots.")
    else:
        print(f"generate_tidal_plots: {len(missing)} missing file(s), generating.")

    # ------------------------------------------------------------------
    # Late imports — only needed when we actually generate
    # ------------------------------------------------------------------
    warnings.filterwarnings("ignore")

    import matplotlib
    matplotlib.use("Agg")  # headless — no display required
    import matplotlib.pyplot as plt
    import pandas as pd

    from us_marine_energy_resource import tidal_hindcast as tidal
    from us_marine_energy_resource.tidal_hindcast import PlotSettings

    # ------------------------------------------------------------------
    # Load data via the high-level facade
    # ------------------------------------------------------------------
    SITE_LAT = 60.735016
    SITE_LON = -151.431396
    SITE_LABEL = "Cook Inlet, Near Nikiski, AK"

    # Point the cache at the sibling us_tidal_cache/ directory so that
    # downloaded parquet files are shared with any other tools in this repo.
    cache_dir = docs_dir.parent / "us_tidal_cache"

    print(f"  Fetching data for {SITE_LABEL} ({SITE_LAT}, {SITE_LON})...")
    df = tidal.get_data_at_point(lat=SITE_LAT, lon=SITE_LON, cache_dir=cache_dir)
    print(f"  -> loaded {len(df):,} timesteps  ({df.index[0].date()} → {df.index[-1].date()})")

    # Zoom window — 3 days starting 7 days into the record
    _zoom_start = df.index[0] + pd.Timedelta(days=7)
    zoom_start = str(_zoom_start.date())
    zoom_end = str((_zoom_start + pd.Timedelta(days=3)).date())

    # ------------------------------------------------------------------
    # Helper — save figure, close it, and report
    # ------------------------------------------------------------------
    def _save(fig: plt.Figure, name: str) -> None:
        path = out / name
        fig.savefig(path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        print(f"  saved {path.relative_to(docs_dir.parent)}")

    # ------------------------------------------------------------------
    # 1. Sigma layer speed — full year
    # ------------------------------------------------------------------
    fig, _ax = tidal.plot_sigma_layers_speed(
        df,
        settings=PlotSettings(
            title=f"Full Model Year | Current Speed | {SITE_LABEL}",
            fig_width=9,
            fig_height=2.5,
            caption=f"Latitude: {SITE_LAT}, Longitude: {SITE_LON}",
        ),
    )
    _save(fig, "cook_inlet_sigma_layers_speed_full.png")

    # ------------------------------------------------------------------
    # 2. Sigma layer direction — full year
    # ------------------------------------------------------------------
    fig, _ax = tidal.plot_sigma_layers_direction(
        df,
        settings=PlotSettings(
            title=f"Full Model Year | Direction [deg cw from True North] | {SITE_LABEL}",
            fig_width=9,
            fig_height=2.5,
            caption=f"Latitude: {SITE_LAT}, Longitude: {SITE_LON}",
        ),
    )
    _save(fig, "cook_inlet_sigma_layers_direction_full.png")

    # ------------------------------------------------------------------
    # 3. Sigma layer speed — 3-day zoom
    # ------------------------------------------------------------------
    fig, _ax = tidal.plot_sigma_layers_speed(
        df,
        settings=PlotSettings(
            title=f"3 Days | Current Speed | {SITE_LABEL}",
            start_date=zoom_start,
            end_date=zoom_end,
            fig_width=8,
            fig_height=3,
            caption=f"Latitude: {SITE_LAT}, Longitude: {SITE_LON}",
        ),
    )
    _save(fig, "cook_inlet_sigma_layers_speed_zoom.png")

    # ------------------------------------------------------------------
    # 4. Sigma layer direction — 3-day zoom
    # ------------------------------------------------------------------
    fig, _ax = tidal.plot_sigma_layers_direction(
        df,
        settings=PlotSettings(
            title=f"3 Days | Direction [deg cw from True North] | {SITE_LABEL}",
            start_date=zoom_start,
            end_date=zoom_end,
            fig_width=8,
            fig_height=3,
            caption=f"Latitude: {SITE_LAT}, Longitude: {SITE_LON}",
        ),
    )
    _save(fig, "cook_inlet_sigma_layers_direction_zoom.png")

    # ------------------------------------------------------------------
    # 5. Joint probability distribution — sigma layer 4
    # ------------------------------------------------------------------
    fig = tidal.generate_tidal_joint_probability(
        df,
        sigma_layer=4,
        settings=PlotSettings(
            title=f"Joint Probability Distribution\n{SITE_LABEL}\nSigma Layer 4",
            fig_width=8,
            fig_height=8,
            caption=f"Latitude: {SITE_LAT}, Longitude: {SITE_LON}",
        ),
    )
    _save(fig, "cook_inlet_jpd.png")

    # ------------------------------------------------------------------
    # 6. Velocity exceedance — all sigma layers
    # ------------------------------------------------------------------
    fig, _stats = tidal.plot_velocity_exceedance(
        df,
        settings=PlotSettings(
            title=f"Velocity Exceedance | {SITE_LABEL}",
            fig_width=10,
            fig_height=5,
            caption=f"Latitude: {SITE_LAT}, Longitude: {SITE_LON}",
        ),
    )
    _save(fig, "cook_inlet_exceedance.png")

    # ------------------------------------------------------------------
    # 7. Tidal asymmetry JPD comparison — Tacoma Narrows, Admiralty Inlet,
    #    Piscataqua River (bottom sigma layer)
    # ------------------------------------------------------------------
    asymmetry_sites = [
        {"label": "Tacoma Narrows, WA",    "lat": 47.270191, "lon": -122.548172},
        {"label": "Admiralty Inlet, WA",   "lat": 48.173931, "lon": -122.774963},
        {"label": "UNH Living Bridge, NH", "lat": 43.079498, "lon": -70.752319},
    ]

    print("  Fetching data for tidal asymmetry comparison sites...")
    site_records_jpd = []
    for site in asymmetry_sites:
        print(f"    {site['label']}")
        df_site = tidal.get_data_at_point(
            lat=site["lat"], lon=site["lon"], cache_dir=cache_dir
        )
        site_records_jpd.append((site["label"], df_site, 0))

    fig = tidal.plot_jpd_comparison_grid(
        site_records_jpd,
        ncols=3,
        settings=PlotSettings(
            title="Joint Probability Distribution | Tidal Asymmetry Examples",
            fig_width=14,
            fig_height=5,
        ),
    )
    _save(fig, "tidal_asymmetry_jpd.png")

    print("generate_tidal_plots: done.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--force",
        action="store_true",
        help="Regenerate every plot even if the output files already exist.",
    )
    p.add_argument(
        "--docs-dir",
        type=Path,
        default=_DEFAULT_DOCS_DIR,
        help="Path to the MkDocs docs/ directory (default: %(default)s).",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        sys.exit(f"error: docs directory not found: {docs_dir}")
    generate(docs_dir=docs_dir, force=args.force)


if __name__ == "__main__":
    main()
