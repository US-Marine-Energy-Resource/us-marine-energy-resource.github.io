# Time Series Variables

Each grid point in the High Resolution Tidal Hindcast stores a one-year
hourly (Alaska) or half-hourly (contiguous U.S.) time series in a parquet
file. The table below describes every column in that file. These are the
variables returned by [`get_data_at_point`](data-access.md) and the
`us-tidal` CLI.

For the single-value summary variables shown in the Atlas (annual mean
speed, 95th percentile, etc.), see
[Atlas Variables](variables.md).

--8<-- "docs/includes/readme/ts-variables.md"

--8<-- "docs/tidal/high-resolution-hindcast/_cite-widget.md"
