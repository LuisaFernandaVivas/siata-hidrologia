from meta.models import Basin
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
import ast

print('working')

estaciones = Basin.objects.filter()
bad = []
estacion = estaciones[0]
for estacion in estaciones:
    try:
        codigo = estacion.codigo
        polygon_path = 'staticfiles/polygon/%s/%s.shp'%(codigo,codigo)
        ds = DataSource(polygon_path)
        layer = ds[0]
        geojson = ast.literal_eval(layer[0].geom.json)
        estacion.basin_polygon = str(geojson)
        estacion.save()
    except:
        bad.append(estacion.codigo)

print(bad)
