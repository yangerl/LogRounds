from django.shortcuts import get_object_or_404, render, redirect 

# Create your views here.
from django.utils import *
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from logrounds.models import *
from logrounds.forms import *

def home(request):
	head = 'Welcome to the CUP Logging application (Admin Version)!'
	create = 'Click here to create a new round.'
	index = 'Click here to go to Rounds index'
	context = {
		'create' : create,
		'index' : index,
		'head' : head
	}
	
	return render(request, 'logrounds/home.html', context)

def index(request):
	rounds_list = RoundType.objects.order_by('-start_date')
	h1 = 'This is the index for all rounds that have been created!'
	h2 = 'Click on one of these Rounds to view details'
	else_p = 'No rounds are available.'
	context = {
		'rounds_list' : rounds_list,
		'h1' : h1,
		'h2' : h2,
		'else_p' : else_p
	}
	return render(request, 'logrounds/index.html', context)

def round_detail(request, round_id):
	get_round = get_object_or_404(RoundType, pk=round_id)
	logdef_qs = LogDef.objects.filter(rt=get_round)
	logset_qs = set()
	start_date = get_round.start_date


	context = {	
		'round' : get_round,
		'logdef_qs' : logdef_qs,
		'logset_qs' : logset_qs, 
		'start_date' : start_date,
	}
	return render(request, 'logrounds/round_detail.html', context)

class RoundCreate(CreateView):
	template_name_suffix = '_form_create'
	model = RoundType
	success_url = reverse_lazy('logrounds:new_logdef')
	fields = ['rt_name', 'rt_desc', 'start_date']

class RoundUpdate(UpdateView):
	template_name_suffix = '_form_update'
	model = RoundType
	fields = ['rt_name', 'rt_desc']

class RoundDelete(DeleteView):
	model = RoundType
	success_url = reverse_lazy('logrounds:index')



def activities(request, round_id):
	get_round = get_object_or_404(RoundType, pk=round_id)
	logdef_qs = LogDef.objects.filter(rt=get_round)
	entry_tuple = []
	buffer_time = timedelta(0,0,0,0,15)
	curr_time = timezone.now()
	logset_qs = set()
	start_date = get_round.start_date


	lowest = None
	lowest_phase = None
	lowest_period = None
	buffer_time = timedelta(0,0,0,0,15)
	for lgdf in logdef_qs:
		if (lowest_period is None) or (lowest_period > lgdf.period.parse_period()):
			lowest_period = lgdf.period.parse_period()
		if (lowest_phase is None) or (lowest_phase > lgdf.period.parse_phase()):
			test = lgdf.period.phase
			lowest_phase = lgdf.period.parse_phase()
		temp = LogSet.objects.filter(rt=get_round).order_by('-start_time')[:1]

		if temp:
			logset_qs.add(temp)
			if (lowest is None) or (lowest < temp[0].next_time):
				lowest = temp[0].next_time


	if (lowest is None):
		start_date =  lowest_phase + start_date
	else:
		start_date = lowest

	next_start_time = start_date + lowest_period

	while (curr_time > next_start_time):
		missed_lgst = LogSet(rt=get_round, start_time=start_date, \
			next_time=next_start_time,log_time=None, status=0 )
		missed_lgst.save()
		start_date = next_start_time
		next_start_time = next_start_time + lowest_period

	curr_lgst = LogSet.objects.filter(next_time = start_date)[:1]
	if (not curr_lgst) and (curr_time >= start_date) and (curr_time<=next_start_time):
		curr_lgst = LogSet(rt=get_round, start_time=start_date, \
				next_time=next_start_time,log_time=curr_time, status=1)
		curr_lgst.save()
	elif (not curr_lgst) and (curr_time < start_date):
		curr_lgst = LogSet(rt=get_round, start_time=start_date, \
				next_time=next_start_time,log_time=None, status=-1)
		curr_lgst.save()
	else:
		curr_lgst = curr_lgst[0]

	context = {
		'round': get_round,
		'logdef_qs' : logdef_qs,
		'tuple' : entry_tuple,
		'buffer_time' : buffer_time,
	
	}
	return render(request, 'logrounds/activities.html', context)


"""
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
"""

class LogDefCreate(CreateView):
	template_name_suffix = '_form_create'
	model = LogDef
	success_url = reverse_lazy('logrounds:new_logdef')
	fields = ['rt','period','name','desc','is_qual_data',
				'units','low_low','high_high','low','high']

class LogDefUpdate(UpdateView):
	pass
class LogDefDelete(DeleteView):
	pass


def logdef_detail(request, logdef_id):
	# Queryset of the LogDef needed
	get_lgdf_qs = LogDef.objects.filter(pk = logdef_id)
	# if not exists
	if (not get_lgdf_qs):
		raise Http404("No LogDef matches the given query.")
	else:
		lgdf_dict = get_lgdf_qs.values()[0]
		pd = get_object_or_404(Period, pk =lgdf_dict['period_id'])
		rt = get_object_or_404(RoundType, pk=lgdf_dict['rt_id'])
		context = {'dict' : lgdf_dict,
					'round' : rt,
					'lgdf' : get_lgdf_qs[0],
					'pd' : pd }
		return render(request, 'logrounds/logdef_detail.html', context)

def edit_logdef(request, logdef_id):
	h1 = 'Edit one of more Log Properties'
	redir = request.path
	instance = LogDef.objects.get(pk=logdef_id)
	if request.method == "POST":
		form = LogDefForm(request.POST, instance=instance)
		if(form.is_valid()):
			post = form.save()
			regex = re.compile('^.*(/logrounds/logdef/[0-9]+/)edit')
			redir = regex.match(redir).group(1)
			return HttpResponseRedirect(redir)
	else:
		form = LogDefForm(instance=instance)
	context = {'form': form, 'h1' : h1, 'redir' : redir}
	return render(request, 'logrounds/edit_logdef.html', context)


def add_period(request): 
	h1 = ' Welcome to Period Creation, please fill out this form'
		
	redir=get_next(request)
	if request.method == "POST":
		form = PeriodForm(request.POST)
		if(form.is_valid()):
			post = form.save()		
			return HttpResponseRedirect(redir)
	else:
		form = PeriodForm()
	context = {'form': form, 'h1': h1,} 
	return render(request, 'logrounds/add_period.html', context)






### custom methods

def get_next(request):
	req = request.get_full_path()
	regex = re.compile('^.*\?next=(/.*)')
	match = regex.match(req)
	# STRIGN SANITIZATION NEEDED, TESTING ONLY
	return match.group(1)

#

def periods(request):
	return HttpResponse("Hello World")
	
