- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~4.4 TB
- **Version:** `v1.0.0`

**2011–2020** (10 files)

- Grid points: 1,696,188 &nbsp;·&nbsp; ~189.7 GB per year

??? note "Variable definitions (10) · 2011–2020"

    | Variable | Description | IEC Name | SWAN name | Units |
    |:---|:---|:---|:---|:---|
    | `depth` | Water depth |  | Depth | m |
    | `directionality_coefficient` | Directionality coefficient | $d$ |  |  |
    | `energy_period` | Energy period | $T_{e}$, $T_{-10}$ | TMM10 | s |
    | `maximum_energy_direction` | Peak wave direction (nautical convention) |  | PDIR | degr |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr |
    | `omni-directional_wave_power` | Omnidirectional wave power | $J$ |  | W/m |
    | `peak_period` | Relative peak period of the variance density spectrum | $T_{p}$ | RTP | s |
    | `significant_wave_height` | Significant wave height | $H_{m0}$ | HSIGN | m |
    | `spectral_width` | Spectral width | $\epsilon_{0}$ |  |  |

??? note "Variable schema (10) · 2011–2020"

    | Variable | Units | Dimensions | Type |
    |:---|:---|:---|:---|
    | `depth` | m | 2,928 × 1,696,188 | `float32` |
    | `directionality_coefficient` |  | 2,928 × 1,696,188 | `float32` |
    | `energy_period` | s | 2,928 × 1,696,188 | `float32` |
    | `maximum_energy_direction` | degr | 2,928 × 1,696,188 | `float32` |
    | `mean_absolute_period` | s | 2,928 × 1,696,188 | `float32` |
    | `mean_wave_direction` | degr | 2,928 × 1,696,188 | `float32` |
    | `omni-directional_wave_power` | W/m | 2,928 × 1,696,188 | `float32` |
    | `peak_period` | s | 2,928 × 1,696,188 | `float32` |
    | `significant_wave_height` | m | 2,928 × 1,696,188 | `float32` |
    | `spectral_width` |  | 2,928 × 1,696,188 | `float32` |

??? note "Metadata (7 fields) · 2011–2020"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `depth` | `float32` |
    | `distance_to_shore` | `float32` |
    | `timezone` | `int16` |
    | `eez` | `str[13]` |
    | `jurisdiction` | `str[14]` |

**1979–2010** (32 files)

- Grid points: 700,414 &nbsp;·&nbsp; ~81.9 GB per year

??? note "Variable definitions (10) · 1979–2010"

    | Variable | Description | IEC Name | SWAN name | Units |
    |:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Fraction of total wave energy travelling in the "direction of maximum wave power" direction | $d$ |  |  |
    | `energy_period` | Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak | $T_{e}$ | TM02 | s |
    | `maximum_energy` | Maximum directionally resolved wave energy | $J_{\sigma,jdmax}$ | jdmax | W/m |
    | `maximum_energy_direction` | The direction from which the most wave energy is travelling | $Jsigma_{Jmax}$ |  | deg |
    | `mean_absolute_period` | Resolved Spectral Moment (m_0/m_1) | $T_{p}$ | PER | s |
    | `mean_wave_direction` | Direction Normal to the Wave Crests | $\Sigma$ | DIR | deg |
    | `omni-directional_wave_power` | Total wave energy flux from all directions | $J$ |  | W/m |
    | `peak_period` | The period associated with the maximum value of the wave energy spectrum | $T_{p}$ | RTP | s |
    | `significant_wave_height` | Calculated as the zeroth spectral moment (i.e., H_m0) | $H_{s}$ | HSIGN | m |
    | `spectral_width` | Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak | $\epsilon_{0}$ |  |  |

??? note "Variable schema (10) · 1979–2010"

    | Variable | Units | Dimensions | Type |
    |:---|:---|:---|:---|
    | `directionality_coefficient` |  | 2,920 × 700,414 | `float32` |
    | `energy_period` | s | 2,920 × 700,414 | `float32` |
    | `maximum_energy` | W/m | 2,920 × 700,414 | `float32` |
    | `maximum_energy_direction` | deg | 2,920 × 700,414 | `float32` |
    | `mean_absolute_period` | s | 2,920 × 700,414 | `float32` |
    | `mean_wave_direction` | deg | 2,920 × 700,414 | `float32` |
    | `omni-directional_wave_power` | W/m | 2,920 × 700,414 | `float32` |
    | `peak_period` | s | 2,920 × 700,414 | `float32` |
    | `significant_wave_height` | m | 2,920 × 700,414 | `float32` |
    | `spectral_width` |  | 2,920 × 700,414 | `float32` |

??? note "Metadata (6 fields) · 1979–2010"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `distance_to_shore` | `float32` |
    | `timezone` | `int16` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |
