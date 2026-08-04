# Data Access

The hindcast data is available through three interfaces depending on your workflow.

## Marine Energy Atlas

The [Marine Energy Atlas][marine-energy-atlas] provides a point-and-click interface for exploring time- and depth-averaged current speed and power density across all five hindcast domains. Use it for initial site screening before downloading time series data.

See the [Atlas guide](../../getting-started/marine-energy-atlas.md) for usage instructions.

## Python Library and CLI

The [`us-marine-energy-resource` Python library][python-library] (which includes the `us-tidal` CLI) can query tidal hindcast data by point, transect, or area, with built-in tools to visualize and analyze the results.

### Install

--8<-- "docs/includes/readme/installation.md"

### Python quick start

```python
import us_marine_energy_resource.tidal_hindcast as tidal

# Fetch the full hindcast time series for the nearest grid point.
# Data is downloaded from S3 and cached locally on first call.
df = tidal.get_data_at_point(lat=60.73, lon=-151.43)

# Plot velocity exceedance curves across all depth layers.
fig, stats = tidal.plot_velocity_exceedance(df)

# Plot the joint probability distribution at a single depth layer.
fig = tidal.generate_tidal_joint_probability(df, sigma_layer=4)
```

### `us-tidal` CLI reference { #us-tidal-cli }

The `us-tidal` command line tool is included with the library install. It supports point, transect, bounding box, and polygon queries without writing Python.

--8<-- "docs/includes/us-tidal-help.md"

#### Point query

--8<-- "docs/includes/readme/cli-point-query.md"

#### Area query

--8<-- "docs/includes/readme/cli-area-query.md"

#### Transect query

--8<-- "docs/includes/readme/cli-transect-query.md"

#### Export options

--8<-- "docs/includes/readme/cli-export-options.md"

### Direct API downloads

--8<-- "docs/includes/readme/direct-downloads.md"

For full documentation see the [library README][python-library].

## Bulk Access (HSDS and AWS S3)

For bulk downloads or programmatic access to the raw parquet files, the data is available via HSDS and AWS S3.

- [HSDS Setup](../../getting-started/hsds-setup.md)
- [AWS S3 Downloads](../../getting-started/aws-s3.md)

Dataset citation: [@mhkdr_tidal_hindcast_submission]

--8<-- "docs/tidal/high-resolution-hindcast/_cite-widget.md"
--8<-- "docs/includes/links.md"
