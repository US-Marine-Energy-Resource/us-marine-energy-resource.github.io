- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~18.1 TB
- **Version:** `v1.0.1`

**2011–2020** (10 files)

- Grid points: 3,894,283 &nbsp;·&nbsp; ~399.1 GB per year

??? note "Variable definitions (9) · 2011–2020"

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

??? note "Variable schema (9) · 2011–2020"

    | Variable | Units | Dimensions | Type |
    |:---|:---|:---|:---|
    | `directionality_coefficient` |  | 2,928 × 3,894,283 | `float32` |
    | `energy_period` | s | 2,928 × 3,894,283 | `float32` |
    | `maximum_energy_direction` | degr | 2,928 × 3,894,283 | `float32` |
    | `mean_absolute_period` | s | 2,928 × 3,894,283 | `float32` |
    | `mean_wave_direction` | degr | 2,928 × 3,894,283 | `float32` |
    | `omni-directional_wave_power` | W/m | 2,928 × 3,894,283 | `float32` |
    | `peak_period` | s | 2,928 × 3,894,283 | `float32` |
    | `significant_wave_height` | m | 2,928 × 3,894,283 | `float32` |
    | `spectral_width` |  | 2,928 × 3,894,283 | `float32` |

??? note "Metadata (6 fields) · 2011–2020"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `float32` |
    | `distance` | `float32` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |

**1979–2010** (32 files)

- Grid points: 3,894,283 &nbsp;·&nbsp; ~455.2 GB per year

??? note "Variable definitions (10) · 1979–2010"

    | Variable | Description | IEC Name | SWAN name | Units |
    |:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Directionality coefficient | $d$ |  |  |
    | `energy_period` | Energy period | $T_{e}$, $T_{-10}$ | TMM10 | s |
    | `maximum_energy_direction` | Direction of maximum directionally resolved wave power (nautical convention) | $\theta_{J}$ |  | degr |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr |
    | `mean_zero-crossing_period` | Mean absolute zero-crossing period | $T_{z}$, $T_{02}$ | TM02 | s |
    | `omni-directional_wave_power` | Omnidirectional wave power | $J$ |  | W/m |
    | `peak_period` | Relative peak period of the variance density spectrum | $T_{p}$ | RTP | s |
    | `significant_wave_height` | Significant wave height | $H_{m0}$ | HSIGN | m |
    | `spectral_width` | Spectral width | $\epsilon_{0}$ |  |  |

??? note "Variable schema (10) · 1979–2010"

    | Variable | Units | Dimensions | Type |
    |:---|:---|:---|:---|
    | `directionality_coefficient` |  | 2,920 × 3,894,283 | `float32` |
    | `energy_period` | s | 2,920 × 3,894,283 | `float32` |
    | `maximum_energy_direction` | degr | 2,920 × 3,894,283 | `float32` |
    | `mean_absolute_period` | s | 2,920 × 3,894,283 | `float32` |
    | `mean_wave_direction` | degr | 2,920 × 3,894,283 | `float32` |
    | `mean_zero-crossing_period` | s | 2,920 × 3,894,283 | `float32` |
    | `omni-directional_wave_power` | W/m | 2,920 × 3,894,283 | `float32` |
    | `peak_period` | s | 2,920 × 3,894,283 | `float32` |
    | `significant_wave_height` | m | 2,920 × 3,894,283 | `float32` |
    | `spectral_width` |  | 2,920 × 3,894,283 | `float32` |

??? note "Metadata (6 fields) · 1979–2010"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `timezone` | `float32` |
    | `distance` | `float32` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |
