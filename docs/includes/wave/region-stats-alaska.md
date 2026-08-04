- **Grid points:** 3,894,283
- **File size:** ~399.1 GB per year
- **Total archive:** ~16.4 TB
- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Version:** `v1.0.1`

??? note "Spatiotemporal variables (9)"

    | Variable | Description | IEC name | SWAN name | Units | Dimensions | Type |
    |:---|:---|:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Directionality coefficient | d |  |  | 2,928 × 3,894,283 | `float32` |
    | `energy_period` | Energy period | T_e,T_-10 | TMM10 | s | 2,928 × 3,894,283 | `float32` |
    | `maximum_energy_direction` | Direction of maximum directionally resolved wave power (nautical convention) | theta_J |  | degr | 2,928 × 3,894,283 | `float32` |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s | 2,928 × 3,894,283 | `float32` |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr | 2,928 × 3,894,283 | `float32` |
    | `omni-directional_wave_power` | Omnidirectional wave power | J |  | W/m | 2,928 × 3,894,283 | `float32` |
    | `peak_period` | Relative peak period of the variance density spectrum | T_p | RTP | s | 2,928 × 3,894,283 | `float32` |
    | `significant_wave_height` | Significant wave height | H_m0 | HSIGN | m | 2,928 × 3,894,283 | `float32` |
    | `spectral_width` | Spectral width | epsilon_0 |  |  | 2,928 × 3,894,283 | `float32` |

??? note "Metadata (6 fields)"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `float32` |
    | `distance` | `float32` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |
