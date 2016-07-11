from django.shortcuts import render
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect,Http404,HttpResponse
import json,random
from .forms import *
from django.template import RequestContext

#Datacube Imports
import matplotlib.pyplot as plt
import datacube
import pyproj

#Imports for RVI algo
import numpy
from datetime import datetime
from datacube.analytics.analytics_engine import AnalyticsEngine
from datacube.execution.execution_engine import ExecutionEngine
from datacube.analytics.utils.analytics_utils import plot

#Imports for NDVI algo
import xarray as xr
from datacube.api import API
from datacube.ndexpr import NDexpr

#*******************************************************
from django.views.decorators.csrf import csrf_exempt
#*******************************************************

# Create your views here.
@csrf_exempt
def Home(request):
	form = dataForm(request.POST or None)
	imsource = ''
	context = {'imsource':imsource,
				'form':form}
	return render_to_response("five.html",context,context_instance = RequestContext(request))

@csrf_exempt
def AJAXHandle(request):	
	if request.is_ajax():		
		year = int(request.POST['year'])
		layer = request.POST['layer']
		epsg = request.POST['epsg']
		prod = request.POST['prod']
		algo = request.POST['algo']		
		x1 = float(request.POST['x1'])
		x2 = float(request.POST['x2'])
		y1 = float(request.POST['y1'])
		y2 = float(request.POST['y2'])		
		utm44 = pyproj.Proj("+init=EPSG:32644")
		gcs = pyproj.Proj("+init=EPSG:4326")
		x1, y1 = pyproj.transform(gcs, utm44, x1, y1)
		x2, y2 = pyproj.transform(gcs, utm44, x2, y2)
		print x1, x2, y1, y2

		imsource = plot(year,layer,x1,x2,y1,y2,epsg,prod,algo)
		response = {'status': 1, 'message': imsource + "?t=" + str(random.randint(1,1000))} 
	else:
		response = {'status': 0, 'message': "error"} 
	return HttpResponse(json.dumps(response), content_type='application/json')

def plot(year,layer,x1,x2,y1,y2,epsg,prod,algo):	
	if prod == "Reflectance":		
		if algo == "None":	
			return Reflectance(x1,x2,y1,y2,year,layer)
		#elif algo == "NDVI":			
		#	return NDVI(x1,x2,y1,y2,year)
		elif algo == 'RVI' or algo == 'TVI' or algo == 'NDVI':
			return algos(x1,x2,y1,y2,year,algo)
		else:
			return ''
	elif prod == "NDVI":
		return NDVI(x1, x2, y1, y2, year)
	elif prod == "LST":
		return LST(x1, x2, y1, y2, year)


def Reflectance(x1, x2, y1, y2, year,layer):
	dc = datacube.Datacube(config="/home/sharat910/.datacube.conf")
	la = dc.load(product=get_product(year), x=(x1, x2), y=(y1,y2))
	print la
	if layer == "1":
		a = la.blue
		a = a.where(a != a.attrs['nodata'])
	elif layer == "2":
		a = la.green
		a = a.where(a != a.attrs['nodata'])		
	elif layer == "3":
		a = la.red
		a = a.where(a != a.attrs['nodata'])
	elif layer == "4":
		a = la.nir
		a = a.where(a != a.attrs['nodata'])
	print str(year)
	a = a.where(a<1)
	a = a.loc[str(year)]
	a[0].plot()
	path = 'media/images/' +  str(year) + '.png'
	plt.savefig(path)
	plt.clf()
	return path

def NDVI(x1, x2, y1, y2, year):	
	dc = datacube.Datacube(config="/home/rishabh/.datacube.conf")
	la = dc.load(product='Output_NDVI', x = (x1, x2),y = (y1, y2))
	a = la.NDVI.loc[str(year)]
	a = a.where(a != a.attrs['nodata'])
	a = a.where(a < 1)
	a = a.where(a > -1)
	a[0].plot()
	path = 'media/images/' + 'prod-ndvi' + str(year) + '.png'
	plt.savefig(path)
	plt.clf()
	return path

def LST(x1, x2, y1, y2, year):
	dc = datacube.Datacube(config="/home/rishabh/.datacube.conf")
	la = dc.load(product='Output_LST', x = (x1, x2),y = (y1, y2))
	a = la.LST.loc[str(year)]
	a = a.where(a != a.attrs['nodata'])
	a = a.where(a > 220)
	a[0].plot()
	path = 'media/images/' + 'prod-lst' + str(year) + '.png'
	plt.savefig(path)
	plt.clf()
	return path

def algos (x1, x2, y1, y2, year,algo):
	dc = datacube.Datacube(config="/home/rishabh/.datacube.conf")	
	
	a = AnalyticsEngine()	
	e = ExecutionEngine()

	product = get_product(year)
	#assert product
	#dc.list_products() is pandas dataframe, .loc[:]['name'] selects
	#   the products is a pandas series. values is array
	assert (product in dc.list_products().loc[:]['name'].values), "Product not in database"

	# 2 index for platform, 3 for product type
	for prod  in dc.list_products().loc[:].values:
	    if(product == prod[0]):
	        platform = prod[2]
	        product_type = prod[3]

	
	# assert time
	la = dc.load(product=product, x = (x1, x2),y = (y1, y2))
	# this is date of product (la.items()[0])[1].values[0]
	date_of_prod = (la.items()[0])[1].values[0]
	#this is numpy.datetime64

	# TO DO COMPARE numpy.datetime64 with datetime.datetime    
	#assert (date_of_prod >= time1 and date_of_prod <= time2), "Product not in the provided time"

	time1 = datetime(year, 1, 1)
	time2 = datetime(year, 12, 31)
	# calculate output
	dimensions = {'x':    {'range': (x1, x2)},
	              'y':    {'range': (y1, y2)},
	              'time': {'range': (time1, time2)}}

	# create arrays
	b40 = a.create_array((platform, product_type), ['nir'], dimensions, 'b40')
	b30 = a.create_array((platform, product_type), ['red'], dimensions, 'b30')

	if algo == 'RVI':
		#ratio vegetation index
		rvi = a.apply_expression([b40, b30], '(array1 / array2)', 'rvi')

		e.execute_plan(a.plan)

		#result x array
		res = e.cache['rvi']['array_result']['rvi']
		res[0].plot()
		path = 'media/images/' +  'rvi-' + str(year) + '.png'
	elif algo == 'NDVI':
		ndvi = a.apply_expression([b40, b30], '((array1 - array2) / (array1 + array2))', 'ndvi')

		e.execute_plan(a.plan)

		#result x array
		res = e.cache['ndvi']['array_result']['ndvi']
		res[0].plot()
		path = 'media/images/' +  'ndvi-' + str(year) + '.png'

	elif algo == 'TVI':
		#Transformed Vegetation Index
		tvi = a.apply_expression([b40, b30], '(sqrt(((array1 - array2) / (array1 + array2)) + 0.5) * 100)', 'tvi')

		e.execute_plan(a.plan)

		#result x array
		res = e.cache['tvi']['array_result']['tvi']
		res[0].plot()
		path = 'media/images/' +  'tvi-' + str(year) + '.png'
	else:
		pass 	
	plt.savefig(path)
	plt.clf()
	return path

def reductionTime(start_year,end_year,operation):
	from datetime import datetime
	from datacube.analytics.analytics_engine import AnalyticsEngine
	from datacube.execution.execution_engine import ExecutionEngine
	from datacube.analytics.utils.analytics_utils import plot

	a = AnalyticsEngine()
	e = ExecutionEngine()

	dimensions = {'x':    {'range': (x1, x2)},
	              'y':    {'range': (y1, y2)},
	              'time': {'range': (datetime(start_year, 1, 1), datetime(end_year, 12, 31))}}

	arrays = a.create_array(('LANDSAT_5', 'ledaps'), ['nir'], dimensions, 'get_data')

	median = a.apply_expression(arrays, operation +'(array1, 0)', 'medianT')

def get_product(year):	
	if year<=1995 or year == 2010:
		product = 'ls5_ledaps_albers'
	elif year<=2003:
		product = 'ls7_ledaps_albers'
	elif year == 2015:
		product = 'ls8_ledaps_albers'
	return product

def get_sat(year):
	if year<=1995 or year == 2010:
		satellite = 'LANDSAT_5'
	elif year<=2003:
		satellite = 'LANDSAT_7'
	elif year == 2015:
		satellite = 'LANDSAT_8'
	return satellite

def CodeView(request):
	form = CodeForm2(request.POST or None)
	context = {'form':form}
	return render_to_response("code.html",context,context_instance = RequestContext(request))

