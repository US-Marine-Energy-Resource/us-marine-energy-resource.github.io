# Tidal Energy Datasets

High-resolution tidal current datasets for U.S. coastal locations, generated using the Finite Volume Community Ocean Model (FVCOM) [@fvcom].

## What Are Tides?

Tides are the periodic rise and fall of sea level caused by the gravitational attraction of the Moon and Sun acting on Earth's rotating oceans [@noc_tidal_modelling]. Most U.S. coastal locations experience **semidiurnal tides**, two high waters and two low waters every ~24 hours 50 minutes.

The kinetic energy carried by tidal currents as water accelerates through constricted passages is the primary resource exploited by current energy converters (CEC).

<!--

---

## The Spring–Neap Cycle

The most important low-frequency modulation of tidal energy is the **spring–neap cycle** — a ~14.8-day oscillation driven by the alignment of the Moon and Sun [@noc_tidal_modelling]:

| Phase      | Condition                               | Relative Current Speed | Relative Power Density |
| ---------- | --------------------------------------- | ---------------------- | ---------------------- |
| **Spring** | Moon and Sun aligned (new or full moon) | ≈ 1.4× mean            | ≈ 2.7× mean            |
| **Neap**   | Moon at first/third quarter             | ≈ 0.7× mean            | ≈ 0.3× mean            |

Because tidal power density scales as $P \propto \frac{1}{2}\rho U^3$, the spring tidal current can generate roughly **8 times** the power of a neap current [@noc_tidal_modelling] — making the spring–neap cycle the dominant source of variability in tidal energy yield over a typical project assessment period.

The time series below shows one spring–neap cycle at Upper Cook Inlet, AK (2005), plotting current speed across the surface (layer 0), mid-column (layer 4), and near-bed (layer 9) sigma layers:

![Cook Inlet — one spring–neap tidal current time series (March 2005)](../assets/tidal/cook_inlet_time_series.png)

_Cook Inlet, AK — March 2005. Three sigma layers (surface, mid-column, near-bed). Generated with [`plot_tidal_time_series()`](high_resolution_hindcast/usage-examples.md) from the `us-marine-energy-resource` Python library._

---

## Tidal Harmonics and Constituents

The observed tide at any location can be decomposed into a sum of sinusoidal **tidal constituents** (harmonics), each with a fixed astronomical frequency but a locally determined amplitude and phase [@noc_tidal_modelling]. The local amplitude and phase reflect the shape of the coastline, water depth, and resonant properties of the basin.

$$Z(t) = Z_0 + \sum_{n} A_n \cos\!\left(\omega_n t + \phi_n\right)$$

where $Z_0$ is the mean water level, $A_n$ is the amplitude, $\omega_n$ is the angular frequency, and $\phi_n$ is the phase of the $n$-th constituent.

### Principal Constituents

| Constituent | Period (hours) | Type          | Description                              |
| ----------- | -------------- | ------------- | ---------------------------------------- |
| **M₂**      | 12.42          | Semidiurnal   | Principal lunar — dominant at most sites |
| **S₂**      | 12.00          | Semidiurnal   | Principal solar                          |
| **N₂**      | 12.66          | Semidiurnal   | Larger lunar elliptic                    |
| **K₁**      | 23.93          | Diurnal       | Lunar–solar diurnal                      |
| **O₁**      | 25.82          | Diurnal       | Principal lunar diurnal                  |
| **M₄**      | 6.21           | Shallow-water | Overtide of M₂                           |
| **M₆**      | 4.14           | Shallow-water | Second overtide of M₂                    |

!!! info "Shallow-water harmonics"
In constricted, shallow channels — such as **Cook Inlet** and **Piscataqua River** — shallow-water overtides (M₄, M₆) can reach amplitudes of 10–50% of M₂, producing **tidal asymmetry**: a faster flood or ebb half-cycle. This asymmetry affects sediment transport and net turbine energy output over a tidal cycle. See [Definitions](high_resolution_hindcast/definitions.md).

By fitting these constituents to the hindcast time series — **harmonic analysis** — the signal can be reconstructed and extrapolated. The figure below shows the harmonic decomposition for Cook Inlet: the observed vs. reconstructed speed, the FFT spectrum with labelled constituent periods, and a bar chart of the strongest constituent amplitudes.

![Cook Inlet — tidal harmonic analysis](../assets/tidal/cook_inlet_harmonics.png)

_Cook Inlet, AK — sigma layer 4, full year 2005. Generated with [`plot_tidal_harmonic_analysis()`](high_resolution_hindcast/usage-examples.md)._

---

## Tidal Statistics and Water Level

The tidal statistics plot shows the full-year surface elevation record with reference levels (MHHW, MHW, MSL, MLW, MLLW) and detected high/low tide events:

![Cook Inlet — tidal statistics and reference levels](../assets/tidal/cook_inlet_tidal_statistics.png)

_Cook Inlet, AK — full year 2005. Generated with [`plot_tidal_statistics()`](high_resolution_hindcast/usage-examples.md)._

---

## From Harmonics to Power Density

The instantaneous kinetic power density available to a tidal turbine is:

$$P(t) = \frac{1}{2}\,\rho\,U(t)^3 \quad [\text{W m}^{-2}]$$

where $\rho \approx 1025\,\text{kg m}^{-3}$ is seawater density. Because of the cubic relationship, doubling the current speed produces **eight times** the power.

The **exceedance curve** shows what fraction of the year the current exceeds a given speed — a key input for turbine capacity-factor estimates and IEC 62600-201 Stage 1 site screening [@iec_62600_201]:

![Cook Inlet — velocity exceedance curve](../assets/tidal/cook_inlet_exceedance.png)

_Cook Inlet, AK — sigma layers 0, 4, 9 (surface → near-bed), full year 2005. Generated with [`plot_velocity_exceedance()`](high_resolution_hindcast/usage-examples.md)._

---

## Current Direction

Tidal stream sites suitable for energy extraction are characterised by strongly bidirectional (reversing) flow. The **current direction rose** below shows that Cook Inlet has a dominant flood–ebb axis with little lateral spread, which maximises turbine capture efficiency and simplifies yaw alignment:

![Cook Inlet — current direction rose](../assets/tidal/cook_inlet_current_rose.png)

_Cook Inlet, AK — sigma layer 4, full year 2005. Generated with [`plot_current_rose()`](high_resolution_hindcast/usage-examples.md)._

---

## Vertical Current Structure (Sigma Layers)

FVCOM resolves the water column using **10 sigma (terrain-following) layers**. Current speed decreases toward the seabed due to bottom friction — a critical factor for turbine hub-height selection and blade load analysis:

![Cook Inlet — sigma layer current speed profile](../assets/tidal/cook_inlet_sigma_layers.png)

_Cook Inlet, AK — depth-averaged and per-layer statistics, full year 2005. Generated with [`plot_sigma_layers_speed()`](high_resolution_hindcast/usage-examples.md)._

For detailed background on sigma coordinates see [Sigma Layers](high_resolution_hindcast/sigma-layers.md).

---

## Energy Yield Estimate

Combining the exceedance curve with a simplified turbine power curve gives an indicative annual energy production (AEP) estimate. The figure below assumes a 10 m rotor diameter, 45% efficiency, and 0.5 m/s cut-in speed:

![Cook Inlet — tidal energy yield estimate](../assets/tidal/cook_inlet_energy_yield.png)

_Cook Inlet, AK — sigma layer 4, full year 2005. Generated with [`plot_tidal_energy_yield()`](high_resolution_hindcast/usage-examples.md)._

---

## How FVCOM Models Tidal Currents

The datasets here are produced using the **Finite Volume Community Ocean Model (FVCOM)** [@fvcom], a 3D unstructured-grid coastal ocean model. Key aspects relevant to tidal energy assessment [@noc_tidal_modelling]:

**Governing equations.** FVCOM solves the 3D Reynolds-averaged Navier–Stokes equations for horizontal velocities $u$, $v$ and sea surface elevation $\eta$ on a triangular finite-volume mesh. Tidal forcing enters as open-boundary conditions prescribed from a larger-scale ocean tidal atlas.

**Unstructured grid.** Unlike regular-grid models, FVCOM's triangular mesh can be refined around complex coastlines and constricted passages without wasting resolution in the open ocean. Grid resolution at the five U.S. sites ranges from ~10 m in narrow channels to ~500 m offshore. See [Unstructured Grid](high_resolution_hindcast/unstructured-grid.md).

**Sigma (terrain-following) coordinates.** The water column is divided into a fixed number of vertical layers that scale with local depth, so the near-bed boundary layer and the near-surface zone are always resolved regardless of water depth [@noc_tidal_modelling]. The dataset provides **10 sigma layers** per grid point. See [Sigma Layers](high_resolution_hindcast/sigma-layers.md).

**Boundary conditions.** Tidal constituents from a global ocean tidal atlas are imposed at the open boundaries of each regional model domain. The model is spun up and run for a full hindcast year to capture seasonal spring–neap variability [@noc_tidal_modelling].

**Validation.** Each site's model output is compared against tide gauge observations and, where available, ADCP current measurements, using standard skill metrics (RMSE, bias, $R^2$). See [Validation](high_resolution_hindcast/validation.md).

---

## Python Library Quick Start

The [`us-marine-energy-resource`](https://github.com/US-Marine-Energy-Resource/us-marine-energy-resource-python) Python library provides tools to query, load, and visualize the hindcast data. The images on this page were generated with it.

### Install

```bash
pip install us-marine-energy-resource
```

### Query the Nearest Grid Point

```python
from us_marine_energy_resource import S3CacheManager, TidalManifestQuery
from us_marine_energy_resource.query import find_latest_manifest_s3

cache = S3CacheManager(bucket="marine-energy-data", prefix="us-tidal")
manifest_path, _ = find_latest_manifest_s3(cache)
query = TidalManifestQuery(manifest_path, s3_cache=cache)

# Returns a parquet file path for the nearest grid cell to this lat/lon
result = query.query_nearest_point(lat=60.73, lon=-151.43)  # Upper Cook Inlet, AK
```

### Load and Prepare a Time Series

```python
from us_marine_energy_resource.analysis.preprocessing import load_parquet, prepare_dataframe

df, meta, col_meta = load_parquet(result)
df = prepare_dataframe(df, meta)

# df has a DatetimeIndex and columns including:
#   vap_sea_water_speed_layer_{0..9}          — current speed (m/s) per sigma layer
#   vap_sea_water_power_density_layer_{0..9}  — power density (W/m²) per sigma layer
#   vap_sea_water_to_direction_layer_{0..9}   — current direction (°) per sigma layer
#   vap_sigma_depth_layer_{0..9}              — depth at layer mid-point (m)
#   vap_surface_elevation                     — sea surface elevation (m)
print(df.shape, df.index.min(), df.index.max())
```

### Generate Plots

```python
import matplotlib
matplotlib.use("Agg")   # headless rendering
import matplotlib.pyplot as plt

from us_marine_energy_resource.viz.tidal import (
    plot_tidal_time_series,
    plot_velocity_exceedance,
    plot_current_rose,
    plot_sigma_layers_speed,
    plot_tidal_harmonic_analysis,
    plot_tidal_energy_yield,
)
from us_marine_energy_resource.viz.tidal import plot_tidal_statistics

# Time series — one spring–neap cycle
fig = plot_tidal_time_series(df, start_date="2005-03-01", end_date="2005-03-31", layers=[0, 4, 9])
fig.savefig("time_series.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Tidal statistics and reference levels
surface = df["vap_surface_elevation"]
fig, ax, stats = plot_tidal_statistics(surface, times=surface.index, location_label="Cook Inlet, AK", data_year="2005")
fig.savefig("tidal_statistics.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Velocity exceedance curve
fig, percentile_data = plot_velocity_exceedance(df)
fig.savefig("exceedance.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Current direction rose
fig = plot_current_rose(df, layer=4)
fig.savefig("current_rose.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Tidal harmonic analysis (observed vs reconstructed + FFT spectrum)
fig = plot_tidal_harmonic_analysis(df, layer=4, n_components=7)
fig.savefig("harmonics.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Sigma layer speed profile
fig, ax = plot_sigma_layers_speed(df)
fig.savefig("sigma_layers.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Energy yield estimate
fig = plot_tidal_energy_yield(df, layer=4, turbine_diameter=10.0, efficiency=0.45,
                               cut_in_speed=0.5, generator_rated_power_kw=100.0)
fig.savefig("energy_yield.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

!!! tip "Full worked example"
A complete site-assessment notebook covering all of these plots — plus joint probability distributions, rolling power comparisons, multi-site exceedance overlays, and turbine energy output comparisons — is available in the repository under `examples/tidal_site_assessment.ipynb`.

---

## Available Datasets

| Dataset                                                       | Locations            | Duration    | Resolution           | Grid Points        |
| ------------------------------------------------------------- | -------------------- | ----------- | -------------------- | ------------------ |
| [High Resolution Hindcast](high_resolution_hindcast/index.md) | 5 U.S. coastal sites | 1 year each | Hourly / Half-hourly | 231K–1.7M per site |

## High Resolution Hindcast

The [WPTO High Resolution Tidal Hindcast](high_resolution_hindcast/index.md) provides 3D tidal current data at five U.S. coastal locations selected for their tidal energy potential. The dataset includes depth-resolved current speed, power density, water depth, tidal range, and other engineering variables derived from FVCOM simulations.

| Location                                                  | Period    | Sampling    | Grid Points |
| --------------------------------------------------------- | --------- | ----------- | ----------- |
| [Aleutian Islands, AK](high_resolution_hindcast/index.md) | 2010–2011 | Hourly      | 797,978     |
| [Cook Inlet, AK](high_resolution_hindcast/index.md)       | 2005      | Hourly      | 392,002     |
| [Piscataqua River, NH](high_resolution_hindcast/index.md) | 2007      | Half-hourly | 292,927     |
| [Puget Sound, WA](high_resolution_hindcast/index.md)      | 2015      | Half-hourly | 1,734,765   |
| [Western Passage, ME](high_resolution_hindcast/index.md)  | 2017      | Half-hourly | 231,208     |

Click the dataset name above to view full documentation including model configuration, variable descriptions, data access, and quality assurance.

---

-->

--8<-- "docs/tidal/index-cite.md"
