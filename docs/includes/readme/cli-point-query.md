`us-tidal` accepts a positional `lat,lon` argument. Start with
`--dry-run` to check the size before committing to a download.

``` bash
us-tidal 60.73,-151.43 --dry-run
```

    face_id    00126601                                                            
     location   AK_cook_inlet                                                       
     latitude   60.7298317                                                          
     longitude  -151.4297485                                                        
     distance   0.00 km (containing cell)                                           
     file       AK_cook_inlet/v1.0.0/b1_vap_by_point_partition/lat_deg=60/lon_deg=… 
     s3         s3://marine-energy-data/us-tidal/AK_cook_inlet/v1.0.0/b1_vap_by_po… 
     url        https://marine-energy-data.s3.us-west-2.amazonaws.com/us-tidal/AK_… 
      Files matched          1  
      Total size        3.6 MB  
      Already cached    3.6 MB  
      To download       0.0 MB

On first run the file is fetched from S3. Subsequent calls read from the
local cache with no network traffic.

``` bash
