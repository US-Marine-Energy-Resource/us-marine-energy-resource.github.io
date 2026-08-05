- **Grid points:** 4,656,637
- **File size:** ~572.8 GB per year
- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~23.5 TB
- **Version:** `v1.0.1`

??? note "Variable definitions (11)"

    | Variable | Description | IEC Name | SWAN name | Units |
    |:---|:---|:---|:---|:---|
    | `direction_of_maximum_directionally_resolved_wave_power` | Direction of maximum directionally resolved wave power (nautical convention) | $\theta_{J}$ |  | degr |
    | `directionality_coefficient` | Directionality coefficient | $d$ |  |  |
    | `energy_period` | Energy period | $T_{e}$, $T_{-10}$ | TMM10 | s |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr |
    | `mean_zero-crossing_period` | Mean absolute zero-crossing period | $T_{z}$, $T_{02}$ | TM02 | s |
    | `omnidirectional_wave_power` | Omnidirectional wave power | $J$ |  | W/m |
    | `peak_period` | Relative peak period of the variance density spectrum | $T_{p}$ | RTP | s |
    | `peak_wave_direction` | Peak wave direction (nautical convention) |  | PDIR | degr |
    | `significant_wave_height` | Significant wave height | $H_{m0}$ | HSIGN | m |
    | `spectral_width` | Spectral width | $\epsilon_{0}$ |  |  |

??? note "Variable schema (11)"

    | Variable | Units | Dimensions | Type |
    |:---|:---|:---|:---|
    | `direction_of_maximum_directionally_resolved_wave_power` | degr | 2,928 × 4,656,637 | `float32` |
    | `directionality_coefficient` |  | 2,928 × 4,656,637 | `float32` |
    | `energy_period` | s | 2,928 × 4,656,637 | `float32` |
    | `mean_absolute_period` | s | 2,928 × 4,656,637 | `float32` |
    | `mean_wave_direction` | degr | 2,928 × 4,656,637 | `float32` |
    | `mean_zero-crossing_period` | s | 2,928 × 4,656,637 | `float32` |
    | `omnidirectional_wave_power` | W/m | 2,928 × 4,656,637 | `float32` |
    | `peak_period` | s | 2,928 × 4,656,637 | `float32` |
    | `peak_wave_direction` | degr | 2,928 × 4,656,637 | `float32` |
    | `significant_wave_height` | m | 2,928 × 4,656,637 | `float32` |
    | `spectral_width` |  | 2,928 × 4,656,637 | `float32` |

??? note "Metadata (6 fields)"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `int16` |
    | `depth` | `float32` |
    | `distance_to_shore` | `float32` |
    | `jurisdiction` | `str[19]` |
