import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class RedRio:
    def __init__(self,codigo = None,**kwargs):
        self.info = pd.Series()
        self.codigo = codigo
        self.info.slug = None
        self.fecha = '2006-06-06 06:06'
        self.workspace = '/media/'
        self.seccion = pd.DataFrame(columns = [u'vertical', u'x', u'y', u'v01', u'v02', u'v03', u'v04',
                                               u'v05', u'v06', u'v07', u'v08', u'v09', u'vsup'])
        self.parametros = "id_aforo,fecha,ancho_superficial,caudal_medio,velocidad_media,perimetro,area_total,profundidad_media,radio_hidraulico"
        self.aforo = pd.Series(index = [u'fecha', u'ancho_superficial', u'caudal_medio',
                                        u'velocidad_media',u'perimetro', u'area_total',
                                        u'profundidad_media', u'radio_hidraulico',u'levantamiento'])
        self.levantamiento = pd.DataFrame(columns = ['vertical','x','y'])
        self.alturas = pd.DataFrame(index=pd.date_range(start = pd.to_datetime('2018').strftime('%Y-%m-%d 06:00'),periods=13,freq='H'),columns = ['profundidad','offset','lamina','caudal'])
        self.alturas.index = map(lambda x:x.strftime('%H:00'),self.alturas.index)

    @property
    def caudales(self):
        pass

    @property
    def folder_path(self):
        return self.workspace+pd.to_datetime(self.fecha).strftime('%Y%m%d')+'/'+self.info.slug+'/'

    def insert_vel(self,vertical,v02,v04,v08):
        self.seccion.loc[vertical,'v02'] = v02
        self.seccion.loc[vertical,'v04'] = v04
        self.seccion.loc[vertical,'v08'] = v08

    def velocidad_media_dovela(self):
        columns = [u'vertical', u'x', u'y', u'v01', u'v02', u'v03',
                   u'v04', u'v05', u'v06', u'v07', u'v08', u'v09', u'vsup']
        dfs = self.seccion[columns].copy()
        self.seccion['vm'] = np.NaN
        vm = []
        for index in dfs.index:
            vm.append(round(self.estima_velocidad_media_vertical(dfs.loc[index].dropna()),3))
        self.seccion['vm'] = vm

    def area_dovela(self):
        self.seccion['area'] = self.get_area(self.seccion['x'].abs().values,self.seccion['y'].abs().values)

    def estima_velocidad_media_vertical(self,vertical,factor=0.0,v_index=0.8):
        vertical = vertical[vertical.index!='vm']
        index = list(vertical.index)
        if index == ['vertical','x','y']:
            if vertical['x'] == 0.0:
                vm = factor * self.seccion.loc[vertical.name+1,'vm']
            else:
                vm = factor * self.seccion.loc[vertical.name-1,'vm']
        elif (index == ['vertical','x','y','vsup']) or (index == ['vertical','x','y','v08']):
            try:
                vm = v_index*vertical['vsup']
            except:
                vm = v_index*vertical['v08']
        elif (index == ['vertical','x','y','v04']) or (index == ['vertical','x','y','v04','vsup']):
            vm = vertical['v04']
        elif (index == ['vertical','x','y','v04','v08']) or (index == ['vertical','x','y','v04','v08','vsup']) or (index == ['vertical','x','y','v02','v04']):
            vm = vertical['v04']
        elif index == ['vertical','x','y','v08','vsup']:
            vm = v_index*vertical['vsup']
        elif (index == ['vertical','x','y','v02','v04','v08']) or (index == ['vertical','x','y','v02','v04','v08','vsup']):
            vm = (2*vertical['v04']+vertical['v08']+vertical['v02'])/4.0
        elif (index == ['vertical','x','y','v02','v08']):
            vm = (vertical['v02']+vertical['v08'])/2.0
        return vm

    def perimetro(self):
        x,y = (self.seccion['x'].values,self.seccion['y'].values)
        def perimeter(x,y):
            p = []
            for i in range(len(x)-1):
                p.append(round(float(np.sqrt(abs(x[i]-x[i+1])**2.0+abs(y[i]-y[i+1])**2.0)),3))
            return [0]+p
        self.seccion['perimetro'] = perimeter(self.seccion['x'].values,self.seccion['y'].values)

    def get_area(self,x,y):
        '''Calcula las áreas y los caudales de cada
        una de las verticales, con el método de mid-section
        Input:
        x = Distancia desde la banca izquierda, type = numpy array
        y = Produndidad
        v = Velocidad en la vertical
        Output:
        area = Área de la subsección
        Q = Caudal de la subsección
        '''
        # cálculo de áreas
        d = np.absolute(np.diff(x))/2.
        b = x[:-1]+d
        area = np.diff(b)*y[1:-1]
        area = np.insert(area, 0, d[0]*y[0])
        area = np.append(area,d[-1]*y[-1])
        area = np.absolute(area)
        # cálculo de caudal
        return np.round(area,3)

    def read_excel_format(self,file):
        df = pd.read_excel(file)
        df = df.loc[df['x'].dropna().index]
        df['vertical'] = range(1,df.index.size+1)
        df['y'] = df['y'].abs()*-1
        df.columns = map(lambda x:x.lower(),df.columns)
        self.seccion = df[self.seccion.columns]
        df = pd.read_excel(file,sheetname=1)
        self.aforo.fecha = df.iloc[1].values[1].strftime('%Y-%m-%d')+df.iloc[2].values[1].strftime(' %H:%M')
        self.aforo['x_sensor'] = df.iloc[4].values[1]
        self.aforo['lamina'] = df.iloc[5].values[1]
        df = pd.read_excel(file,sheetname=2)
        self.levantamiento = df[df.columns[1:]]
        self.levantamiento.columns = ['x','y']
        self.levantamiento.index.name = 'vertical'
        self.aforo.levantamiento = True

    def plot_bars(self,s,filepath=None,bar_fontsize=14,decimales=2,xfactor =1.005,yfactor=1.01,ax=None):
        if ax is None:
            plt.figure(figsize=(20,6))

        s.plot(kind='bar',ax=ax)
        ax.set_ylim(s.min()*0.01,s.max()*1.01)
        for container in ax.containers:
                  plt.setp(container, width=0.8)
        for p in ax.patches:
            ax.annotate(str(round(p.get_height(),decimales)),
                        (p.get_x() * xfactor, p.get_height() * yfactor),
                        fontsize = bar_fontsize)
        for j in ['top','right']:
            ax.spines[j].set_edgecolor('white')
        ax.set_ylabel(r'$Caudal\ [m^3/s]$')
        if filepath:
            plt.savefig(filepath,bbox_inches='tight')

    def plot_levantamientos(self):
        for id_aforo in self.levantamientos:
            self.plot_section(self.get_levantamiento(id_aforo),x_sensor=2,level=0.0)
            plt.title("%s : %s,%s"%(self.info.slug,self.codigo,id_aforo))

    def procesa_aforo(self):
        self.velocidad_media_dovela()
        self.area_dovela()
        self.seccion['caudal'] = np.round(np.array(self.seccion.vm*self.seccion.area),3)
        self.perimetro()
        self.aforo.caudal_medio = round(self.seccion.caudal.sum(),3)
        self.aforo.area_total = round(self.seccion.area.sum(),3)
        self.aforo.velocidad_media = round(self.aforo.caudal_medio/self.aforo.area_total,3)
        self.aforo.ancho_superficial = self.seccion['x'].abs().max()-self.seccion['x'].abs().min()
        self.aforo.perimetro = round(self.seccion.perimetro.sum(),3)
        self.aforo.profundidad_media = round(self.seccion['y'].abs()[self.seccion['y'].abs()>0.0].mean(),3)
        self.aforo.radio_hidraulico = round(self.aforo.area_total/self.aforo.perimetro,3)
        self.fecha = self.aforo.fecha

    def ajusta_levantamiento(self):
        cond = (self.levantamiento['x']<self.aforo.x_sensor).values
        flag = cond[0]
        for i,j in enumerate(cond):
            if j==flag:
                pass
            else:
                point = ((self.levantamiento.iloc[i-1].x,self.levantamiento.iloc[i-1].y),(self.levantamiento.iloc[i].x,self.levantamiento.iloc[i].y))
            flag = j
        point2 = ((self.aforo.x_sensor,0.1*self.levantamiento['y'].min()),((self.aforo.x_sensor,1.1*self.levantamiento['y'].max())))
        intersection = self.line_intersection(point,point2)
        self.levantamiento = self.levantamiento.append(pd.DataFrame(np.matrix(intersection),index=['self.aforo.x_sensor'],columns=['x','y'])).sort_values('x')
        self.levantamiento['y'] = self.levantamiento['y']-intersection[1]
        self.levantamiento['vertical'] = range(1,self.levantamiento.index.size+1)
        self.levantamiento.index = range(0,self.levantamiento.index.size)

    def line_intersection(self,line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect')
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return (x, y)

    def get_sections(self,levantamiento,level):
                hline = ((levantamiento['x'].min()*1.1,level),(levantamiento['x'].max()*1.1,level)) # horizontal line
                lev = pd.DataFrame.copy(levantamiento) #df to modify
                #PROBLEMAS EN LOS BORDES
                borderWarning = 'Warning:\nProblemas de borde en el levantamiento'
                if lev.iloc[0]['y']<level:
                    lev = pd.DataFrame(np.matrix([lev.iloc[0]['x'],level]),columns=['x','y']).append(lev)
                if lev.iloc[-1]['y']<level:
                    lev = lev.append(pd.DataFrame(np.matrix([lev.iloc[-1]['x'],level]),columns=['x','y']))
                condition = (lev['y']>=level).values
                flag = condition[0]
                nlev = []
                intCount = 0
                ids=[]
                for i,j in enumerate(condition):
                    if j==flag:
                        ids.append(i)
                        nlev.append([lev.iloc[i].x,lev.iloc[i].y])
                    else:
                        intCount+=1
                        ids.append('Point %s'%intCount)
                        line = ([lev.iloc[i-1].x,lev.iloc[i-1].y],[lev.iloc[i].x,lev.iloc[i].y]) #  #puntoA
                        inter = self.line_intersection(line,hline)
                        nlev.append(inter)
                        ids.append(i)
                        nlev.append([lev.iloc[i].x,lev.iloc[i].y])
                    flag = j
                df = pd.DataFrame(np.matrix(nlev),columns=['x','y'],index=ids)
                dfs = []
                conteo = (np.arange(1,100,2))
                for i in conteo[:int(intCount/2)]:
                    dfs.append(df.loc['Point %s'%i:'Point %s'%(i+1)])
                return dfs

    def plot_section(self,*args,**kwargs):
            '''Grafica de la seccion transversal de estaciones de nivel
            |  ----------Parametros
            |  df : dataFrame con el levantamiento topo-batimetrico, columns=['x','y']
            |  level : Nivel del agua
            |  riskLevels : Niveles de alerta
            |  *args : argumentos plt.plot()
            |  **kwargs : xSensor,offset,riskLevels,xLabel,yLabel,ax,groundColor,fontsize,figsize,
            |  Nota: todas las unidades en metros'''
            # Kwargs
            level = kwargs.get('level',None)
            xLabel = kwargs.get('xLabel','x [m]')
            yLabel = kwargs.get('yLabel','Profundidad [m]')
            waterColor = kwargs.get('waterColor','#e5efff')
            groundColor = kwargs.get('groundColor','tan')
            fontsize= kwargs.get('fontsize',14)
            figsize = kwargs.get('figsize',(6,2))
            riskLevels = kwargs.get('riskLevels',None)
            xSensor = kwargs.get('xSensor',None)
            offset = kwargs.get('offset',0)
            scatterSize = kwargs.get('scatterSize',0.0)
            ax = kwargs.get('ax',None)
            df = self.levantamiento.copy()
            # main plot
            if ax is None:
                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(111)
            ax.plot(df['x'].values,df['y'].values,color='k',lw=0.5)
            ax.fill_between(np.array(df['x'].values,float),np.array(df['y'].values,float),float(df['y'].min()),color=groundColor,alpha=1.0)
            # waterLevel
            sections = []
            if level is not None:
                for data in self.get_sections(df.copy(),level):
                    #ax.hlines(level,data['x'][0],data['x'][-1],color='k',linewidth=0.5)
                    ax.fill_between(data['x'],level,data['y'],color=waterColor,alpha=0.9)
                    ax.plot(data['x'],[level]*data['x'].size,linestyle='--',alpha=0.3)
                    sections.append(data)
            # Sensor
            if (offset is not None) and (xSensor is not None):
                ax.scatter(xSensor,level,marker='v',color='k',s=30+scatterSize,zorder=22)
                ax.scatter(xSensor,level,color='white',s=120+scatterSize+10,edgecolors='k')
                #ax.annotate('nivel actual',xy=(label,level*1.2),fontsize=8)
                #ax.vlines(xSensor, level,offset,linestyles='--',alpha=0.5,color=self.colores_siata[-1])
            #labels
            ax.set_xlabel(xLabel)
            ax.set_facecolor('white')
            #risks
            xlim_max = df['x'].max()
            if riskLevels is not None:
                x = df['x'].max() -df['x'].min()
                y = df['y'].max() -df['y'].min()
                factorx = 0.05
                ancho = x*factorx
                locx = df['x'].max()+ancho/2.0
                miny = df['y'].min()
                locx = 1.03*locx
                risks = np.diff(np.array(list(riskLevels)+[offset]))
                ax.bar(locx,[riskLevels[0]+abs(miny)],width=ancho,bottom=0,color='green')
                colors = ['yellow','orange','red','red']
                for i,risk in enumerate(risks):
                    ax.bar(locx,[risk],width=ancho,bottom=riskLevels[i],color=colors[i],zorder=19)

                if level is not None:
                    ax.hlines(data['y'].max(),data['x'].max(),locx,lw=1,linestyles='--')
                    ax.scatter([locx],[data['y'].max()],s=30,color='k',zorder=20)
                xlim_max=locx+ancho
    #        ax.hlines(data['y'].max(),df['x'].min(),sections[0].min(),lw=1,linestyles='--')
            ax.set_xlim(df['x'].min(),xlim_max)
            for j in ['top','right','left']:
                ax.spines[j].set_edgecolor('white')
            ax.set_ylabel('y [m]')
    def plot_aforo(self):
        self.seccion['y'] = self.seccion['y'].abs()*(-1.0)
        x = list(self.seccion['x'].values)*4
        y = list(self.seccion['y'].values*(1-0.2))+list(self.seccion['y'].values*(1-0.4))+list(self.seccion['y'].values*(1-0.8))+self.seccion.y.size*[0.0]
        z = list(self.seccion['v02'].values)+list(self.seccion['v04'].values)+list(self.seccion['v08'].values)+list(self.seccion['vsup'].values)
        x+=list(self.seccion['x'].values)
        y+=list(self.seccion['y'].values)
        z+=self.seccion.index.size*[0]

        fig = plt.figure(figsize=(7,3))
        ax = fig.add_subplot(111)
        cm = plt.cm.get_cmap('jet')
        sc = plt.scatter(x,y,c=z,vmin=0.0,vmax=3.0,cmap=cm,s=80,zorder=20)
        cb = plt.colorbar(sc, pad=0.05)
        cb.ax.set_title('V(m/s)')
        ax.plot(self.seccion['x'].values,[0]*self.seccion.index.size,linestyle='--',alpha=0.3)
        ax.fill_between(np.array(self.seccion['x'].values,float),np.array(self.seccion['y'].values,float),float(self.seccion['y'].min()),color='tan',alpha=1.0)
        ax.fill_between(np.array(self.seccion['x'].values,float),np.array(self.seccion['y'].values,float),0,color='#e5efff')
        for j in ['top','right','left']:
            ax.spines[j].set_edgecolor('white')
        ax.set_ylabel('y [m]')
        ax.set_xlabel('x [m]')



from hydraulics.models import *
from meta.models import *
from django.db.models import Q
from django_pandas.io import read_frame
from uploadfiles.models import *
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Hidraulica:
    def __init__(self,item = None,workspace = 'media',**kwargs):
        self.workspace     = workspace
        self.item          = item
        self.section       = pd.DataFrame()
        self.topo          = pd.DataFrame()
        self.estacion      = None
        self.infost        = pd.DataFrame()
        self.info          = pd.Series()
        self.alturas       = pd.DataFrame(index=['06:00','07:00','08:00','09:00','10:00','11:00',
                                                 '12:00','13:00','14:00','15:00','16:00','17:00','18:00'],
                                          columns = ['profundidad','offset','lamina','caudal'])
        self.items         = pd.DataFrame()
        self.topos         = pd.DataFrame()

    def set_from_django(self,item):
        if type(item) == int:
            item = Item.objects.get(id=item)
        self.item     = item
        self.section  = read_frame(Section.objects.filter(fk = self.item.pk)).sort_values('vertical')
        self.topo     = read_frame(Topo.objects.filter(fk = self.item.pk)).sort_values('vertical')
        self.estacion = estaciones.objects.get(id = self.item.item_fk_id)
        self.infost   = read_frame(estaciones.objects.filter(Q(clase='Nivel')| Q(clase='Section'))).set_index('id')
        self.info     = self.infost.loc[self.item.item_fk_id]
        self.items    = read_frame(Item.objects.filter(item_fk_id = self.estacion.id)).id.values


    def plot_section(self,*args,**kwargs):
        if self.topo.empty:
            print("Warning: Empty DataFrame, no data to plot")
        else:
            level = kwargs.get('level',None)
            xLabel = kwargs.get('xLabel','x [m]')
            yLabel = kwargs.get('yLabel','Profundidad [m]')
            waterColor = kwargs.get('waterColor','#e5efff')
            groundColor = kwargs.get('groundColor','tan')
            fontsize= kwargs.get('fontsize',14)
            figsize = kwargs.get('figsize',(6,2))
            riskLevels = kwargs.get('riskLevels',None)
            xSensor = kwargs.get('xSensor',None)
            offset = kwargs.get('offset',0)
            scatterSize = kwargs.get('scatterSize',0.0)
            ax = kwargs.get('ax',None)
            df = self.topo.copy()
            # main plot
            if ax is None:
                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(111)
            ax.plot(df['x'].values,df['y'].values,color='k',lw=0.5)
            ax.fill_between(np.array(df['x'].values,float),np.array(df['y'].values,float),float(df['y'].min()),color=groundColor,alpha=1.0)
            # waterLevel
            sections = []
            if level is not None:
                for data in self.get_sections(df.copy(),level):
                    #ax.hlines(level,data['x'][0],data['x'][-1],color='k',linewidth=0.5)
                    ax.fill_between(data['x'],level,data['y'],color=waterColor,alpha=0.9)
                    ax.plot(data['x'],[level]*data['x'].size,linestyle='--',alpha=0.3)
                    sections.append(data)
            # Sensor
            if (offset is not None) and (xSensor is not None):
                ax.scatter(xSensor,level,marker='v',color='k',s=30+scatterSize,zorder=22)
                ax.scatter(xSensor,level,color='white',s=120+scatterSize+10,edgecolors='k')
                #ax.annotate('nivel actual',xy=(label,level*1.2),fontsize=8)
                #ax.vlines(xSensor, level,offset,linestyles='--',alpha=0.5,color=self.colores_siata[-1])
            #labels
            ax.set_xlabel(xLabel)
            ax.set_facecolor('white')
            #risks
            xlim_max = df['x'].max()
            if riskLevels is not None:
                x = df['x'].max() -df['x'].min()
                y = df['y'].max() -df['y'].min()
                factorx = 0.05
                ancho = x*factorx
                locx = df['x'].max()+ancho/2.0
                miny = df['y'].min()
                locx = 1.03*locx
                risks = np.diff(np.array(list(riskLevels)+[offset]))
                ax.bar(locx,[riskLevels[0]+abs(miny)],width=ancho,bottom=0,color='green')
                colors = ['yellow','orange','red','red']
                for i,risk in enumerate(risks):
                    ax.bar(locx,[risk],width=ancho,bottom=riskLevels[i],color=colors[i],zorder=19)

                if level is not None:
                    ax.hlines(data['y'].max(),data['x'].max(),locx,lw=1,linestyles='--')
                    ax.scatter([locx],[data['y'].max()],s=30,color='k',zorder=20)
                xlim_max=locx+ancho
    #        ax.hlines(data['y'].max(),df['x'].min(),sections[0].min(),lw=1,linestyles='--')
            ax.set_xlim(df['x'].min(),xlim_max)
            for j in ['top','right','left']:
                ax.spines[j].set_edgecolor('white')
            ax.set_ylabel('y [m]')

    def plot_aforo(self):
        self.section['y'] = self.section['y'].abs()*(-1.0)
        x = list(self.section['x'].values)*4
        y = list(self.section['y'].values*(1-0.2))+list(self.section['y'].values*(1-0.4))+list(self.section['y'].values*(1-0.8))+self.section.y.size*[0.0]
        z = list(self.section['v02'].values)+list(self.section['v04'].values)+list(self.section['v08'].values)+list(self.section['vsup'].values)
        x+=list(self.section['x'].values)
        y+=list(self.section['y'].values)
        z+=self.section.index.size*[0]

        fig = plt.figure(figsize=(7,3))
        ax = fig.add_subplot(111)
        cm = plt.cm.get_cmap('jet')
        sc = plt.scatter(x,y,c=z,vmin=0.0,vmax=3.0,cmap=cm,s=80,zorder=20)
        cb = plt.colorbar(sc, pad=0.05)
        cb.ax.set_title('V(m/s)')
        ax.plot(self.section['x'].values,[0]*self.section.index.size,linestyle='--',alpha=0.3)
        ax.fill_between(np.array(self.section['x'].values,float),np.array(self.section['y'].values,float),float(self.section['y'].min()),color='tan',alpha=1.0)
        ax.fill_between(np.array(self.section['x'].values,float),np.array(self.section['y'].values,float),0,color='#e5efff')
        for j in ['top','right','left']:
            ax.spines[j].set_edgecolor('white')
        ax.set_ylabel('y [m]')
        ax.set_xlabel('x [m]')

    def procesa_imagen(self,filepath):
        image = images()
        image.document =filepath
        image.user_id = 1
        image.company = self.item
        print('imagen prcesada en :%s'%filepath)
        image.save()
        return image

    def plot_section_history(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for item in self.items:
            section = read_frame(Section.objects.filter(fk_id = item)).sort_values('vertical')
            if not section.empty:
                if item==self.item.id:
                    color = 'red'
                    alpha = 1
                else:
                    color = 'blue'
                    alpha = 0.3
                try:
                    ax.plot(section['x'].values,section['y'].values,color=color,alpha=alpha)
                except:
                        print('Warning: can not plot %s'%item)
