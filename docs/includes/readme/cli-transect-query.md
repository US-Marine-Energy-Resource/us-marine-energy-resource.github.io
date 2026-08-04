`--coord` defines a waypoint. Repeat it to build a multi-segment path.
All faces whose triangles geometrically intersect the path are returned.

``` bash
mer tidal --coord 60.72,-151.43 --coord 60.75,-151.44 --dry-run
```

    Matched 39 faces  ·  AK_cook_inlet
                                                                  
      face_id    location             lat          lon   dist_km  
     ──────────────────────────────────────────────────────────── 
      00127818   AK_cook_inlet   60.72053   -151.43036       0.0  
      00127621   AK_cook_inlet   60.72163   -151.43011       0.0  
      00127622   AK_cook_inlet   60.72207   -151.43176       0.0  
      00127423   AK_cook_inlet   60.72301   -151.43188       0.0  
      00127422   AK_cook_inlet   60.72375   -151.43024       0.0  
      00127220   AK_cook_inlet   60.72469   -151.43073       0.0  
      00127219   AK_cook_inlet   60.72481   -151.43262       0.0  
      00127200   AK_cook_inlet    60.7257   -151.43311       0.0  
      00127012   AK_cook_inlet   60.72645   -151.43164       0.0  
      00126992   AK_cook_inlet   60.72733   -151.43219       0.0  
      00126807   AK_cook_inlet   60.72812   -151.43073       0.0  
      00126788   AK_cook_inlet   60.72897   -151.43127       0.0  
      00126787   AK_cook_inlet   60.72909   -151.43335       0.0  
      00126764   AK_cook_inlet      60.73   -151.43396       0.0  
      00126581   AK_cook_inlet   60.73064   -151.43268       0.0  
      00126558   AK_cook_inlet   60.73155   -151.43317       0.0  
      00126557   AK_cook_inlet    60.7319   -151.43494       0.0  
      00126345   AK_cook_inlet   60.73349   -151.43335       0.0  
      00126347   AK_cook_inlet   60.73291   -151.43512       0.0  
      00126128   AK_cook_inlet    60.7345   -151.43329       0.0  
                                                                  
      … and 19 more
      Files matched            39  
      Total size        ~139.1 MB  
      Already cached       0.0 MB  
      To download       ~139.1 MB

``` bash
