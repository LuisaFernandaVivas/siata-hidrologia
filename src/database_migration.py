#!/usr/bin/env python
# -*- coding: utf-8 -*-

from meta.models import Basin
import numpy as np
from django.utils import timezone
import datetime
import os

def insert_df(table_name,model):
    data_migration_path = 'staticfiles/'
    import pandas as pd
    df = pd.read_csv(data_migration_path+table_name+'.csv',index_col=0)
    df = df.drop('basin_polygon',axis=1)
    df_all = []
    df['user_id'] = 1
    for index in df.index:
        df_all.append(model(**dict(df.loc[index].dropna())))
    model.objects.bulk_create(df_all)

insert_df('meta_basin',Basin)
