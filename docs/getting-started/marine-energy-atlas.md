# Marine Energy Atlas

The [NLR Marine Energy Atlas](https://maps.nlr.gov/marine-energy-atlas) is an interactive web application for exploring marine energy resource data across the United States.

## What Is the Atlas?

The Marine Energy Atlas provides a visual interface for browsing summary statistics from the wave and tidal hindcast datasets. Users can explore spatial patterns, compare locations, and download point data without writing code.

## Browse Data

1. Navigate to [maps.nlr.gov/marine-energy-atlas](https://maps.nlr.gov/marine-energy-atlas)
2. Select a dataset layer (e.g., "Tidal Mean Current Speed")
3. Use the map controls to zoom to your area of interest
4. Color-coded grid cells show variable magnitudes across the domain

## Query Point Data

The atlas includes a point query tool for extracting data at specific locations:

1. Select the point query tool from the toolbar
2. Click on a grid cell of interest
3. View summary statistics for that location
4. Download the data as CSV

## How Our Datasets Appear on the Atlas

The Marine Energy Atlas displays summary-level data (processing level `b5_vap_atlas_summary_parquet`) derived from the full hindcast datasets. These summaries include:

- Significant wave height, wave power, and period statistics (wave)
- Mean and 95th percentile current speed and power density (tidal)
- Water depth, tidal range, and grid resolution (tidal)

For full time-series data, use [HSDS](hsds-setup.md) or [AWS S3](aws-s3.md) to access the complete datasets.

## Relationship to This Documentation

The atlas provides **visual exploration** - this documentation provides **technical detail**. Together they serve different stages of the user journey:

| Need | Where to Go |
| ---- | ----------- |
| "Where is the tidal resource strongest?" | [Marine Energy Atlas](https://maps.nlr.gov/marine-energy-atlas) |
| "What variables are available?" | [Wave Variables](../wave/hindcast/variables.md) or [Tidal Variables](../tidal/high-resolution-hindcast/variables.md) |
| "How was this data produced?" | [Tidal Methodology](../tidal/high-resolution-hindcast/methodology.md) |
| "I need the full time series" | [HSDS Setup](hsds-setup.md) or [AWS S3](aws-s3.md) |
