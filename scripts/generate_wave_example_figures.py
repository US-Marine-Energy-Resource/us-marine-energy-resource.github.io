"""
Generate static example figures for the wave/index.md page.

Downloads 5 years (2016-2020) of 3-hour hindcast data at the PacWave site
(44.624N, 124.279W) near Newport, OR via MHKit HSDS and produces
6 PNGs into docs/assets/wave/:

  pacwave_wave_height_timeseries.png   -- significant wave height, multi-year overlay
  pacwave_energy_period_timeseries.png -- energy period, multi-year overlay
  pacwave_wave_power_timeseries.png    -- omni-directional wave power, multi-year overlay
  pacwave_monthly_barchart.png         -- monthly mean Hm0 with inter-annual spread
  pacwave_scatter_diagram.png          -- Hm0 x Te joint probability distribution (5-yr)
  pacwave_environmental_contour.png    -- 25, 50, 100-yr PCA contours (5-yr)

Usage:
    python3 scripts/generate_wave_example_figures.py [--force]

Requires:
    - mhkit installed (pip install mhkit)
    - seaborn installed (pip install seaborn)
    - NREL API key configured: hsconfigure
"""

import argparse
import contextlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
import cmocean

from mhkit.wave.io.hindcast.hindcast import request_wpto_point_data
from mhkit.wave import graphics as wave_graphics
from mhkit.wave.contours import environmental_contours

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LAT_LON       = (44.624076, -124.280097)   # PacWave, Newport OR
LOCATION_NAME = "PacWave, Newport OR"
TITLE_PREFIX  = "Modeled "  # trailing space; set to "" to remove the qualifier entirely
YEARS         = [2016, 2017, 2018, 2019, 2020]
DATA_TYPE     = "3-hour"
REF_YEAR      = 2000   # leap year, used as common x-axis for multi-year overlay

SCRIPT_DIR = Path(__file__).parent
OUT_DIR    = SCRIPT_DIR.parent / "docs" / "assets" / "wave"

FIGURES = {
    "wave_height_timeseries":        OUT_DIR / "pacwave_wave_height_timeseries.png",
    "energy_period_timeseries":      OUT_DIR / "pacwave_energy_period_timeseries.png",
    "wave_power_timeseries":         OUT_DIR / "pacwave_wave_power_timeseries.png",
    "monthly_barchart_hm0":          OUT_DIR / "pacwave_monthly_barchart_hm0.png",
    "monthly_barchart_te":           OUT_DIR / "pacwave_monthly_barchart_te.png",
    "monthly_barchart_j":            OUT_DIR / "pacwave_monthly_barchart_j.png",
    "scatter_diagram":               OUT_DIR / "pacwave_scatter_diagram.png",
    "environmental_contour":         OUT_DIR / "pacwave_environmental_contour.png",
}

_palette   = sns.color_palette()
COLOR_HM0  = _palette[0]   # Hm0 (blue)
COLOR_TE   = _palette[1]   # Te  (orange)
COLOR_J    = _palette[2]   # J   (green)
_tab10     = list(plt.cm.tab10.colors)
COLOR_C25  = _tab10[1]     # 25-yr contour  (tab10 orange)
COLOR_C50  = _tab10[2]     # 50-yr contour  (tab10 green)
COLOR_C100 = _tab10[3]     # 100-yr contour (tab10 red)
GREY_LINE  = "0.72"   # per-year trace colour

DPI            = 150
FIGSIZE_TS     = (8, 2.5)
FIGSIZE_BAR    = (8, 3.0)
FIGSIZE_SQUARE = (7, 6)

sns.set_theme(context="notebook")

_SOURCE_CAPTION = (
    "Source: U.S. DOE H2O Wave Hindcast, Yang et al., 2020  |  "
    f"Latitude: {LAT_LON[0]}, Longitude: {LAT_LON[1]}"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _savefig(fig: plt.Figure, path: Path, caption_extra: str = "") -> None:
    _add_caption(fig, caption_extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved: {path.name}")


def _add_caption(fig: plt.Figure, extra: str = "") -> None:
    caption = _SOURCE_CAPTION + (f"  |  {extra}" if extra else "")
    fig_h = fig.get_figheight()
    margin = (8 / 72.0 + 0.04) / fig_h
    fig.text(0.01, 0.01, caption, ha="left", va="bottom", fontsize=8, color="0.55")
    with contextlib.suppress(Exception):
        fig.subplots_adjust(bottom=fig.subplotpars.bottom + margin)


def _fetch(parameter: str) -> pd.Series:
    """Fetch a parameter one year at a time and return as a single concatenated Series."""
    chunks = []
    for yr in YEARS:
        df, _ = request_wpto_point_data(DATA_TYPE, parameter, LAT_LON, [yr])
        col = df.columns[0]
        s = df[col].copy()
        s.index = pd.to_datetime(s.index, utc=True)
        chunks.append(s)
        print(f"    {yr} ok ({len(s)} records)")
    combined = pd.concat(chunks)
    combined.name = parameter
    return combined


# --8<-- [start:ts_helpers]
def _to_ref_year(s: pd.Series, year: int) -> pd.Series:
    """Map one calendar year's data onto REF_YEAR for overlay alignment."""
    mask = s.index.year == year
    sub  = s[mask].copy()
    new_idx = sub.index.map(lambda t: t.replace(year=REF_YEAR))
    return pd.Series(sub.values, index=new_idx, name=str(year))


def _multiyear_df(s: pd.Series) -> pd.DataFrame:
    """Return a DataFrame with one column per year, index aligned to REF_YEAR."""
    frames = {yr: _to_ref_year(s, yr) for yr in YEARS}
    return pd.DataFrame(frames)


def _apply_ts_xaxis(ax: plt.Axes, index: pd.DatetimeIndex) -> None:
    """Monthly ticks (Jan to Dec labels only; year suppressed for overlay plots)."""
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlim(index[0], index[-1])
    ax.margins(x=0)
    ax.set_xlabel("Time [UTC]")
# --8<-- [end:ts_helpers]


def _plot_multiyear(ax: plt.Axes, df: pd.DataFrame, color: str) -> None:
    """Plot per-year grey traces and a bold colored mean line."""
    for yr in YEARS:
        if yr in df.columns:
            ax.plot(df.index, df[yr].values,
                    color=GREY_LINE, linewidth=0.5, alpha=0.8, zorder=1)
    mean = df.mean(axis=1)
    ax.plot(mean.index, mean.values,
            color=color, linewidth=1.8, zorder=2, label=f"{YEARS[0]} to {YEARS[-1]} mean")
    ax.legend(fontsize=8, loc="upper right")


# ---------------------------------------------------------------------------
# Figure 1 -- Significant wave height time series
# ---------------------------------------------------------------------------

# --8<-- [start:wave_height_ts]
def fig_wave_height_timeseries(Hm0: pd.Series, force: bool = False) -> None:
    out = FIGURES["wave_height_timeseries"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return

    df  = _multiyear_df(Hm0)
    fig, ax = plt.subplots(figsize=FIGSIZE_TS)
    _plot_multiyear(ax, df, COLOR_HM0)
    _apply_ts_xaxis(ax, df.index)
    ax.set_ylabel("$H_{m0}$ [m]")
    ax.set_title(f"{TITLE_PREFIX}Significant Wave Height, $H_{{m0}}$ [m] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out)
# --8<-- [end:wave_height_ts]
# ---------------------------------------------------------------------------

# --8<-- [start:energy_period_ts]
def fig_energy_period_timeseries(Te: pd.Series, force: bool = False) -> None:
    out = FIGURES["energy_period_timeseries"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return

    df  = _multiyear_df(Te)
    fig, ax = plt.subplots(figsize=FIGSIZE_TS)
    _plot_multiyear(ax, df, COLOR_TE)
    _apply_ts_xaxis(ax, df.index)
    ax.set_ylabel("$T_e$ [s]")
    ax.set_title(f"{TITLE_PREFIX}Energy Period, $T_e$ [s] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out)
# --8<-- [end:energy_period_ts]


# ---------------------------------------------------------------------------
# Figure 3 -- Omni-directional wave power time series
# ---------------------------------------------------------------------------

# --8<-- [start:wave_power_ts]
def fig_wave_power_timeseries(J: pd.Series, force: bool = False) -> None:
    out = FIGURES["wave_power_timeseries"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return

    J_kW = J / 1000.0
    df   = _multiyear_df(J_kW)
    fig, ax = plt.subplots(figsize=FIGSIZE_TS)
    _plot_multiyear(ax, df, COLOR_J)
    _apply_ts_xaxis(ax, df.index)
    ax.set_ylabel("$J$ [kW/m]")
    ax.set_title(f"{TITLE_PREFIX}Omni-directional Wave Power, $J$ [kW/m] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out)
# --8<-- [end:wave_power_ts]


# ---------------------------------------------------------------------------
# Figures 4a, 4b, 4c -- Monthly mean bar charts (Hm0, Te, J) with inter-annual spread
# ---------------------------------------------------------------------------

def _monthly_bar(ax: plt.Axes, s: pd.Series, color, ylabel: str, title: str) -> None:
    """Shared bar chart renderer with error bars and value labels."""
    monthly_by_year = (
        s.groupby([s.index.year, s.index.month])
         .mean()
         .unstack(level=0)   # rows = month, cols = year
    )
    mean   = monthly_by_year.mean(axis=1)
    std    = monthly_by_year.std(axis=1)
    months = [pd.Timestamp(f"{REF_YEAR}-{m:02d}-01").strftime("%b")
              for m in monthly_by_year.index]

    x    = np.arange(len(months))
    bars = ax.bar(x, mean.values, color=color, alpha=0.85,
                  edgecolor="white", linewidth=0.5, zorder=2)
    ax.errorbar(x, mean.values, yerr=std.values,
                fmt="none", color="0.35", capsize=4, linewidth=1.2, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.set_title(title)


# --8<-- [start:monthly_barchart]
def fig_monthly_barchart_hm0(Hm0: pd.Series, force: bool = False) -> None:
    out = FIGURES["monthly_barchart_hm0"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return
    fig, ax = plt.subplots(figsize=FIGSIZE_BAR)
    _monthly_bar(ax, Hm0, COLOR_HM0,
                 ylabel="$H_{m0}$ [m]",
                 title=f"{TITLE_PREFIX}Significant Wave Height, $H_{{m0}}$ [m] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out)


def fig_monthly_barchart_te(Te: pd.Series, force: bool = False) -> None:
    out = FIGURES["monthly_barchart_te"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return
    fig, ax = plt.subplots(figsize=FIGSIZE_BAR)
    _monthly_bar(ax, Te, COLOR_TE,
                 ylabel="$T_e$ [s]",
                 title=f"{TITLE_PREFIX}Energy Period, $T_e$ [s] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out)


def fig_monthly_barchart_j(J: pd.Series, force: bool = False) -> None:
    out = FIGURES["monthly_barchart_j"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return
    J_kW = J / 1000.0
    fig, ax = plt.subplots(figsize=FIGSIZE_BAR)
    _monthly_bar(ax, J_kW, COLOR_J,
                 ylabel="$J$ [kW/m]",
                 title=f"{TITLE_PREFIX}Omni-directional Wave Power, $J$ [kW/m] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out)
# --8<-- [end:monthly_barchart]


# ---------------------------------------------------------------------------
# Figure 5 -- Hm0 x Te joint probability distribution (all years)
# ---------------------------------------------------------------------------

# Shared helpers for JPD and environmental-contour plots
def _wave_bin_edges(Hm0: pd.Series, Te: pd.Series,
                    Te_max_override: float | None = None,
                    Hm0_max_override: float | None = None):
    """Return (Hm0_edges, Te_edges) used by both the JPD and contour plots.

    Te axis starts at 3 s.  Optional overrides let the contour function expand
    the edges to cover the full envelope extent before calling _apply_matrix_axes.
    """
    hm0_max = max(Hm0.max(), Hm0_max_override or 0.0)
    te_max  = max(Te.max(),  Te_max_override  or 0.0)
    Hm0_edges = np.arange(0.0, hm0_max + 0.5, 0.5)
    Te_edges  = np.arange(3.0, te_max  + 1.0, 1.0)
    return Hm0_edges, Te_edges


def _apply_matrix_axes(ax: plt.Axes,
                       Hm0_edges: np.ndarray, Te_edges: np.ndarray,
                       grid_color: str = "white") -> None:
    """Shared axis limits, bin-edge ticks, and minor-style gridlines.

    Buffers are one full bin-width on every side so the outermost cells are
    entirely visible with a clear margin.
    """
    te_step  = Te_edges[1]  - Te_edges[0]   # 1 s
    hm0_step = Hm0_edges[1] - Hm0_edges[0]  # 0.5 m
    ax.set_xlim(Te_edges[0]  - te_step,  Te_edges[-1]  + te_step)
    ax.set_ylim(Hm0_edges[0] - hm0_step, Hm0_edges[-1] + hm0_step)
    ax.set_xticks(Te_edges)
    ax.set_yticks(Hm0_edges)
    ax.tick_params(which="both", length=0)          # hide tick marks; labels stay
    ax.grid(True, which="major", color=grid_color, linewidth=0.5, alpha=0.6)
    ax.set_xlabel("$T_e$ [s]")
    ax.set_ylabel("$H_{m0}$ [m]")


# --8<-- [start:scatter_diagram]
def fig_scatter_diagram(Hm0: pd.Series, Te: pd.Series, force: bool = False) -> None:
    out = FIGURES["scatter_diagram"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return

    Hm0_edges, Te_edges = _wave_bin_edges(Hm0, Te)

    # Bin using left edges as labels so the matrix index/columns are the bin edges
    H_bins = pd.cut(Hm0, bins=Hm0_edges, labels=Hm0_edges[:-1])
    T_bins = pd.cut(Te,  bins=Te_edges,  labels=Te_edges[:-1])

    matrix = pd.crosstab(H_bins, T_bins).replace(0, np.nan)
    matrix = (matrix / matrix.sum().sum() * 100)   # convert counts to %
    matrix.index   = matrix.index.astype(float)
    matrix.columns = matrix.columns.astype(float)

    # Re-index to the full grid so pcolormesh sees every bin slot
    matrix = matrix.reindex(index=Hm0_edges[:-1], columns=Te_edges[:-1])
    Z = matrix.values   # shape: (n_Hm0_bins, n_Te_bins)

    n_hours = int(len(Hm0) * 3)
    fig, ax = plt.subplots(figsize=FIGSIZE_SQUARE)

    cmap = cmocean.cm.haline
    pcm  = ax.pcolormesh(Te_edges, Hm0_edges, Z, cmap=cmap, vmin=0)

    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Probability of Occurrence [%]", rotation=270, labelpad=16)

    _apply_matrix_axes(ax, Hm0_edges, Te_edges, grid_color="0.80")
    ax.set_title(f"{TITLE_PREFIX}Joint Probability Distribution [%] | {LOCATION_NAME}")
    fig.tight_layout()
    _savefig(fig, out,
             f"N\u2009=\u2009{n_hours:,} hours  ·  {len(YEARS)} years "
             f"({YEARS[0]}\u2013{YEARS[-1]})")
# --8<-- [end:scatter_diagram]


# ---------------------------------------------------------------------------
# Figure 6 -- Environmental contours (25, 50, 100-yr return, PCA, all years)
# ---------------------------------------------------------------------------

# --8<-- [start:environmental_contour]
def fig_environmental_contour(Hm0: pd.Series, Te: pd.Series, force: bool = False) -> None:
    out = FIGURES["environmental_contour"]
    if out.exists() and not force:
        print(f"  skip (exists): {out.name}")
        return

    sea_state_duration = 3 * 3600
    n_hours = int(len(Hm0) * 3)

    # Pre-compute all contours so we can size the axes to contain them fully
    contour_specs = [(25, COLOR_C25, "-"), (50, COLOR_C50, "-"), (100, COLOR_C100, "-")]
    contours = []
    for rp, color, ls in contour_specs:
        c = environmental_contours(
            Hm0.values, Te.values,
            sea_state_duration=sea_state_duration,
            return_period=rp,
            method="PCA",
        )
        contours.append((rp, color, ls, np.array(c["PCA_x1"]), np.array(c["PCA_x2"])))

    # Expand bin edges so the largest contour envelope is fully inside the axes
    Te_max_c  = max(Te_c.max()  for _, _, _, _,     Te_c  in contours)
    Hm0_max_c = max(Hm0_c.max() for _, _, _, Hm0_c, _     in contours)
    Hm0_edges, Te_edges = _wave_bin_edges(
        Hm0, Te,
        Te_max_override=Te_max_c,
        Hm0_max_override=Hm0_max_c,
    )

    fig, ax = plt.subplots(figsize=FIGSIZE_SQUARE)

    # Scatter dots: sns palette[0] with opacity
    ax.scatter(Te.values, Hm0.values, s=2, alpha=0.10, color=COLOR_HM0,
               label=f"Sea states ({YEARS[0]} to {YEARS[-1]})", zorder=1)

    for rp, color, ls, Hm0_c, Te_c in contours:
        # Close the contour without re-sorting (sorting scrambles the closed-loop
        # point order into a zigzag that renders as a filled polygon)
        ax.plot(np.append(Te_c, Te_c[0]), np.append(Hm0_c, Hm0_c[0]),
                color=color, linewidth=2, linestyle=ls,
                label=f"{rp}-yr return (PCA)", zorder=3)

    _apply_matrix_axes(ax, Hm0_edges, Te_edges, grid_color="white")
    ax.set_title(f"{TITLE_PREFIX}Environmental Contours, $H_{{m0}}$ vs $T_e$ | {LOCATION_NAME}")
    leg = ax.legend(fontsize=9)
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_alpha(1.0)
    fig.tight_layout()
    _savefig(fig, out,
             f"N\u2009=\u2009{n_hours:,} hours  ·  {len(YEARS)} years "
             f"({YEARS[0]}\u2013{YEARS[-1]})")
# --8<-- [end:environmental_contour]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate wave example figures.")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate figures even if they already exist.")
    args = parser.parse_args()

    print(f"PacWave example figures -> {OUT_DIR}")
    print(f"Fetching {YEARS[0]}-{YEARS[-1]} hindcast data at {LAT_LON} ...")

    print("  downloading significant_wave_height ...")
    Hm0 = _fetch("significant_wave_height")

    print("  downloading energy_period ...")
    Te = _fetch("energy_period")

    print("  downloading omni-directional_wave_power ...")
    J  = _fetch("omni-directional_wave_power")

    print("Generating figures ...")
    fig_wave_height_timeseries(Hm0, force=args.force)
    fig_energy_period_timeseries(Te, force=args.force)
    fig_wave_power_timeseries(J, force=args.force)
    fig_monthly_barchart_hm0(Hm0, force=args.force)
    fig_monthly_barchart_te(Te, force=args.force)
    fig_monthly_barchart_j(J, force=args.force)
    fig_scatter_diagram(Hm0, Te, force=args.force)
    fig_environmental_contour(Hm0, Te, force=args.force)

    print("Done.")


if __name__ == "__main__":
    main()
