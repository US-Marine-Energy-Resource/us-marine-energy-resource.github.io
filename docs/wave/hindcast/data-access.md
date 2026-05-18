# Data Access

!!! tip "First time?"
    See [Getting Started > HSDS Setup](../../getting-started/hsds-setup.md) for installation and configuration instructions.

## Quick Start with rex

```python
from rex import ResourceX

wave_file = '/nrel/US_wave/West_Coast/West_Coast_wave_2010.h5'

with ResourceX(wave_file, hsds=True) as f:
    meta = f.meta
    time_index = f.time_index
    swh = f['significant_wave_height']
```

## Dataset Paths

### HSDS Paths

The HSDS endpoint is `https://developer.nlr.gov/api/hsds`. Paths confirmed via API.

#### Standard Domains (no version prefix)

| Region | HSDS Path Pattern | Years |
| ------ | ----------------- | ----- |
| West Coast | `/nrel/US_wave/West_Coast/West_Coast_wave_{year}.h5` | 1979–2020 |
| Atlantic | `/nrel/US_wave/Atlantic/Atlantic_wave_{year}.h5` | 1979–2020 |
| Alaska | `/nrel/US_wave/Alaska/Alaska_wave_{year}.h5` | 1979–2020 |
| Hawaii | `/nrel/US_wave/Hawaii/Hawaii_wave_{year}.h5` | 1979–2020 |

#### Versioned Domains

| Region | Version | HSDS Path Pattern | Years |
| ------ | ------- | ----------------- | ----- |
| CNMI and Guam | v1.0.0 | `/nrel/US_wave/v1.0.0/CNMI_and_Guam/CNMI_and_Guam_wave_{year}.h5` | 1979–2020 |
| Gulf of Mexico and Puerto Rico | v1.0.0 | `/nrel/US_wave/v1.0.0/Gulf_of_Mexico_and_Puerto_Rico/GOM_PR_{year}.h5` | 1979–2020 |
| West Coast | v1.0.1 | `/nrel/US_wave/v1.0.1/West_Coast/West_Coast_wave_{year}.h5` | 1979–2020 |
| Atlantic | v1.0.1 | `/nrel/US_wave/v1.0.1/Atlantic/Atlantic_wave_{year}.h5` | 1979–2020 |
| Alaska | v1.0.1 | `/nrel/US_wave/v1.0.1/Alaska/Alaska_wave_{year}.h5` | 1979–2020 |
| Gulf of Mexico and Puerto Rico | v1.0.1 | `/nrel/US_wave/v1.0.1/Gulf_of_Mexico_and_Puerto_Rico/GOM_PR_{year}.h5` | 1979–2020 |

#### Virtual Buoy

| Region | HSDS Path Pattern | Years |
| ------ | ----------------- | ----- |
| West Coast | `/nrel/US_wave/virtual_buoy/West_Coast/West_Coast_virtual_buoy_{year}.h5` | 1979–2010 |

### AWS S3 Paths

The S3 bucket is `s3://wpto-pds-us-wave` (public, no credentials required).

| Region | Latest Version | S3 Path | File Pattern | Years |
| ------ | -------------- | ------- | ------------ | ----- |
| West Coast | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/West_Coast/` | `West_Coast_wave_{year}.h5` | 1979–2020 |
| Atlantic | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/Atlantic/` | `Atlantic_wave_{year}.h5` | 1979–2020 |
| Hawaii | v1.0.0 | `s3://wpto-pds-us-wave/v1.0.0/Hawaii/` | `Hawaii_wave_{year}.h5` | 1979–2020 |
| Alaska | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/Alaska/` | `Alaska_wave_{year}.h5` | 1979–2020 |
| CNMI and Guam | v1.0.0 | `s3://wpto-pds-us-wave/v1.0.0/CNMI_and_Guam/` | `CNMI_and_Guam_wave_{year}.h5` | 1979–2020 |
| Gulf of Mexico and Puerto Rico | v1.0.1 | `s3://wpto-pds-us-wave/v1.0.1/Gulf_of_Mexico_and_Puerto_Rico/` | `GOM_PR_{year}.h5` | 1979–2020 |
| Virtual Buoy (West Coast) | v1.0.0 | `s3://wpto-pds-us-wave/v1.0.0/virtual_buoy/West_Coast/` | `West_Coast_virtual_buoy_{year}.h5` | 1979–2010 |

## Extract Data at a Location

```python
from rex import ResourceX

wave_file = '/nrel/US_wave/West_Coast/West_Coast_wave_2010.h5'
lat_lon = (34.399408, -119.841181)

with ResourceX(wave_file, hsds=True) as f:
    lat_lon_swh = f.get_lat_lon_df('significant_wave_height', lat_lon)
```

## Extract Data by Region

```python
from rex import ResourceX

wave_file = '/nrel/US_wave/West_Coast/West_Coast_wave_2010.h5'
jurisdiction = 'California'

with ResourceX(wave_file, hsds=True) as f:
    ca_swh = f.get_region_df('significant_wave_height', jurisdiction,
                             region_col='jurisdiction')
```

## Direct h5pyd Access

```python
import h5pyd
import pandas as pd

with h5pyd.File('/nrel/US_wave/West_Coast/West_Coast_wave_2010.h5', mode='r') as f:
    meta = pd.DataFrame(f['meta'][...])
    swh = f['significant_wave_height']
    scale_factor = swh.attrs['scale_factor']
    mean_swh = swh[...].mean(axis=0) / scale_factor

meta['Average Wave Height'] = mean_swh
```

## AWS S3 Direct Download

```bash
# List available versions
aws s3 ls s3://wpto-pds-us-wave/ --no-sign-request

# List domains within a version
aws s3 ls s3://wpto-pds-us-wave/v1.0.1/ --no-sign-request

# Download a specific file
aws s3 cp s3://wpto-pds-us-wave/v1.0.1/West_Coast/West_Coast_wave_2010.h5 . --no-sign-request
```

See [AWS S3 Downloads](../../getting-started/aws-s3.md) for more details.
