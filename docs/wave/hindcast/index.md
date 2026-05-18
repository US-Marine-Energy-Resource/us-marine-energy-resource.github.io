# High Resolution Ocean Surface Wave Hindcast

42-year high-resolution wave hindcast covering the U.S. Exclusive Economic Zone, generated using WaveWatch III and SWAN models.

## Overview

The development of this dataset was funded by the U.S. Department of Energy's [Hydropower and Hydrokinetic Office (H2O)](https://www.energy.gov/cmei/water/hydropower-and-hydrokinetic-office) to improve our understanding of the U.S. wave energy resource and to provide critical information for wave energy project development and wave energy converter design.

This is the highest resolution publicly available long-term wave hindcast dataset covering the entire U.S. Exclusive Economic Zone (EEZ). The data can be used to investigate the historical record of wave statistics at any U.S. site and could be of value to any entity with marine operations inside the U.S. EEZ.

!!! info "Dataset Summary"
    - **Duration**: 42-Year Wave Hindcast (1979–2020)
    - **Temporal Resolution**: 3-hour intervals
    - **Spatial Resolution**: 200 meters (shallow water) to ~10 km (deep water)
    - **Coverage**: U.S. Exclusive Economic Zone

!!! info "Data Access"
    See [Getting Started](../../getting-started/index.md) for HSDS/S3 setup and [Data Access](data-access.md) for dataset-specific code examples.

## Regional Coverage

| Region | Domain Name | Latest Version | Years | S3 Browser |
| ------ | ----------- | -------------- | ----- | ---------- |
| West Coast | `West_Coast` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FWest_Coast%2F) |
| East Coast (Atlantic) | `Atlantic` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FAtlantic%2F) |
| Hawaii | `Hawaii` | v1.0.0 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.0%2FHawaii%2F) |
| Alaska | `Alaska` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FAlaska%2F) |
| CNMI and Guam | `CNMI_and_Guam` | v1.0.0 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.0%2FCNMI_and_Guam%2F) |
| Gulf of Mexico and Puerto Rico | `Gulf_of_Mexico_and_Puerto_Rico` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FGulf_of_Mexico_and_Puerto_Rico%2F) |

!!! note "File naming"
    Gulf of Mexico and Puerto Rico files use a shortened prefix: `GOM_PR_{year}.h5`.
    All other domains follow the pattern `{DomainName}_wave_{year}.h5`.

## Citation

Please cite the most relevant publication when referencing this dataset. See [References](references.md) for the full list.

## Acknowledgement

This study was funded by the U.S. Department of Energy's [Hydropower and Hydrokinetic Office (H2O)](https://www.energy.gov/cmei/water/hydropower-and-hydrokinetic-office) under Contract DE-AC05-76RL01830 to Pacific Northwest National Laboratory (PNNL).
