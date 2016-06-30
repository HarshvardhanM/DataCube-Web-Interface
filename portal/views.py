from django.shortcuts import render
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect,Http404,HttpResponse
import json
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
	return render_to_response("one.html",context,context_instance = RequestContext(request))

def AJAXHandle(request):
	print "in AJAXHandle"
	print request
	if request.is_ajax():
		print request.POST
		print "\n\n\n","HEERRRERRER","\n\n\n"
		year = request.POST['year']
		layer = request.POST['layer']
		x1 = float(request.POST['x1'])
		x2 = float(request.POST['x2'])
		y1 = float(request.POST['y1'])
		y2 = float(request.POST['y2'])
		imsource = plot(year,layer,x1,x2,y1,y2)
		response = {'status': 1, 'message': imsource} 
	else:
		response = {'status': 0, 'message': "error"} 
	return HttpResponse(json.dumps(response), content_type='application/json')

def plot(year,layer,x1,x2,y1,y2):
	plt.hold(False)
	##
	dc = datacube.Datacube(config="/home/sharat910/.datacube.conf")
	##
	la = dc.load(product='ls5_ledaps_albers', x=(x1, x2), y=(y1,y2))
	print la
	if layer == "1":
		a = la.blue
	elif layer == "2":
		a = la.green
	elif layer == "3":
		a = la.red
	elif layer == "4":
		a = la.nir
	print str(year)
	a = a.loc[str(year)]
	a.plot()
	path = 'media/images/' +  str(year) + '.png'
	plt.savefig(path)
	plt.clf()
	return path
