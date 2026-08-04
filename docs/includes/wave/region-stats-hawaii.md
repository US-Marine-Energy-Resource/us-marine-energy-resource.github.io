- **Grid points:** 700,414
- **File size:** ~81.9 GB per year
- **Total archive:** ~2.6 TB
- **Period:** 1979–2010 &nbsp;·&nbsp; 32 annual files
- **Version:** `v1.0.0`

!!! warning "Incomplete archive"
    Files for 2011–2020 are not available on AWS S3 or HSDS.

??? note "Spatiotemporal variables (10)"

    | Variable | Description | IEC name | SWAN name | Units | Dimensions | Type |
    |:---|:---|:---|:---|:---|:---|:---|
    | `directionality_coefficient` | Fraction of total wave energy travelling in the "direction of maximum wave power" direction | d | description: Fraction of total wave energy travelling in the "direction of maximum wave power" direction |  | 2,920 × 700,414 | `float32` |
    | `energy_period` | Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak | T_e | TM02 | s | 2,920 × 700,414 | `float32` |
    | `maximum_energy` | Maximum directionally resolved wave energy | J_sigma_jdmax | jdmax | W/m | 2,920 × 700,414 | `float32` |
    | `maximum_energy_direction` | The direction from which the most wave energy is travelling | Jsigma_Jmax | description: The direction from which the most wave energy is travelling | deg | 2,920 × 700,414 | `float32` |
    | `mean_absolute_period` | Resolved Spectral Moment (m_0/m_1) | T_p | PER | s | 2,920 × 700,414 | `float32` |
    | `mean_wave_direction` | Direction Normal to the Wave Crests | Sigma | DIR | deg | 2,920 × 700,414 | `float32` |
    | `omni-directional_wave_power` | Total wave energy flux from all directions | J | description: Total wave energy flux from all directions | W/m | 2,920 × 700,414 | `float32` |
    | `peak_period` | The period associated with the maximum value of the wave energy spectrum | T_p | RTP | s | 2,920 × 700,414 | `float32` |
    | `significant_wave_height` | Calculated as the zeroth spectral moment (i.e., H_m0) | H_s | HSIGN | m | 2,920 × 700,414 | `float32` |
    | `spectral_width` | Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak | epsilon_o | description: Spectral width characterizes the relative spreading of energy in the wave spectrum. Large values indicate a wider spectral peak |  | 2,920 × 700,414 | `float32` |

??? note "Metadata (6 fields)"

    | Field | Type |
    |:---|:---|
    | `latitude` | `float32` |
    | `longitude` | `float32` |
    | `distance_to_shore` | `float32` |
    | `timezone` | `int16` |
    | `jurisdiction` | `str[7]` |
    | `water_depth` | `float32` |
