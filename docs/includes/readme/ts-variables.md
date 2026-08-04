The [full variable
reference](../../tidal/high-resolution-hindcast/variables.md)
documents every field in the dataset. The table and metadata below are
generated directly from the parquet schema of the downloaded file.

Column names prefixed with `vap_` are **Value Added Products**:
quantities derived from the raw model output (e.g. speed computed from
u/v components, power density from speed). Pass `return_metadata=True`
to `get_data_at_point` to receive CF-convention variable and file-level
metadata alongside the DataFrame.

Layered variables span all 10 sigma layers (layer 0 = sea surface, layer
9 = near-seafloor) and are collapsed to a single row.

| Variable | Label | Units |
|:---|:---|:---|
| vap_sea_water_speed_layer\_(0–9) | Sea Water Speed | m s-1 |
| vap_water_column_max_sea_water_speed | Depth maximum Sea Water Speed | m s-1 |
| vap_water_column_mean_sea_water_speed | Depth averaged Sea Water Speed | m s-1 |
| vap_sea_water_power_density_layer\_(0–9) | Sea Water Power Density | W m-2 |
| vap_water_column_max_sea_water_power_density | Depth maximum Sea Water Power Density | W m-2 |
| vap_water_column_mean_sea_water_power_density | Depth averaged Sea Water Power Density | W m-2 |
| vap_sea_water_to_direction_layer\_(0–9) | Sea Water Velocity To Direction | degree |
| vap_water_column_mean_sea_water_to_direction | Depth averaged Sea Water Velocity To Direction | degree |
| vap_surface_elevation | Sea Surface Elevation Relative to Mean Sea Level | m |
| u_layer\_(0–9) | Eastward Water Velocity | m s-1 |
| v_layer\_(0–9) | Northward Water Velocity | m s-1 |
| vap_sigma_depth_layer\_(0–9) | Depth Below Sea Surface at Sigma Levels | m |
| element_corner_1_lat | Nodal Latitude | degrees_north |
| element_corner_1_lon | Nodal Longitude | degrees_east |
| element_corner_2_lat | Nodal Latitude | degrees_north |
| element_corner_2_lon | Nodal Longitude | degrees_east |
| element_corner_3_lat | Nodal Latitude | degrees_north |
| element_corner_3_lon | Nodal Longitude | degrees_east |
| vap_sea_floor_depth | Water Depth from Sea Surface to Seafloor | m |
| vap_water_column_mean_u | Depth averaged Eastward Water Velocity | m s-1 |
| vap_water_column_mean_v | Depth averaged Northward Water Velocity | m s-1 |
| vap_zeta_center | Sea Surface Height at Cell Centers from NAVD88 | m from NAVD88 |

### Variable Metadata

Each column carries full CF-convention metadata accessible via
`return_metadata=True`. Here is the complete attribute set for
`vap_sea_water_power_density_layer_0` as an example:

``` python
_, file_meta, var_meta = tidal.get_data_at_point(lat=lat, lon=lon, return_metadata=True)

pd.DataFrame(var_meta["vap_sea_water_power_density_layer_0"].items(), columns=["Attribute", "Value"])
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | Attribute | Value |
|----|----|----|
| 0 | long_name | Sea Water Power Density |
| 1 | units | W m-2 |
| 2 | grid | fvcom_grid |
| 3 | type | data |
| 4 | mesh | fvcom_mesh |
| 5 | location | face |
| 6 | coverage_content_type | modelResult |
| 7 | additional_processing | Computed using the fluid power density equatio... |
| 8 | computation | sea_water_power_density = 0.5 \* rho \* sea_wate... |
| 9 | input_variables | sea_water_speed (m/s), rho=\`1025.0\` (kg/m³) |
| 10 | citation | Haas, Kevin A., et al. 'Assessment of Energy P... |

</div>

### Dataset Metadata

Each parquet file in this dataset also contains metadata that describes
the dataset:

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | Attribute | Value |
|----|----|----|
| 0 | WPTO_HINDCAST_FORMAT_VERSION | 1.0 |
| 1 | WPTO_HINDCAST_METADATA_TYPE | netcdf_compatible |
| 2 | Conventions | CF-1.10, ACDD-1.3, ME Data Pipeline-1.0 |
| 3 | acknowledgement | This work was funded by the U.S. Department of... |
| 4 | code_url | https://github.com/NREL/Marine_Energy_Resource... |
| 5 | code_version | 1.0.0 |
| 6 | creator_country | USA |
| 7 | creator_email | zhaoqing.yang@pnnl.gov |
| 8 | creator_institution | Pacific Northwest National Laboratory (PNNL) |
| 9 | creator_institution_url | https://www.pnnl.gov/ |
| 10 | creator_name | Zhaoqing Yang |
| 11 | creator_sector | gov_federal |
| 12 | creator_state | Washington |
| 13 | creator_type | institution |
| 14 | creator_url | https://www.pnnl.gov/projects/ocean-dynamics-m... |
| 15 | contributor_name | Mithun Deb, Preston Spicer, Taiping Wang, Levi... |
| 16 | contributor_role | author, author, author, author, author, proces... |
| 17 | contributor_role_vocabulary | https://vocab.nerc.ac.uk/collection/G04/current/ |
| 18 | contributor_url | https://www.pnnl.gov, www.nrel.gov |
| 19 | data_level | b1 |
| 20 | dataset_name | wpto_high_res_tidal.ak_cook_inlet.v1.0.0 |
| 21 | datastream | wpto_high_res_tidal.ak_cook_inlet.b1.v1.0.0 |
| 22 | description | High-resolution tidal energy resource hindcas... |
| 23 | featureType | timeSeries |
| 24 | geospatial_lat_units | degrees_north |
| 25 | geospatial_lon_units | degrees_east |
| 26 | geospatial_vertical_origin | geoid |
| 27 | geospatial_vertical_positive | down |
| 28 | geospatial_vertical_units | m |
| 29 | history | Ran by asimms on x1003c2s1b1n1 (OS: Linux, Ker... |
| 30 | id | AK_cook_inlet.wpto_high_res_tidal.v1.0.0 |
| 31 | infoURL | https://www.github.com/nrel/marine_energy_reso... |
| 32 | inputs | \['/kfs2/projects/hindcastra/Tidal/datasets/hig... |
| 33 | keywords | OCEAN TIDES, TIDAL ENERGY, VELOCITY, SPEED, DI... |
| 34 | license | Freely Distributed |
| 35 | naming_authority | gov.nrel.water_power |
| 36 | references | Deb, Mithun, Zhaoqing Yang, and Taiping Wang. ... |
| 37 | temporal | hourly |
| 38 | date_created | 2023-02-07T20:23:00 |
| 39 | date_issued | 2025-11-12 |
| 40 | date_metadata_modified | 2025-11-20T19:46:18.682654+00:00 |
| 41 | date_modified | 2025-11-20T19:46:18.682654+00:00 |
| 42 | processing_level | b1 |
| 43 | product_version | 1.0.0 |
| 44 | program | U.S. Department of Energy (DOE) Office of Ener... |
| 45 | project | High Resolution Tidal Hindcast |
| 46 | summary | High-resolution tidal energy resource hindcas... |
| 47 | publisher_country | USA |
| 48 | publisher_email | michael.lawson@nrel.gov |
| 49 | publisher_institution | National Renewable Energy Laboratory (NREL) |
| 50 | publisher_name | Michael Lawson |
| 51 | publisher_state | Colorado |
| 52 | publisher_type | institution |
| 53 | publisher_url | https://www.nrel.gov |
| 54 | source | FVCOM_4.3.1 |
| 55 | title | High Resolution Tidal Hindcast for Cook Inlet,... |

</div>
