# Geospatial

FEO utilises a wide variety of geospatial data and allows users to explore thematic data `Collection`s. A `Collection` can be either a vector collection or a raster collection.

## Vector Collections

Vector collections are thematic groups of `Features`, each with a set of attributes and a corresponding `Geometry`. The geometry represents the real-world location of the data as either a point, line, or polygon.

FEO Vector collections include:

- Administrative and Node geometries: the area the node represents.
- Exclusive Economic Zones (EEZ): offshore regions by country.
- Hydrobasins: watershed boundaries and sub-basin delineations.
- Protected areas: marine and terrestrial areas of conservation.
- More to come ...


## Raster Data

Raster collections are thematic groups of `Rasters`. Raster data represent geographic data as a matrix of cells, each with a value corresponding to a certain attribute . For example the attribute could be the amount of precipitation observed at the cell location. The value can also represent a category e.g., in land cover raster datasets the cell value will correspond to a label such as urban area, forests, etc. The size of each cell, in real-world units, is known and the `resolution`. This varies widely across datasets.

FEO Raster collections include:

- Copernicus Global Land Cover: satellite-derived global land cover classification at 100m resolution
- More to come ...

## Examples

To access a wide variety of geospatial data you can use this [Jupyter Notebook on Github](https://github.com/transition-zero/feo-client-examples/blob/main/feo-client-examples/4_geospatial_data.ipynb).
