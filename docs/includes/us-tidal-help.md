```
                                                                                                                        
 Usage: us-tidal [OPTIONS] [LOCATION]                                                                                   
                                                                                                                        
 Query and download modeled tidal current data from the U.S. DOE H2O High Resolution Tidal Hindcast — FVCOM simulations 
 covering five U.S. coastal regions: Cook Inlet AK, Aleutian Islands AK, Salish Sea WA, Piscataqua River NH, and        
 Western Passage ME.                                                                                                    
                                                                                                                        
 A point query returns the mesh face containing the coordinate. Area and transect queries return all faces whose        
 triangles geometrically intersect the specified geometry. Each matched face downloads as a full-year, hourly or        
 half-hourly time series of current speed, direction, and kinetic power density at 10 depth layers (sea surface to      
 seafloor).                                                                                                             
                                                                                                                        
 Dataset citation: https://mhkdr.openei.org/submissions/632                                                             
 Documentation:    https://github.com/US-Marine-Energy-Resource/us-marine-energy-resource-python                        
 AWS S3 browser:   https://data.openei.org/s3_viewer?bucket=marine-energy-data&prefix=us-tidal%2F                       
                                                                                                                        
 Provide exactly one geometry input: a positional lat,lon for                                                           
 a point query, or one of --coord, --bbox, --file,                                                                      
 or --wkt for area queries.                                                                                             
                                                                                                                        
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   location      [LOCATION]  Point as lat,lon (e.g. 60.73,-151.43).                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --coord               -c      TEXT   Transect waypoint as lat,lon. Repeat for multi-segment lines.                   │
│ --bbox                        TEXT   Bounding box as lat_min,lon_min,lat_max,lon_max.                                │
│ --file                -f      PATH   Polygon from a GeoJSON file. Draw one at https://geojson.io/next/.              │
│ --wkt                         TEXT   Polygon as a WKT POLYGON string or path to a .wkt file.                         │
│ --output-dir          -o      PATH   Copy downloaded parquet files to this directory.                                │
│ --csv                                Export downloaded data as CSV files. Written to --output-dir if set, otherwise  │
│                                      to the current directory.                                                       │
│ --dry-run                            Show size estimate without downloading.                                         │
│ --max-size-mb                 FLOAT  Abort if uncached data to download exceeds this limit (MB). 0 = no limit.       │
│                                      [env var: US_TIDAL_MAX_SIZE_MB]                                                 │
│                                      [default: 500.0]                                                                │
│ --max-distance-km             FLOAT  Reject if nearest face is farther than this (km). Point queries only.           │
│ --config                      PATH   Path to config file (default: ~/.us_tidal.toml).                                │
│ --aws-profile                 TEXT   Override AWS profile from config.                                               │
│ --cache-dir                   PATH   Override local cache directory from config.                                     │
│ --use-hpc                            Use HPC local filesystem instead of S3.                                         │
│ --hpc-base-path               TEXT   Override HPC dataset root path from config.                                     │
│ --clear-cache                        Clear the local cache before running.                                           │
│ --install-completion                 Install completion for the current shell.                                       │
│ --show-completion                    Show completion for the current shell, to copy it or customize the              │
│                                      installation.                                                                   │
│ --help                               Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Dataset Info ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --info                           Show dataset metadata, schema, and statistics without downloading. Reads only the   │
│                                  parquet footer (fast range requests).                                               │
│ --info-speed                     Show speed category info only (implies --info).                                     │
│ --info-direction                 Show direction category info only (implies --info).                                 │
│ --info-power                     Show power density category info only (implies --info).                             │
│ --info-depth                     Show depth/water-level category info only (implies --info).                         │
│ --layer                 INTEGER  Sigma layer for --info statistics (0=surface, 9=near-bed). Repeat to select         │
│                                  multiple layers.                                                                    │
│ --depth                 FLOAT    Select the sigma layer nearest to this depth (m from surface) for --info            │
│                                  statistics. Approximate — uses footer depth stats.                                  │
│ --depth-avg                      Average --info statistics across all sigma layers.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                                        
 Examples                                                                                                               
 us-tidal 60.73,-151.43                              Point query                                                        
 us-tidal --coord 60.7,-151.4 --coord 60.9,-151.2   Transect                                                            
 us-tidal --bbox 60.7,-151.5,60.9,-151.2            Bounding box                                                        
 us-tidal --file study_area.geojson                  Polygon from file                                                  
 us-tidal --wkt "POLYGON((-151.5 60.7,...))"         Polygon from WKT                                                   
 us-tidal 60.73,-151.43 --dry-run                    Size estimate                                                      
 us-tidal 60.73,-151.43 --info                       Dataset info (no download)                                         
 us-tidal 60.73,-151.43 --info-speed                 Speed category only                                                
 us-tidal 60.73,-151.43 --info --layer 3             Layer 3 stats                                                      
 us-tidal 60.73,-151.43 --info --depth 15.0          Layer nearest 15 m                                                 
 us-tidal 60.73,-151.43 --info --depth-avg           Average all layers                                                 
 us-tidal --bbox 60.7,-151.5,60.9,-151.2 --info      Aggregate area info                                                
 us-tidal 60.73,-151.43 --output-dir ./data          Save parquet files                                                 
 us-tidal 60.73,-151.43 --csv                        Export CSV to current dir                                          
 us-tidal 60.73,-151.43 --csv --output-dir ./data    Export CSV to ./data                                               
 Config file (~/.us_tidal.toml) sets defaults for AWS, cache, and HPC options.
```
