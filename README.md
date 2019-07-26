# svxdem.py

This tool is intented to be used with the Survex cave mapping software (https://survex.com).

svxdem.py (SURVEX-DEM) creates svx files from raster DEMs exported from GRASS-GIS as ASCII files

like this:  
```r.out.ascii input=topo output=somefile.ascii```

```svxdem.py -i somefile.ascii -o somefile.svx -p UTM22S```



