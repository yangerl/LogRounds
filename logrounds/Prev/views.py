from django.shortcuts import get_object_or_404, render, redirect 

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest

from logrounds.models import *
from logrounds.forms import *

def home(request):
	head = 'Welcome to the CUP Logging application (Admin Version)!'
	create = 'Click here to create a new round.'
	index = 'Click here to go to Rounds index'
	context = {'create' : create,
				'index' : index,
				'head' : head}
	return render(request, 'logrounds/home.html', context)

def index(request):
	rounds_list = RoundType.objects.order_by('-start_date')
	h1 = 'This is the index for all rounds that have been created!'
	h2 = 'Click on one of these Rounds to view details'
	else_p = 'No rounds are available.'
	context = {'rounds_list' : rounds_list,
				'h1' : h1,
				'h2' : h2,
				'else_p' : else_p
			}
	return render(request, 'logrounds/index.html', context)

def round_detail(request, round_id):
	get_round = get_object_or_404(RoundType, pk=round_id)
	logdef_qs = LogDef.objects.filter(rt=get_round)
	logset_qs = set()

	for lgdf in logdef_qs:
		temp = LogSet.objects.filter(logdef=lgdf).order_by('-start_time')
		if temp:
			logset_qs.add(temp)
	context = {'round' : get_round,
				'logdef_qs' : logdef_qs,
				'logset_qs' : logset_qs }
	return render(request, 'logrounds/round_detail.html', context)


def create(request):
	h1 = 'Welcome to Round Creation, please fill out this form'
	if request.method == "POST":
		form = RoundTypeForm(request.POST)
		if(form.is_valid()):
			post = form.save()
			return HttpResponseRedirect('/logrounds/add_logdef')
	else:
		form = RoundTypeForm()
	context = {'form': form, 'h1' : h1}
	return render(request, 'logrounds/create.html', context)

def add_logdef(request):
	h1 = 'Create one of more Log Properties'
	if request.method == "POST":
		form = LogDefForm(request.POST)
		if(form.is_valid()):
			post = form.save()
			return HttpResponseRedirect('/logrounds/add_logdef')
	else:
		form = LogDefForm()
	context = {'form': form, 'h1' : h1, 'redir':request.path}
	return render(request, 'logrounds/add_logdef.html', context)

def logdef_detail(request, logdef_id):
	# Queryset of the LogDef needed
	get_lgdf_qs = LogDef.objects.filter(pk = logdef_id)
	# if not exists
	if (not get_lgdf_qs):
		raise Http404("No LogDef matches the given query.")
	else:
		lgdf_dict = get_lgdf_qs.values()[0]
		lgdf_keys = lgdf_dict.keys()

		rt = get_object_or_404(RoundType, pk=lgdf_dict['rt_id'])
		context = {'dict' : lgdf_dict,
					'keys' : lgdf_keys,
					'round' : rt,
					'lgdf' : get_lgdf_qs[0], }
		return render(request, 'logrounds/logdef_detail.html', context)

def edit_logdef(request, logdef_id):
	h1 = 'Edit one of more Log Properties'
	redir = ""
	instance = LogDef.objects.get(pk=logdef_id)
	if request.method == "POST":
		form = LogDefForm(request.POST, instance=instance)
		if(form.is_valid()):
			post = form.save()
			return HttpResponseRedirect(redir)
	else:
		form = LogDefForm(instance=instance)
	context = {'form': form, 'h1' : h1, 'redir' : redir}
	return render(request, 'logrounds/edit_logdef.html', context)


	
def add_period(request): 
	h1 = ' Welcome to Period Creation, please fill out this form'
	if request.method == "POST":
		form = PeriodForm(request.POST)
		if(form.is_valid()):
			post = form.save()
			
			return HttpResponseRedirect(redir)
	else:
		form = PeriodForm()
	context = {'form': form, 'h1': h1,} 
	return render(request, 'logrounds/add_period.html', context)




def periods(request):
	return HttpResponse("Hello World")
	
