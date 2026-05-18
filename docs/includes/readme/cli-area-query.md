`--bbox` takes `lat_min,lon_min,lat_max,lon_max`. Use `--dry-run` first;
bbox queries can match thousands of faces.

``` bash
us-tidal --bbox 60.725,-151.445,60.735,-151.425 --dry-run
```

    Matched 103 faces  ·  AK_cook_inlet
                                                                  
      face_id    location             lat          lon   dist_km  
     ──────────────────────────────────────────────────────────── 
      00127584   AK_cook_inlet   60.72406    -151.4444       0.0  
      00126347   AK_cook_inlet   60.73291   -151.43512       0.0  
      00127215   AK_cook_inlet   60.72453   -151.42508       0.0  
      00127216   AK_cook_inlet   60.72458   -151.42688       0.0  
      00127220   AK_cook_inlet   60.72469   -151.43073       0.0  
      00127219   AK_cook_inlet   60.72481   -151.43262       0.0  
      00127383   AK_cook_inlet   60.72487   -151.43976       0.0  
      00127585   AK_cook_inlet    60.7249    -151.4458       0.0  
      00127382   AK_cook_inlet   60.72509   -151.44177       0.0  
      00127380   AK_cook_inlet   60.72521   -151.43649       0.0  
      00127007   AK_cook_inlet   60.72524   -151.42371       0.0  
      00127217   AK_cook_inlet   60.72542   -151.42734       0.0  
      00127381   AK_cook_inlet   60.72544   -151.43842       0.0  
      00127218   AK_cook_inlet   60.72548   -151.42923       0.0  
      00127200   AK_cook_inlet    60.7257   -151.43311       0.0  
      00127201   AK_cook_inlet   60.72588   -151.43506       0.0  
      00127384   AK_cook_inlet    60.7259    -151.4422       0.0  
      00127006   AK_cook_inlet    60.7261   -151.42401       0.0  
      00127387   AK_cook_inlet   60.72612   -151.44556       0.0  
      00127008   AK_cook_inlet   60.72623   -151.42584       0.0  
                                                                  
      … and 83 more
      Files matched           103  
      Total size        ~367.3 MB  
      Already cached       3.6 MB  
      To download       ~363.7 MB

``` bash
