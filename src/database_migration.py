#!/usr/bin/env python
# -*- coding: utf-8 -*-

from meta.models import *
from hydraulics.models import *
import numpy as np
from django.utils import timezone
import datetime
import os

def insert_df(table_name,model):
    data_migration_path = 'staticfiles/'
    import pandas as pd
    df = pd.read_csv(data_migration_path+table_name+'.csv',index_col=0, encoding = "ISO-8859-1")
    try:
        df['date'] = df['date'].strftime("%Y-%m-%d %H:%M:00")
    except:
        pass

    try:
        df = df.drop('basin_polygon',axis=1)
    except:
        pass
    df_all = []
    df['user_id'] = 1
    print(df.head())
    for index in df.index:
        df_all.append(model(**dict(df.loc[index].dropna())))
    model.objects.bulk_create(df_all)

insert_df('meta_basin',Basin)
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

insert_df('meta_stations',Stations)
insert_df('hydraulics_item',Item)
insert_df('hydraulics_section',Section)
insert_df('hydraulics_topo',Topo)
