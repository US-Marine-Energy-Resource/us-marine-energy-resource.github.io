- **Period:** 1979–2020 &nbsp;·&nbsp; 42 annual files
- **Total archive:** ~4.4 TB
- **Version:** `v1.0.0`

!!! note "2 model products under one version"
    The `v1.0.0` archive changes grid resolution, variable set and metadata fields at 2011. Read across the break with care.

**2011–2020** (10 files)

- Grid points: 1,696,188 &nbsp;·&nbsp; ~189.7 GB per year

**1979–2010** (32 files)

- Grid points: 700,414 &nbsp;·&nbsp; ~81.9 GB per year

??? note "Spatiotemporal variables (10) · 2011–2020"

    | Variable | Description | IEC name | SWAN name | Units | Dimensions | Type |
    |:---|:---|:---|:---|:---|:---|:---|
    | `depth` | Water depth |  | Depth | m | 2,928 × 1,696,188 | `float32` |
    | `directionality_coefficient` | Directionality coefficient | d |  |  | 2,928 × 1,696,188 | `float32` |
    | `energy_period` | Energy period | T_e,T_-10 | TMM10 | s | 2,928 × 1,696,188 | `float32` |
    | `maximum_energy_direction` | Peak wave direction (nautical convention) |  | PDIR | degr | 2,928 × 1,696,188 | `float32` |
    | `mean_absolute_period` | Mean absolute wave period - equivalent to T_m01 |  | PER | s | 2,928 × 1,696,188 | `float32` |
    | `mean_wave_direction` | Mean wave direction (nautical convention) |  | DIR | degr | 2,928 × 1,696,188 | `float32` |
    | `omni-directional_wave_power` | Omnidirectional wave power | J |  | W/m | 2,928 × 1,696,188 | `float32` |
    | `peak_period` | Relative peak period of the variance density spectrum | T_p | RTP | s | 2,928 × 1,696,188 | `float32` |
    | `significant_wave_height` | Significant wave height | H_m0 | HSIGN | m | 2,928 × 1,696,188 | `float32` |
    | `spectral_width` | Spectral width | epsilon_0 |  |  | 2,928 × 1,696,188 | `float32` |

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

??? note "Spatiotemporal variables (10) · 1979–2010"

    | Variable | Description | IEC name | SWAN name | Units | Dimensions | Type |
    |:---|:---|:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Fraction of total wave energy travelling in the "direction of maximum wave power" direction | d |  |  | 2,920 × 700,414 | `float32` |
    | `energy_period` | Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak | T_e | TM02 | s | 2,920 × 700,414 | `float32` |
    | `maximum_energy` | Maximum directionally resolved wave energy | J_sigma_jdmax | jdmax | W/m | 2,920 × 700,414 | `float32` |
    | `maximum_energy_direction` | The direction from which the most wave energy is travelling | Jsigma_Jmax |  | deg | 2,920 × 700,414 | `float32` |
    | `mean_absolute_period` | Resolved Spectral Moment (m_0/m_1) | T_p | PER | s | 2,920 × 700,414 | `float32` |
    | `mean_wave_direction` | Direction Normal to the Wave Crests | Sigma | DIR | deg | 2,920 × 700,414 | `float32` |
    | `omni-directional_wave_power` | Total wave energy flux from all directions | J |  | W/m | 2,920 × 700,414 | `float32` |
    | `peak_period` | The period associated with the maximum value of the wave energy spectrum | T_p | RTP | s | 2,920 × 700,414 | `float32` |
    | `significant_wave_height` | Calculated as the zeroth spectral moment (i.e., H_m0) | H_s | HSIGN | m | 2,920 × 700,414 | `float32` |
    | `spectral_width` | Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak | epsilon_o |  |  | 2,920 × 700,414 | `float32` |

??? note "Metadata (6 fields) · 1979–2010"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `distance_to_shore` | `float32` |
    | `timezone` | `int16` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |
