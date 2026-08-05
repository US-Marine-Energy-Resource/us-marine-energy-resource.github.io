- **Grid points:** 461,465
- **File size:** ~47.3 GB per year
- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~1.9 TB
- **Version:** `v1.0.0`

??? note "Variable definitions (9)"

    | Variable | Description | IEC Name | SWAN name | Units |
    |:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Directionality coefficient | $d$ |  |  |
    | `energy_period` | Energy period | $T_{e}$, $T_{-10}$ | TMM10 | s |
    | `maximum_energy_direction` | Direction of maximum directionally resolved wave power (nautical convention) | $\theta_{J}$ |  | degr |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr |
    | `omni-directional_wave_power` | Omnidirectional wave power | $J$ |  | W/m |
    | `peak_period` | Relative peak period of the variance density spectrum | $T_{p}$ | RTP | s |
    | `significant_wave_height` | Significant wave height | $H_{m0}$ | HSIGN | m |
    | `spectral_width` | Spectral width | $\epsilon_{0}$ |  |  |

??? note "Variable schema (9)"

    | Variable | Units | Dimensions | Type |
    |:---|:---|:---|:---|
    | `directionality_coefficient` |  | 2,928 × 461,465 | `float32` |
    | `energy_period` | s | 2,928 × 461,465 | `float32` |
    | `maximum_energy_direction` | degr | 2,928 × 461,465 | `float32` |
    | `mean_absolute_period` | s | 2,928 × 461,465 | `float32` |
    | `mean_wave_direction` | degr | 2,928 × 461,465 | `float32` |
    | `omni-directional_wave_power` | W/m | 2,928 × 461,465 | `float32` |
    | `peak_period` | s | 2,928 × 461,465 | `float32` |
    | `significant_wave_height` | m | 2,928 × 461,465 | `float32` |
    | `spectral_width` |  | 2,928 × 461,465 | `float32` |

??? note "Metadata (6 fields)"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `int16` |
    | `depth` | `float32` |
    | `distance_to_shore` | `float32` |
    | `jurisdiction` | `str[24]` |
