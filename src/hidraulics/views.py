import numpy as np
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import Item,Section,Topo
from meta.models import Stations
from .forms import *
import locale
from django.urls import reverse_lazy
import matplotlib
matplotlib.use('agg')
import pandas as pd
import matplotlib.pyplot as plt
from uploadfiles.models import UploadImage as images
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django_pandas.io import read_frame
import manager as mg

class Manager(mg.RedRio):
	def __init__(self,item,section_objects,topo_objects,*keys,**kwargs):
		mg.RedRio.__init__(self)
		self.item = item
		self.section_objects = section_objects
		self.topo_objects = topo_objects
		if topo_objects:
			self.levantamiento = read_frame(self.topo_objects).set_index('vertical')[['x','y']]
			self.aforo['x_sensor'] = float(self.item.x_lamina)
		self.topo_filepath = 'document/topo-%s.png'%item
		self.section_filepath = 'document/section-%s.png'%item

	def procesa_imagen(self,filepath):
		image = images()
		image.document =filepath
		image.user_id = 1
		image.company = self.item
		print('imagen prcesada en :%s'%filepath)
		image.save()
		return image

	def plot_topo(self):
		fig = plt.figure(figsize=(5,5))
		ax = fig.add_subplot(211)
		ax2 = fig.add_subplot(212)
		self.plot_section(ax=ax,xLabel=' ')
		try:
			self.ajusta_levantamiento()
			self.plot_section(xSensor = float(self.item.x_lamina),level=float(self.item.y_lamina),ax=ax2)
		except:
			pass
		ax2.set_xlabel(u'Gráfica ajustada x [m]')
		plt.savefig('media/%s'%self.topo_filepath,bbox_inches='tight')

from django.db.models import Q
from django_pandas.io import read_frame
import os, sys
from scipy.optimize import curve_fit

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
        self.sections      = pd.DataFrame()

    def set_from_django(self,Item,Section,Topo,Stations,item):
        if type(item) == int:
            item = Item.objects.get(id=item)
        self.item     = item
        self.section  = read_frame(Section.objects.filter(fk = self.item.pk),verbose=False).sort_values('vertical')
        self.topo     = read_frame(Topo.objects.filter(fk = self.item.pk),verbose=False).sort_values('vertical')
        self.estacion = Stations.objects.get(id = self.item.item_fk_id)
        self.infost   = read_frame(Stations.objects.filter(Q(clase='Nivel')| Q(clase='Section')),verbose=False)
        self.info     = self.infost.set_index('id').loc[self.item.item_fk_id]
        self.items    = read_frame(Item.objects.filter(item_fk_id = self.estacion.id),verbose=False)
        self.topos    = read_frame(Topo.objects.all(),verbose=False)
        self.sections = read_frame(Section.objects.all(),verbose=False)

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

    def plot_aforo(self,ax=None):
        self.section['y'] = self.section['y'].abs()*(-1.0)
        x = list(self.section['x'].values)*4
        y = list(self.section['y'].values*(1-0.2))+list(self.section['y'].values*(1-0.4))+list(self.section['y'].values*(1-0.8))+self.section.y.size*[0.0]
        z = list(self.section['v02'].values)+list(self.section['v04'].values)+list(self.section['v08'].values)+list(self.section['vsup'].values)
        x+=list(self.section['x'].values)
        y+=list(self.section['y'].values)
        z+=self.section.index.size*[0]
        if ax is None:
            fig = plt.figure(figsize=(7,3))
            ax = fig.add_subplot(111)
        cm = plt.cm.get_cmap('jet')
        sc = ax.scatter(x,y,c=z,vmin=0.0,vmax=2.5,cmap=cm,s=80,zorder=20)
        cb = plt.colorbar(sc, ax=ax,pad=0.05)
        cb.ax.set_title('V(m/s)')
        ax.plot(self.section['x'].values,[0]*self.section.index.size,linestyle='--',alpha=0.3)
        ax.fill_between(np.array(self.section['x'].values,float),np.array(self.section['y'].values,float),float(self.section['y'].min()),color='tan',alpha=1.0)
        ax.fill_between(np.array(self.section['x'].values,float),np.array(self.section['y'].values,float),0,color='#e5efff')
        for j in ['top','right','left']:
            ax.spines[j].set_edgecolor('white')
        ax.set_ylabel('y [m]')
        ax.set_xlabel('x [m]')

    def procesa_imagen(self,images,filepath):
        image = images()
        image.document =filepath
        image.user_id = 1
        image.company = self.item
        image.save()
        print('imagen prcesada en :%s'%filepath)
        return image

    @staticmethod
    def get_x_banca(ancho_canal,valor):
        '''
        estimates distance from nearest bank
        Returns
        -------
        nearest bank distance,float
        '''
        if (valor == 0.0) or (ancho_canal==valor): # para evitar problemas de borde
            x_banca = np.NaN
        else:
            if valor > ancho_canal/2.0:
                x_banca = ancho_canal-valor
            else:
                x_banca = valor
        return x_banca

    def plot_diagonal(self,ax,**kwargs):
        '''
        45 grades plot
        Parameters
        ----------
        ax     : matplotlib.axes._subplots.AxesSubplot
        kwargs : plt.plot kwargs
        -------
        '''
        minimum = min(list(ax.get_xlim())+list(ax.get_ylim()))
        maximum = max(list(ax.get_xlim())+list(ax.get_ylim()))
        ax.set_xlim(minimum,maximum)
        line = np.linspace(minimum,maximum,100)
        ax.plot(line,line,**kwargs)

    def default_plot(self,ax=None,verbose=False,*keys,**kwargs):
        '''
        Read SQL query or database table into a DataFrame.
        Parameters
        ----------
        ax : string SQL query or SQLAlchemy Selectable (select or text object)
            to be executed, or database table name.
        fields :
        verbose : print logs

        keys and kwargs = x_label,y_label,xlim,ylim,title,fontsize,grid.
            (default values are None)
        Returns
        -------
        matplotlib.axes._subplots.AxesSubplot
        '''
        if kwargs.get('fontsize'):
            if verbose:
                print('warning matplotlib default fontsize changed')
            plt.rc('font', **{'size'   :kwargs.get('fontsize')})
        if ax:
            pass
        else:
            if kwargs.get('figure'):
                fig = plt.figure(**kwargs.get('figure'))
            else:
                fig = plt.figure()
            ax = fig.add_subplot(111)
        if kwargs.get('xlim'):
            ax.set_xlim(kwargs.get('xlim')[0],kwargs.get('xlim')[1])
        if kwargs.get('ylim'):
            ax.set_ylim(kwargs.get('ylim')[0],kwargs.get('ylim')[1])
        if kwargs.get('x_label'):
            ax.set_xlabel(kwargs.get('x_label'))
        if kwargs.get('y_label'):
            ax.set_ylabel(kwargs.get('y_label'))
        if kwargs.get('title'):
            ax.set_title(kwargs.get('title'))
        if kwargs.get('grid'):
            ax.grid()
        return ax

    def ajuste_curva(self,df,func,x='x',y='y',**kwargs):
        df = df.copy().sort_values(x)
        return curve_fit(func, df[x], df[y],*kwargs)

    def func_exp_1(self,x, a, b,c):
        return a*(x+c)**b

    def func_exp_2(self,x, a, b):
        return (a*pow(x,b))

    @property
    def aforos(self):
        fks = []
        for fk in self.items.id.values:
            if fk in list(set(self.sections.fk.values)):
                fks.append(fk)
        return fks

    @property
    def levantamientos(self):
        fks = []
        for fk in self.items.id.values:
            if fk in list(set(self.topos.fk.values)):
                fks.append(fk)
        return fks

    def scatter(self,df,x='x',y='y',z=None,vmin=None,vmax=None,ax=None,**kwargs):
        '''
        scatter plot personalizada
        Parameters
        ----------
        x : x_axis column name
        y : y_axis column name
        z : column name to be apply colorbar
        -------
        matplotlib.axes._subplots.AxesSubplot
        '''
        ax = self.default_plot(ax=ax,**kwargs)
        if kwargs.get('scatter_keys'):
            if z is None:
                sc = ax.scatter(df[x].values,df[y].values,**kwargs.get('scatter_keys'))
            else:
                sc = ax.scatter(df[x].values,df[y].values,c=df[z].values,**kwargs.get('scatter_keys'))
                title = kwargs.get('cbar_keys').get('title')
                del kwargs['cbar_keys']['title']
                cb = plt.colorbar(sc,**kwargs.get('cbar_keys'))
                cb.ax.set_title(title)
                kwargs['cbar_keys']['title'] = title
        else:
            ax.scatter(df[x].values,df[y].values)
        return ax

    def plot_curva_calibracion(self,df=None,parametro='profundidad_media',ax=None,**kwargs):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        if df is None:
            df = self.items.set_index('id').loc[self.aforos]
        self.scatter(df,parametro,'caudal_total',ax=ax,**kwargs)
        popt, pcov = self.ajuste_curva(df,self.func_exp_1,x=parametro,y='caudal_total')
        ax.plot(df[parametro].sort_values().values,
                self.func_exp_1(df[parametro].sort_values().values, *popt),
                'k-',
                linewidth=2,
                label=(r'$Q\ =\ %s(H+%s)^{%s}$'% (round(popt[0],3),round(popt[2],3),round(popt[1],3))))
        ax.legend(fontsize=12)


    def plot_vm_sup_xbanca(self,ax=None,**kwargs):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        df = self.sections.set_index('fk').loc[self.aforos]
        bad_vsup = []
        bad_vsup+=list(df[df['vm']>5].index)
        bad_vsup+=list(df[df['vsup']>5].index)
        df = df.drop(list(set(bad_vsup)))

        df['ancho_superficial'] = self.items.set_index('id').loc[df.index,'ancho_superficial']
        df['x_banca'] = df.apply(lambda x:self.get_x_banca(x.ancho_superficial,x.x),axis=1)
        self.scatter(df,x='vm',y='vsup',z='x_banca',ax=ax,**kwargs)
        self.plot_diagonal(ax,color='grey',linestyle='--')

    def plot_section_history(self,items_ids,c='blue',ax=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        for item in items_ids:
            try:
                section = self.sections.set_index('fk').loc[item].sort_values('vertical')
            except:
                section = pd.DataFrame()

            if not section.empty:
                if item==self.item.id:
                    color = 'red'
                    alpha = 1
                else:
                    color = c
                    alpha = 0.3
                try:
                    ax.plot(section['x'].values,section['y'].values,color=color,alpha=alpha)
                except:
                        print('Warning: can not plot %s'%item)
        return ax

    def plot_history(self,df):
        fontsize=12
        font = {'size':fontsize}
        plt.rc('font', **font)
        buenos = df[df.calidad==1]
        malos = df[df.calidad!=1]
        if buenos.empty:
            buenos = df.copy()
            malos = pd.DataFrame()
        if len(self.aforos) == 0:
            print('Warning: no data to plot')
        else:
            fig = plt.figure(figsize=(12,14))
            fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.3)
            plt.suptitle(("%s - %s")%(self.info.nombre,self.item.id),y=0.92)
            ax2 = fig.add_subplot(3,2,1)
            ax1 = fig.add_subplot(3,2,2)
            ax3 = fig.add_subplot(3,2,3)
            ax4 = fig.add_subplot(3,2,4)
            ax5 = fig.add_subplot(3,2,5)
            self.plot_section_history(buenos.index,ax=ax1,c='blue')
            self.plot_section_history(malos.index,c='green',ax=ax1)
            try:
                self.plot_aforo(ax=ax2)
            except:
                ax2.set_title('no plot')
            kwargs = {'x_label'     : r'$Profundidad\ [m]$',
                      'y_label'     : r'$Caudal\ [m^3/s]$',
                      'xlim'        : None,
                      'ylim'        : None,
                      'title'       : None,
                      'fontsize'    : 20,
                      'grid'        : True,
                      'scatter_keys': {'vmin'   : 0,
                                       'vmax'   : None,
                                       'cmap'   : None,
                                       's'      : 80,
                                       },
                      'cbar_keys'   : {'pad'   : 0.05,
                                       'title' : 'y',
                                      }
             }
            try:
                self.plot_curva_calibracion(buenos,ax=ax3,**kwargs)
            except:
                ax3.set_title('optimal not founded',fontsize=fontsize)
            try:
                self.plot_curva_calibracion(buenos,ax=ax4,parametro='area_mojada',**kwargs)
            except:
                ax4.set_title('optimal not founded',fontsize=fontsize)

            try:
                if self.item.calidad == 1:
                    color = 'r'
                else:
                    color = 'green'
                ax3.scatter(self.item.profundidad_media,self.item.caudal_total,color=color)
                ax4.scatter(self.item.area_mojada,self.item.caudal_total,color=color)
                ax3.grid()
            except:
                pass
            kwargs = {'x_label'     : 'velocidad_media [m/s]',
                      'y_label'     : 'velocidad_superficial [m/s]',
                      'xlim'        : None,
                      'ylim'        : None,
                      'title'       : None,
                      'fontsize'    : 15,
                      'grid'        : False,
                      'scatter_keys': {'vmin'   : 0,
                                       'vmax'   : None,
                                       'cmap'   : None,
                                       's'      : 50,
                                       },
                      'cbar_keys'   : {'pad'   : 0.05,
                                       'title' : '',
                                      }
                     }

            self.plot_vm_sup_xbanca(ax=ax5,**kwargs)

class ItemListView(ListView):
	def get_queryset(self):
		return Item.objects.all()

class ItemDetailView(DetailView):
	def get_queryset(self):
		return Item.objects.all()

class ItemCreateView(LoginRequiredMixin,CreateView):
	template_name = 'form.html'
	form_class = ItemCreateForm

	def form_valid(self,form):
		obj = form.save(commit = False)
		obj.user = self.request.user
		return super(ItemCreateView,self).form_valid(form)

	def get_queryset(self):
		return Item.objects.all()

	def get_form_kwargs(self):
		self.success_url = reverse_lazy('hidraulics:nueva-vertical',current_app='hydraulics')
		kwargs = super(ItemCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		date = datetime.datetime.now()-datetime.timedelta(hours=5)
		kwargs['initial']={'date':date,'y_factor':0.0}
		return kwargs

	def get_context_data(self,*args,**kwargs):
		context = super(ItemCreateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'Registro'
		return context

class ItemUpdateView(LoginRequiredMixin,UpdateView,Hidraulica):
	template_name = 'hidraulics/item-update.html'
	form_class = ItemUpdateForm

	def get_queryset(self):
		return Item.objects.all()

	def get_context_data(self,*args,**kwargs):
		context = super(ItemUpdateView,self).get_context_data(*args,**kwargs)
		Hidraulica.__init__(self)
		self.set_from_django(Item,Section,Topo,Stations,context['item'])
		# build dependencies
		filepath = 'images/item_history/history-%s.png'%context['item']
		import os
		os.system('mkdir media/images')
		os.system('mkdir media/images/item_history')
		if images.objects.filter(document=filepath):
			pass
		else:
			df = self.items.set_index('id').loc[self.aforos]
			self.plot_history(df)
			plt.savefig('media/'+filepath,bbox_inches='tight')
			self.procesa_imagen(images,filepath)
		objeto = context['item']
		objeto.user = self.request.user
		objeto.save()
		history = False
		for obj in images.objects.filter(company = context['item']):
			if obj.document == filepath:
				context['image'] = obj
				history = True
		if not history:
			print('jueputa home')
		return context

	def get_form_kwargs(self):
		'''Gets the object after submit'''
		kwargs = super(ItemUpdateView,self).get_form_kwargs()
		y_factor = float(self.request.POST.get('y_factor', False))
		instance = kwargs['instance']
		section_objects = Section.objects.filter(fk = instance).order_by('vertical')
		if y_factor !=0.0:
			redrio = mg.RedRio()
			for count,obj in enumerate(section_objects):
				if (obj.y == 0.0) or (obj.y > 10.0):
					pass
				else:
					obj.y = obj.y + float(y_factor)
				redrio.seccion.loc[count] = [int(obj.vertical),obj.x,obj.y,obj.v01,obj.v02,obj.v03,obj.v04,obj.v05,obj.v06,obj.v07,obj.v08, obj.v09,obj.vsup]
				obj.save()

			try:
				redrio.procesa_aforo()
				def convert(id,field):
					import math
					value = redrio.seccion.loc[id,field]
					if math.isnan(value):
						value = None
					return value

				for count,obj in enumerate(section_objects):
					obj.caudal_i = convert(count,'caudal')
					obj.area_i = convert(count,'area')
					obj.perimetro_i = convert(count,'perimetro')
					obj.vm = convert(count,'vm')
					obj.save()

				def convert_item(field):
					import math
					value = redrio.aforo[field]
					if math.isnan(value):
						value = None
					return value

				instance.caudal_total		= convert_item('caudal_medio')
				instance.profundidad_media  = convert_item('profundidad_media')
				instance.perimetro_mojado   = convert_item('perimetro')
				instance.ancho_superficial  = convert_item('ancho_superficial')
				instance.velocidad_promedio = convert_item('velocidad_media')
				instance.radio_hidraulico   = convert_item('radio_hidraulico')
				instance.area_mojada        = convert_item('area_total')
				instance.save()
			except:
				pass

			from pandas import ExcelWriter
			excel_filepath = 'media/document/%s.xlsx'%instance
			writer =  ExcelWriter(excel_filepath)
			redrio.seccion.set_index('vertical').to_excel(writer,'seccion')
			info = pd.Series(index = ['Codigo','Nombre','Fecha','hora inicial','hora final','x_lamina','y_lamina'])
			fecha = datetime.datetime(instance.fecha.year,instance.fecha.month,instance.fecha.day,instance.hora,instance.minuto)
			info['Fecha']  = pd.to_datetime(instance.fecha).strftime('%Y-%m-%d')
			info['hora inicial'] = fecha.strftime('%H:%M')
			info['hora final'] = fecha.strftime('%H:%M')
			info.to_excel(writer,'informacion',header=False)
			workbook  = writer.book
			worksheet = writer.sheets['informacion']
			redrio.levantamiento.to_excel(writer,'levantamiento')
			redrio.alturas.index.name = 'Hora'
			redrio.alturas.fillna('').to_excel(writer,'caudales_horarios')
			workbook  = writer.book
			worksheet = writer.sheets['caudales_horarios']
			#worksheet.set_column('B:B', 15)
			try:
			    redrio.alturas.to_excel(writer,'profundidades_reportadas')
			    redrio.h_horaria.to_excel(writer,'h_horaria')
			    redrio.a_horaria.to_excel(writer,'a_horaria')
			    redrio.q_horaria.to_excel(writer,'q_horaria')
			except:
			    print ('no hourly data')
			    pass
			writer.save()
		kwargs['user'] = self.request.user # obtains the User name that made the changes
		return kwargs

class SectionListView(LoginRequiredMixin,ListView):
	def get_queryset(self):
		return Section.objects.all()

class SectionDetailView(LoginRequiredMixin,DetailView):
	def get_queryset(self):
		return Section.objects.all()

class SectionCreateView(LoginRequiredMixin,CreateView):
	'''Creates form for path /Stations/nuevo/'''
	form_class = SectionForm
	template_name = "form_create_section.html"

	def form_valid(self,form):
		self.success_url = reverse_lazy('hidraulics:nueva-vertical',current_app='hidraulics')
		instance = form.save(commit=False)
		instance.user = self.request.user
		SUPER = super(SectionCreateView,self).form_valid(form)
		return SUPER

	def get_queryset(self):
		return Section.objects.filter(clase='Section')

	def get_context_data(self,*args,**kwargs):
		context = super(SectionCreateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'Crear Dovela'
		context['caudal'] = 'N/A'
		item = Item.objects.filter(user=self.request.user)
		item = item.latest('updated')
		print('item:%s'%item)
		section_objects = Section.objects.filter(fk = item).order_by('vertical')
		manager = Manager(item,section_objects,None)
		try:
			redrio = mg.RedRio()
			for count,obj in enumerate(section_objects):
				redrio.seccion.loc[count] = [int(obj.vertical),obj.x,obj.y,obj.v01,obj.v02,obj.v03,obj.v04,obj.v05,obj.v06,obj.v07,obj.v08, obj.v09,obj.vsup]
			redrio.procesa_aforo()
			def convert(id,field):
				import math
				value = redrio.seccion.loc[id,field]
				if math.isnan(value):
					value = None
				return value

			for count,obj in enumerate(section_objects):
				obj.caudal_i = convert(count,'caudal')
				obj.area_i = convert(count,'area')
				obj.perimetro_i = convert(count,'perimetro')
				obj.vm = convert(count,'vm')
				obj.save()

			def convert_item(field):
				import math
				value = redrio.aforo[field]
				if math.isnan(value):
					value = None
				return value

			item.caudal_total		= convert_item('caudal_medio')
			item.profundidad_media  = convert_item('profundidad_media')
			item.perimetro_mojado   = convert_item('perimetro')
			item.ancho_superficial  = convert_item('ancho_superficial')
			item.velocidad_promedio = convert_item('velocidad_media')
			item.radio_hidraulico   = convert_item('radio_hidraulico')
			item.area_mojada        = convert_item('area_total')
			item.save()
		except:
			pass
		from pandas import ExcelWriter
		excel_filepath = 'media/document/%s.xlsx'%item
		import os
		os.system("mkdir media/document")
		writer =  ExcelWriter(excel_filepath)
		#worksheet.set_column('A:B', 20)
		redrio.seccion.set_index('vertical').to_excel(writer,'seccion')
		info = pd.Series(index = ['Codigo','Nombre','Fecha','hora inicial','hora final','x_lamina','y_lamina'])
		fecha = pd.to_datetime(item.date)
		info['Fecha']  = pd.to_datetime(fecha).strftime('%Y-%m-%d')
		info['hora inicial'] = fecha.strftime('%H:%M')
		info['hora final'] = fecha.strftime('%H:%M')
		info.to_excel(writer,'informacion',header=False)
		workbook  = writer.book
		worksheet = writer.sheets['informacion']
		redrio.levantamiento.to_excel(writer,'levantamiento')
		redrio.alturas.index.name = 'Hora'
		redrio.alturas.fillna('').to_excel(writer,'caudales_horarios')
		workbook  = writer.book
		worksheet = writer.sheets['caudales_horarios']
		#worksheet.set_column('B:B', 15)
		try:
		    redrio.alturas.to_excel(writer,'profundidades_reportadas')
		    redrio.h_horaria.to_excel(writer,'h_horaria')
		    redrio.a_horaria.to_excel(writer,'a_horaria')
		    redrio.q_horaria.to_excel(writer,'q_horaria')
		except:
		    pass
		writer.save()
		# data coordinates and values
		fig = plt.figure(figsize=(6,3))
		redrio.plot_aforo()
		images.objects.filter(document=manager.section_filepath).delete()
		context['image'] = manager.procesa_imagen(manager.section_filepath)
		plt.savefig('media/%s'%manager.section_filepath,bbox_inches='tight')
		context['item'] = item
		context['verticales'] = section_objects
		try:
			context['last_topo'] = Topo.objects.filter(fk = context['object'].fk).latest('updated')
		except:
			context['last_topo'] = None

		#for row in context['form'].fields.values(): print('')
		return context

	def get_form_kwargs(self):
		kwargs = super(SectionCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

class SectionUpdateView(LoginRequiredMixin,UpdateView):
	form_class = SectionUpdateForm
	template_name = "form_section.html"

	def form_valid(self,form):
		self.success_url = reverse_lazy('hidraulics:nueva-vertical',current_app='hidraulics')
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(SectionUpdateView,self).form_valid(form)

	def get_context_data(self,*args,**kwargs):
		context = super(SectionUpdateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'Actualizar dovela: %s | %s'%(self.get_object().fk, self.get_object().fk.fecha)
		section_objects = Section.objects.filter(fk = context['object'].fk).order_by('vertical')
		context['item'] = context['object'].fk
		context['verticales'] = section_objects
		try:
			context['last_topo'] = Topo.objects.filter(fk = context['object'].fk).latest('updated')
		except:
			context['last_topo'] = None
		try:
			context['image'] = images.objects.get(document='document/section-%s.png'%context['object'].fk)
		except:
			manager = Manager(context['object'].fk,section_objects,None)
			#print(read_frame(section_objects))
			manager.seccion = read_frame(section_objects)[manager.seccion.columns]
			print(manager.seccion)
			manager.plot_aforo()
			plt.savefig('media/%s'%manager.section_filepath,bbox_inches='tight')
			context['image'] = manager.procesa_imagen(manager.section_filepath)
		return context

	def get_queryset(self):
		return Section.objects.filter()

def delete_section(request,pk=None):
	instance = get_object_or_404(Section,id=pk)
	instance.delete()
	messages.success(request,"succesfully deleted")
	return redirect("hidraulics:nueva-vertical")

class TopoCreateView(LoginRequiredMixin,CreateView):
	'''Creates View for topo-batimetria'''
	form_class = TopoForm
	template_name = "hidraulics/form_topo.html"

	def form_valid(self,form):
		self.success_url = reverse_lazy('hidraulics:nueva-topo',current_app='hidraulics')
		instance = form.save(commit=False)
		instance.user = self.request.user
		SUPER = super(TopoCreateView,self).form_valid(form)
		return SUPER

	def get_queryset(self):
		return Topo.objects.filter(clase='Section')

	def get_context_data(self,*args,**kwargs):
		context = super(TopoCreateView,self).get_context_data(*args,**kwargs)
		item = Item.objects.filter(user=self.request.user).latest('updated')
		topo_objects = Topo.objects.filter(fk = item).order_by('vertical')
		context['title'] = 'topo-batimetria | %s'%item
		manager = Manager(item,None,topo_objects)
		context['item'] = item
		if len(topo_objects)==0.0:
			context['topo_objects'] = None
			pass
		else:
			images.objects.filter(document=manager.topo_filepath).delete()
			manager.plot_topo()
			context['image'] = manager.procesa_imagen(manager.topo_filepath)
			context['topo_objects'] = topo_objects
		try:
			context['last_section'] = Section.objects.filter(fk = item).latest('updated')
		except:
			context['last_section'] = None
		return context

	def get_form_kwargs(self):
		kwargs = super(TopoCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


class TopoUpdateView(LoginRequiredMixin,UpdateView):
	form_class = TopoUpdateForm
	template_name = "hidraulics/form_topo.html"

	def form_valid(self,form):
		self.success_url = reverse_lazy('hidraulics:nueva-topo',current_app='hidraulics')
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(TopoUpdateView,self).form_valid(form)

	def get_context_data(self,*args,**kwargs):
		context = super(TopoUpdateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'Actualizar topo-batimetria: %s'%context['object'].fk
		context['item'] = context['object'].fk
		topo_objects = Topo.objects.filter(fk = context['object'].fk).order_by('vertical')
		if topo_objects:
			try:
				context['image'] = images.objects.get(document='document/topo-%s.png'%context['object'].fk)
			except:
				manager = Manager(context['object'].fk,None,topo_objects)
				images.objects.filter(document=manager.topo_filepath).delete()
				manager.plot_topo()
				context['image'] = manager.procesa_imagen(manager.topo_filepath)
		context['topo_objects'] = topo_objects
		try:
			context['last_section'] = Section.objects.filter(fk = context['object'].fk).latest('updated')
		except:
			context['last_section'] = None
		return context


	def get_queryset(self):
		return Topo.objects.filter()


def delete_topo(request,pk=None):
	instance = get_object_or_404(Topo,id=pk)
	instance.delete()
	messages.success(request,"succesfully deleted")
	return redirect("hidraulics:nueva-topo")


def transfer_to_topo(request,pk=None):
	instance = get_object_or_404(Item,id=pk)
	topo_objects = Topo.objects.filter(fk = instance).delete()
	section_objects = Section.objects.filter(fk = instance).order_by('vertical')
	for obj in section_objects:
		topo_object = Topo()
		topo_object.fk = obj.fk
		topo_object.x = obj.x
		topo_object.y = obj.y
		topo_object.vertical = obj.vertical
		topo_object.user_id = 1
		topo_object.save()
	messages.success(request,"succesfully transfered")
	return redirect("hidraulics:nueva-topo")

from django.http import JsonResponse
