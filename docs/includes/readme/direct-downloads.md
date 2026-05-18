Tidal hindcast data is accessible via multiple functions that can be
used independently of the plotting functions. This allows users to
access the underlying data at specific points, along lines, or within
rectangular areas. This downloads data to a local cache directory and
returns the path to the downloaded files, which can be loaded and
analyzed with the `load_parquet` and `prepare_dataframe` functions in
the `analysis` module.

`tidal._state` is initialized lazily on the first `get_data_at_point()`
call; call that once to populate the shared cache and manifest before
accessing `_state` directly.

``` python
from us_marine_energy_resource import tidal_hindcast as tidal
from us_marine_energy_resource.analysis import load_parquet, prepare_dataframe
