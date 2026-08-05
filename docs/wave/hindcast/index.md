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

See [Variables](variables.md) for the parameters available in this dataset.

## Regional Coverage

| Region | Domain Name | Latest Version | Years | S3 Browser |
| ------ | ----------- | -------------- | ----- | ---------- |
| West Coast | `West_Coast` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FWest_Coast%2F) |
| East Coast (Atlantic) | `Atlantic` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FAtlantic%2F) |
| Hawaii | `Hawaii` | v1.0.0 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.0%2FHawaii%2F) |
| Alaska | `Alaska` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FAlaska%2F) |
| CNMI and Guam | `CNMI_and_Guam` | v1.0.0 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.0%2FCNMI_and_Guam%2F) |
| Gulf of Mexico and Puerto Rico | `Gulf_of_Mexico_and_Puerto_Rico` | v1.0.1 | 1979–2020 | [Browse](https://data.openei.org/s3_viewer?bucket=wpto-pds-us-wave&prefix=v1.0.1%2FGulf_of_Mexico_and_Puerto_Rico%2F) |

!!! note "File Naming"
    Gulf of Mexico and Puerto Rico files use a shortened prefix: `GOM_PR_{year}.h5`.
    All other domains follow the pattern `{DomainName}_wave_{year}.h5`.

## IEC/TS 62600-101 Resource Parameters

[@iec_62600_101]

The six IEC/TS 62600-101 wave energy resource parameters are included in this dataset:

| IEC/TS 62600-101 Parameter | Included | Notes |
| --- | --- | --- |
| Significant wave height ($H_{m0}$) | Yes | All domains |
| Energy period ($T_e$) | Yes | All domains |
| Peak period ($T_p$) | Yes | All domains |
| Mean zero-crossing period ($T_z$) | Yes | All domains |
| Omni-directional wave power ($J$) | Yes | All domains |
| Directionality coefficient ($d$) | Yes | All domains |

See [Variables](variables.md) for full descriptions.

## Citation

[!@general_yang2020_wave_hindcast]

Please also cite the most relevant regional publication. See [References](references.md) for the full list.

## Acknowledgement

This study was funded by the U.S. Department of Energy's [Hydropower and Hydrokinetic Office (H2O)](https://www.energy.gov/cmei/water/hydropower-and-hydrokinetic-office) under Contract DE-AC05-76RL01830 to Pacific Northwest National Laboratory (PNNL).

--8<-- "docs/wave/_cite-widget.md"
