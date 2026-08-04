# Data Access

## Tidal Hindcast

The tidal hindcast data is available through three interfaces depending on your workflow.

### Marine Energy Atlas

The [Marine Energy Atlas](https://maps.nlr.gov/marine-energy-atlas) provides a point-and-click interface for exploring time- and depth-averaged current speed and power density across all five hindcast domains. Use it for initial site screening before downloading time series data.

### Python / CLI Quick Start

The [`us-marine-energy-resource` Python library](https://github.com/US-Marine-Energy-Resource/us-marine-energy-resource.github.io) (which includes the `us-tidal` CLI) can query tidal hindcast data by point, transect, or area, with built-in tools to visualize and analyze the results.

```python
import us_marine_energy_resource.tidal_hindcast as tidal

# Fetch the full hindcast time series for the nearest grid point.
# Data is downloaded from S3 and cached locally on first call.
df = tidal.get_data_at_point(lat=60.73, lon=-151.43)

# Plot velocity exceedance curves across all depth layers.
fig, stats = tidal.plot_velocity_exceedance(df)

# Plot the joint probability distribution at a single depth layer.
fig = tidal.generate_tidal_joint_probability(df, sigma_layer=4)
```

### Bulk Access (HSDS and AWS S3)

For bulk downloads or programmatic access to the raw parquet files, the data is available via HSDS and AWS S3.

<div class="btn-right">
<a href="../tidal/high_resolution_hindcast/data-access/" class="md-button md-button--site">Full tidal data access documentation</a>
<a href="https://mhkdr.openei.org/submissions/632" class="md-button md-button--site">Download Tidal Dataset on MHKDR</a>
</div>

## Wave Hindcast

Wave hindcast data is available via HSDS and AWS S3 using the [`rex`](https://github.com/NatLabRockies/rex) library.

### Quick Start with rex

```python
from rex import ResourceX

wave_file = '/nrel/US_wave/West_Coast/West_Coast_wave_2010.h5'
lat_lon = (34.399408, -119.841181)

with ResourceX(wave_file, hsds=True) as f:
    lat_lon_swh = f.get_lat_lon_df('significant_wave_height', lat_lon)
```

### HSDS Paths

The HSDS endpoint is `https://developer.nlr.gov/api/hsds`.

| Region | HSDS Path Pattern | Years |
| ------ | ----------------- | ----- |
| West Coast | `/nrel/US_wave/West_Coast/West_Coast_wave_{year}.h5` | 1979–2020 |
| Atlantic | `/nrel/US_wave/Atlantic/Atlantic_wave_{year}.h5` | 1979–2020 |
| Alaska | `/nrel/US_wave/Alaska/Alaska_wave_{year}.h5` | 1979–2020 |
| Hawaii | `/nrel/US_wave/Hawaii/Hawaii_wave_{year}.h5` | 1979–2020 |

### AWS S3 Paths

The S3 bucket is `s3://wpto-pds-us-wave` (public, no credentials required).

| Region | Latest Version | S3 Path |
| ------ | -------------- | ------- |
| West Coast | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/West_Coast/` |
| Atlantic | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/Atlantic/` |
| Hawaii | v1.0.0 | `s3://wpto-pds-us-wave/v1.0.0/Hawaii/` |
| Alaska | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/Alaska/` |
| CNMI and Guam | v1.0.0 | `s3://wpto-pds-us-wave/v1.0.0/CNMI_and_Guam/` |
| Gulf of Mexico and Puerto Rico | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/Gulf_of_Mexico_and_Puerto_Rico/` |

<div class="btn-right">
<a href="../wave/" class="md-button md-button--site">Full wave data access documentation</a>
<a href="https://mhkdr.openei.org/submissions/326" class="md-button md-button--site">Download Wave Dataset on MHKDR</a>
</div>
