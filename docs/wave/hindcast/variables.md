# Wave Hindcast Variables

Variables available in the U.S. WPTO wave hindcast. Each variable is requested by its **Hindcast Variable Id**, and maps directly to a [SWAN model "bulk parameter"](https://swanmodel.sourceforge.io/online_doc/swanuse/node35.html).

## Variables

| Name | SWAN Name | Symbol | Units | Hindcast Variable Id | Description |
| --- | --- | --- | --- | --- | --- |
| Significant Wave Height | `HSIGN` | $H_{m_0}$ | meters | `significant_wave_height` | Significant wave height |
| Energy Period | `TMM10` | $T_e$, $T_{-10}$ | seconds | `energy_period` | Energy period |
| Omni-Directional Wave Power | | $J$ | watts per meter | `omni-directional_wave_power` | Omnidirectional wave power |
| Mean Wave Direction | `DIR` | | degrees clockwise from true north | `mean_wave_direction` | Mean wave direction |
| Peak Period | `RTP` | $T_p$ | seconds | `peak_period` | Relative peak period of the variance density spectrum (in the absence of currents) |
| Maximum Energy Direction | | $\theta_J$ | degrees clockwise from true north | `maximum_energy_direction` | Direction of maximum wave energy |
| Directionality Coefficient | | $d$ | unitless, range from 0 to 1 | `directionality_coefficient` | Directionality coefficient |
| Spectral Width | | $\epsilon_0$ | unitless, range from 0 to 1 | `spectral_width` | Spectral width |

!!! note "Symbols"
    Symbols follow IEC 62600-101, which the standard refers to as "parameters".

## Additional Variables

| Name | SWAN Name | Symbol | Units | Hindcast Variable Id | Description |
| --- | --- | --- | --- | --- | --- |
| Mean Period | `PER` | | seconds | `mean_average_period` | Mean absolute wave period, equivalent to $T_{m_{01}}$ |
| Mean Absolute Zero Crossing Period | `TM02` | $T_z$, $T_{02}$ | seconds | `mean_zero_crossing_period` | Mean absolute zero crossing period |
| Peak Wave Direction | `PDIR` | | degrees clockwise from true north | `peak_wave_direction` | Peak wave direction, determined by wave power |

## Metadata

Each point carries an associated metadata entry in the hindcast data that identifies non time-varying values.

| Name | SWAN Name | Symbol | Units | Hindcast Variable Id |
| --- | --- | --- | --- | --- |
| X Coordinate | `XP` | | decimal degrees longitude | `longitude` |
| Y Coordinate | `YP` | | decimal degrees latitude | `latitude` |
| Depth | `DEPTH` | $h$ | meters | `depth` |

!!! note "Coming Soon"
    Per-variable documentation, including equations, valid ranges, and usage guidance, is under development.

--8<-- "docs/wave/_cite-widget.md"
