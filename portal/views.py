from django.shortcuts import render
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect,Http404,HttpResponse
import json,random
import matplotlib.pyplot as plt
import datacube
from .forms import *
from django.template import RequestContext

# Create your views here.
def Home(request):
	form = dataForm(request.POST or None)		
	if form.is_valid():
		year = request.POST['year']
		layer = request.POST['layer']
		x1 = float(request.POST['x1'])
		x2 = float(request.POST['x2'])
		y1 = float(request.POST['y1'])
		y2 = float(request.POST['y2'])
		imsource = plot(year,layer,x1,x2,y1,y2)
	else:
		imsource = ""
	context = {'imsource':imsource,
					'form':form}
	print context
	return render_to_response("four.html",context,context_instance = RequestContext(request))

def AJAXHandle(request):
	print "in AJAXHandle"
	print request
	if request.is_ajax():
		print request.POST
		print "\n\n\n","HEERRRERRER","\n\n\n"	
		year = request.POST['year']
		layer = request.POST['layer']
		epsg = request.POST['epsg']
		algo = request.POST['prod']
		print "before truncating"
		x1 = float(request.POST['x1'])
		x2 = float(request.POST['x2'])
		y1 = float(request.POST['y1'])
		y2 = float(request.POST['y2'])
		print "before call"
		imsource = plot(year,layer,x1,x2,y1,y2,epsg,algo)
		response = {'status': 1, 'message': imsource + "?t=" + str(random.randint(1,1000))} 
	else:
		response = {'status': 0, 'message': "error"} 
	return HttpResponse(json.dumps(response), content_type='application/json')

def plot(year,layer,x1,x2,y1,y2,epsg,algo):
	print "In Plot"
	print x1,x2,y1,y2
	plt.hold(False)
	##
	dc = datacube.Datacube(config="/home/sharat910/.datacube.conf")
	##
	if algo == "Reflectance":	
		la = dc.load(product='ls5_ledaps_albers', x=(x1, x2), y=(y1,y2))
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
		a = a.loc[str(year)]
		a.plot()
		path = 'media/images/' +  str(year) + '.png'
		plt.savefig(path)
		plt.clf()
		return path

	elif algo == "NDVI":
		import xarray as xr
		from datetime import datetime
		from datacube.api import API
		from datacube.ndexpr import NDexpr
		year = int(year)
		g = API()
		nd = NDexpr()

		satellite = get_sat(year)

		data_request_descriptor = {
    		'platform': satellite,
    		'product': 'ledaps',
    		'variables': ('red', 'nir'),
    		'dimensions': {
        		'x': {
            		'range': (x1,x2)
       			},
        		'y': {
        	    'range': (y1,y2)
       			},
        		'time': {
            		'range': (datetime(year, 1, 1), datetime(year, 12, 31))
        		}
    		}
		}

		# Retrieving data from API
		d1 = g.get_data(data_request_descriptor)

		b30 = d1['arrays']['red']
		b40 = d1['arrays']['nir']

		ndvi = nd.evaluate('((b40 - b30) / (b40 + b30))')

		ndvi.plot()

		path = 'media/images/' +  'ndvi-' + str(year) + '.png'
		plt.savefig(path)
		plt.clf()
		return path
	else:
		return ''



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

