# FAQ

## Can I use this data for turbine design?

Where the grid resolution is less than 500 meters these datasets are suitable for **Stage 1 (reconnaissance-level)** site assessment per IEC 62600-201. It provides free-stream resource characterization, current speed, power density, and site conditions, useful for initial site screening and comparing locations.

For detailed turbine design or array layout, **Stage 2 and Stage 3 assessments** require higher-resolution modeling with device-specific wake and blockage effects, which are included at specific locations in this dataset (Tacoma Narrows, Western Pasage). The marine energy atlas provides a Grid Resolution layer that follows this specification for determination of grid resolution. See [Limitations](limitations.md) and [Unstructured Grid](unstructured-grid.md#free-stream-velocity).

## Why only one year of data per location?

The tidal hindcast covers one year per location because:

- **Tidal currents are highly predictable** — driven by astronomical forcing that repeats on known cycles
- **One year captures the full range of tidal conditions** — including spring-neap variability and seasonal modulation
- **Computational cost** — each location requires months of supercomputer time; multi-year runs were not feasible within project scope

Interannual variability in tidal currents is generally small compared to the tidal signal itself. However, meteorological effects (storms, river discharge) that vary between years are not fully captured.

## What's the difference between depth-averaged and 95th percentile speed?

- **Depth-averaged speed** averages across all 10 sigma layers, providing a representative value for the entire water column. Used for mean current speed and mean power density.
- **95th percentile speed** takes the 95th percentile of the maximum across all sigma layers over time, capturing the a representative extreme flow anywhere in the water column without being influenced by extreme outliers.

## Why do some grid cells have very low or zero values?

Several possible reasons:

- **Shallow/intertidal areas** — Cells that dry out during low tide will have zero or near-zero time-averaged values
- **Open water boundary** — Cells near domain edges may have reduced accuracy
- **Protected embayments** — Some areas within the domain have naturally weak tidal currents

## How does this compare to NOAA tidal predictions?

NOAA tidal predictions provide water level forecasts at specific stations based on harmonic analysis. This dataset provides:

- **Spatial coverage** — 231K to 1.7M grid points vs. individual stations
- **Current velocity** — 3D velocity fields, not just water levels
- **Engineering variables** — Power density, depth, grid resolution

FVCOM [@fvcom] uses similar tidal constituents but solves the full hydrodynamic equations on a 3D unstructured grid, producing spatially continuous fields rather than point predictions.

## How do I cite this dataset?

<div class="bibliography"></div>

--8<-- "docs/tidal/high_resolution_hindcast/\_cite-widget.md"

See [References](references.md) for location-specific validation publications.
