- **Grid points:** 4,656,637
- **File size:** ~572.8 GB per year
- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~23.5 TB
- **Version:** `v1.0.1`

??? note "Spatiotemporal variables (11)"

    | Variable | Description | IEC name | SWAN name | Units | Dimensions | Type |
    |:---|:---|:---|:---|:---|:---|:---|
    | `direction_of_maximum_directionally_resolved_wave_power` | Direction of maximum directionally resolved wave power (nautical convention) | theta_J |  | degr | 2,928 × 4,656,637 | `float32` |
    | `directionality_coefficient` | Directionality coefficient | d |  |  | 2,928 × 4,656,637 | `float32` |
    | `energy_period` | Energy period | T_e,T_-10 | TMM10 | s | 2,928 × 4,656,637 | `float32` |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s | 2,928 × 4,656,637 | `float32` |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr | 2,928 × 4,656,637 | `float32` |
    | `mean_zero-crossing_period` | Mean absolute zero-crossing period | T_z,T_02 | TM02 | s | 2,928 × 4,656,637 | `float32` |
    | `omnidirectional_wave_power` | Omnidirectional wave power | J |  | W/m | 2,928 × 4,656,637 | `float32` |
    | `peak_period` | Relative peak period of the variance density spectrum | T_p | RTP | s | 2,928 × 4,656,637 | `float32` |
    | `peak_wave_direction` | Peak wave direction (nautical convention) |  | PDIR | degr | 2,928 × 4,656,637 | `float32` |
    | `significant_wave_height` | Significant wave height | H_m0 | HSIGN | m | 2,928 × 4,656,637 | `float32` |
    | `spectral_width` | Spectral width | epsilon_0 |  |  | 2,928 × 4,656,637 | `float32` |

??? note "Metadata (6 fields)"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `int16` |
    | `depth` | `float32` |
    | `distance_to_shore` | `float32` |
    | `jurisdiction` | `str[19]` |
