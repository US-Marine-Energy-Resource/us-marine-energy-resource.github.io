- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~18.1 TB
- **Version:** `v1.0.1`

!!! note "2 model products under one version"
    The `v1.0.1` archive changes variable set at 2011. Read across the break with care.

**2011–2020** (10 files)

- Grid points: 3,894,283 &nbsp;·&nbsp; ~399.1 GB per year

**1979–2010** (32 files)

- Grid points: 3,894,283 &nbsp;·&nbsp; ~455.2 GB per year

??? note "Spatiotemporal variables (9) · 2011–2020"

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

??? note "Metadata (6 fields) · 2011–2020"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `float32` |
    | `distance` | `float32` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |

??? note "Spatiotemporal variables (10) · 1979–2010"

    | Variable | Description | IEC name | SWAN name | Units | Dimensions | Type |
    |:---|:---|:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Directionality coefficient | d |  |  | 2,920 × 3,894,283 | `float32` |
    | `energy_period` | Energy period | T_e,T_-10 | TMM10 | s | 2,920 × 3,894,283 | `float32` |
    | `maximum_energy_direction` | Direction of maximum directionally resolved wave power (nautical convention) | theta_J |  | degr | 2,920 × 3,894,283 | `float32` |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s | 2,920 × 3,894,283 | `float32` |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr | 2,920 × 3,894,283 | `float32` |
    | `mean_zero-crossing_period` | Mean absolute zero-crossing period | T_z,T_02 | TM02 | s | 2,920 × 3,894,283 | `float32` |
    | `omni-directional_wave_power` | Omnidirectional wave power | J |  | W/m | 2,920 × 3,894,283 | `float32` |
    | `peak_period` | Relative peak period of the variance density spectrum | T_p | RTP | s | 2,920 × 3,894,283 | `float32` |
    | `significant_wave_height` | Significant wave height | H_m0 | HSIGN | m | 2,920 × 3,894,283 | `float32` |
    | `spectral_width` | Spectral width | epsilon_0 |  |  | 2,920 × 3,894,283 | `float32` |

??? note "Metadata (6 fields) · 1979–2010"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `float32` |
    | `distance` | `float32` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |
