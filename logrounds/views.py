from django.shortcuts import get_object_or_404, render, redirect 

# Create your views here.
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import SafeString
from django.utils import *
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from logrounds.models import *
from logrounds.forms import *


@login_required
def index(request):
	rounds_list = RoundType.objects.order_by('-start_date')
	due_date_list = []
	max_time = timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	duedate_to_round = {}
	# dictionary that stores dict -> roundlist
	for rounds in rounds_list:
		this_logset = update_logsets(rounds)
		this_due_date = LogSet.objects.duedate(this_logset)
		if this_due_date is None:
			this_due_date = max_time
		due_date_list.append(this_due_date)

		if (this_due_date in duedate_to_round):
			duedate_to_round[this_due_date].append(rounds)
		else:
			duedate_to_round[this_due_date] = [rounds]

	
	(due_date_list).sort()
	due_date_list = set(due_date_list)
	# sort ascending so that the rounds will be displayed in order
	context = {
		'rounds_list' : rounds_list,
		'dd_list' : due_date_list,
		'dict' : duedate_to_round,
		'max' : max_time,
	}
	return render(request, 'logrounds/index.html', context)
@login_required
def round_detail(request, round_id):
	get_round = get_object_or_404(RoundType, pk=round_id)
	logdef_qs = LogDef.objects.filter(rt=get_round)
	logset_qs = set()


	if request.method == "POST":
		new_post = request.POST.copy()
		new_post['start_time'] = request.POST['start_time'].replace(" ","")

		form = DataGridForm(new_post)
		
		if(form.is_valid()):

			start_datetime = datetime.combine(
				form.cleaned_data['start_date'], 
				form.cleaned_data['start_time']
				
			)
			context = {
				'round' : get_round,
				'period' : get_round.period,
				'logdef_qs' : logdef_qs,
				'logset_qs' : logset_qs, 
				'form' : form,

			}
			return redirect('logrounds:data_grid', round_id,start_datetime)
				
	else:
		form = DataGridForm()
		form.fields['start_date'].initial = get_round.start_date.strftime("%m/%d/%Y")

	context = {	
		'round' : get_round,
		'period' : get_round.period,
		'logdef_qs' : logdef_qs,
		'logset_qs' : logset_qs, 
		'form' : form,
		'start_date' : get_round.start_date,
	}

	
	return render(request, 'logrounds/round_detail.html', context)


class RoundCreate(CreateView):
	template_name_suffix = '_form_create'
	model = RoundType
	form_class = RoundTypeForm
	#fields = ['rt_name', 'period', 'rt_desc', 'start_date']

	def get_context_data(self, **kwargs):
		ans = super(RoundCreate, self).get_context_data(**kwargs)
		ans['curr_time'] = timezone.now()
		return ans

	def get_success_url(self):
		return reverse_lazy('logrounds:new_logdef',kwargs={'round_id':self.object.id})


class RoundUpdate(UpdateView):
	template_name_suffix = '_form_update'
	model = RoundType
	fields = ['rt_name', 'period', 'rt_desc']


class RoundDelete(DeleteView):
	model = RoundType
	success_url = reverse_lazy('logrounds:index')

@login_required
def activities(request, round_id):
	get_round = get_object_or_404(RoundType, pk=round_id)
	period = get_round.period.parse_period()
	phase = get_round.period.parse_phase()
	logdef_qs = LogDef.objects.filter(rt=get_round)
	logset_qs = LogSet.objects.filter(rt=get_round)
	start_date = get_round.start_date
	curr_lgst = update_logsets(get_round)
	# Changed to a custom method named 'update_logsets'
	# # set current logset to the original logset, then iterate to find all missing
	# first_lgst = LogSet.objects.filter(rt=get_round.id, \
	# 		start_time=(get_round.start_date + phase),\
	# 		next_time=get_round.start_date + phase + period)
	# curr_lgst = None
	# if (not first_lgst):
	# 	# if first logset doesnt exist, create it and set the current to it
	# 	orig_lgst = LogSet(rt=get_round, 
	# 			start_time=get_round.start_date + phase,
	# 			next_time=get_round.start_date + phase + period,
	# 			log_time= None,
	# 			status = LogSet.IN_PROGRESS,)
	# 	orig_lgst.save()
	# 	curr_lgst=orig_lgst
	# else:
	# 	# A logset with the original time is there so we set our 
	# 	# curr_lgst at the original (as a starting point for 
	# 	# iteration
	# 	curr_lgst = first_lgst[0]

	# curr_time = timezone.now()
	# while (curr_time > curr_lgst.next_time):
	# 	nxt = curr_lgst.next_time
	# 	# update old status to missed if it was in progress
	# 	# if it was completed do nothing  to it			
	# 	if (curr_lgst.status is None) \
	# 		or (curr_lgst.status ==	LogSet.IN_PROGRESS) \
	# 		or (curr_lgst.status == LogSet.IN_PROGRESS_LATE):
	# 		# if it is one of these 3 statuses, it must be updated!
	# 		# 3 lines to update status
	# 		curr_lgst.log_time = LogSet.objects.latest_logtime(curr_lgst)
	# 		curr_lgst.status = LogSet.objects.status_update(curr_lgst, logdef_qs)
	# 		curr_lgst.save()

	# 		# 2 lines to create next 'curr_lgst' in iteration
	# 		curr_lgst = LogSet(rt=get_round, start_time=curr_lgst.next_time\
	# 			, next_time=curr_lgst.next_time + period,\
	# 			log_time=None, status=None)
	# 		curr_lgst.save()
	
	# 	else:
	# 		# if it is not None status, or inprogress we can just
	# 		# go to the next logset in the iteration
	# 		try:
	# 			curr_lgst= LogSet.objects.get(rt=get_round, \
	# 				start_time=curr_lgst.next_time, \
	# 				next_time=curr_lgst.next_time + period)
	# 		except LogSet.DoesNotExist:
	# 			curr_lgst = LogSet(
	# 							rt=get_round,\
	# 							start_time=curr_lgst.next_time,\
	# 							next_time=curr_lgst.next_time+period,\
	# 							log_time=None, status=None)

	# 	# Now we have to give the most recent one a status!
	# 	# This can only be complete/complete(late)/inprogress/inprogress(late)
	# 	# because we know that the curr_time < curr_lgst.next_time

	# 	newstatus =LogSet.objects.status_update(curr_lgst,logdef_qs)
	# 	if (newstatus != LogSet.COMPLETE) \
	# 		and (newstatus != LogSet.COMPLETE_LATE):
	# 		# if it is considered 'missed'
	# 		if (curr_time <= LogSet.objects.duedate(curr_lgst)):
	# 			newstatus = LogSet.IN_PROGRESS
	# 		else:
	# 			newstatus = LogSet.IN_PROGRESS_LATE
	# 	curr_lgst.log_time = LogSet.objects.latest_logtime(curr_lgst)
	# 	curr_lgst.status = newstatus
	# 	curr_lgst.save()
		
	# 		# if (curr_lgst.status == 1):
	# 		# 	curr_lgst.status = 0
	# 		# 	curr_lgst.log_time=None
	# 		# 	curr_lgst.save()
	# 		# 	# create new 'curr_lgst' 1 period away
	# 		# 	curr_lgst = LogSet(rt=get_round, start_time=curr_lgst.next_time\
	# 		# 		, next_time=curr_lgst.next_time + period,\
	# 		# 		log_time=timezone.now(), status=1)
	# 		# 	curr_lgst.save()
	# 		# else:
	# 		# 	curr_lgst= LogSet.objects.get(rt=get_round, \
	# 		# 		start_time=curr_lgst.next_time, \
	# 		# 		next_time=curr_lgst.next_time + period)
	# 		# iteration checks if this new logset was missed

	lgdf_lgentry = {}

	for lgdf in logdef_qs:
		

		curr_entry = LogEntry.objects.filter(lg_set=curr_lgst,lg_def=lgdf).\
			order_by('-log_time')
		if curr_entry:

			curr_entry = LogEntry.objects.get(pk=curr_entry[0].id)
		else:
			curr_entry = None 

		lgdf_lgentry[lgdf] = curr_entry

		#use the current logdef for this period temporarily to find the entry

	context = {
		'round': get_round,
		'time' : timezone.now(),
		'period': get_round.period.name,
		'logdef_qs' : logdef_qs,
		'curr_lgst' : curr_lgst,
		'lgdf_lgentry' : lgdf_lgentry,
	}
	return render(request, 'logrounds/activities.html', context)

@login_required
def data_grid(request, round_id, start_time):

	this_round = get_object_or_404(RoundType, pk=round_id)
	update_logsets(this_round)
	# All logsets after the specified time
	logset_qs = LogSet.objects.filter(
		rt=this_round,
		start_time__gte = start_time
	).order_by('start_time')

	logdef_qs = LogDef.objects.filter(rt=this_round)


	# list of json objects, each representing a row in the grid
	# each object is as follows:
	# {
	#	time: Logset.start_time,
	# 	logdef_1: str(logentry value) + logdef1 units,
	#	logdef_2: str(logentry value) + logdef2 units,
	#	if it has qualatative value...
	#	logdef_n: str(logentry select_value)
	# }

	jqxJSON_input = []
	logdef_name = []
	id = 0
	for lgdf in logdef_qs:
			logdef_name.append(lgdf.name)

	for lgst in logset_qs:
		row_obj = {}
		row_obj["id"] = str(id)
		id += 1
		row_obj['time'] = lgst.start_time.strftime("%m-%d-%Y %H:%M")
		

		for lgdf in logdef_qs:
			curr_entry = LogEntry.objects.filter(
				lg_set = lgst,
				lg_def = lgdf,
			).order_by('-log_time')

			# If most recent entry exists continue creating the JSON obj
			# else create json obj with the value 'DoesNotExist'

			if curr_entry:
				# change the 1 entry list to the entry
				curr_entry = curr_entry[0] 
				if lgdf.is_qual_data:
					row_obj[lgdf.name] = curr_entry.select_value
				else:
					row_obj[lgdf.name] = str(curr_entry.num_value) +' '+ lgdf.units

			else:
				row_obj[lgdf.name] = 'Entry Does Not Exist'
		jqxJSON_input.append(row_obj)
	jqxJSON_input = json.dumps(jqxJSON_input,cls=DjangoJSONEncoder)
	logdef_name = json.dumps(logdef_name,cls=DjangoJSONEncoder)
	context = {
		'round' : this_round,
		'start' : start_time,
		'logdefs' : SafeString(logdef_name),
		'logsets' : logset_qs,
		'json' : SafeString(jqxJSON_input),
	} 

	return render(request, 'logrounds/data_grid.html', context)






class LogDefCreate(CreateView):

	template_name_suffix = '_form_create'
	model = LogDef
	fields = ['rt','period','name','desc','is_qual_data',
				'units','low_low','high_high','low','high']

	def get_success_url(self):
 	   return reverse_lazy('logrounds:new_logdef')+'?next='+str(self.object.rt.id)

@login_required
def create_logdef(request, round_id):
	this_round = get_object_or_404(RoundType, pk=round_id)
	if request.method == "POST":
		form = LogDefForm(request.POST)
		if(form.is_valid()):
			post = form.save()		
			return redirect('logrounds:new_logdef', round_id)
				
	else:
		form = LogDefForm(initial={
			'rt': this_round
		})

	context = {
		'form': form,
		'round' : this_round,
	} 
	return render(request, 'logrounds/logdef_form_create.html', context)


class LogDefDelete(DeleteView):
	model = LogDef
	def get_success_url(self):
		return reverse_lazy('logrounds:detail',kwargs={'round_id':self.object.rt.id})
 
@login_required
def logdef_detail(request, logdef_id):
	# Queryset of the LogDef needed
	lgdf = get_object_or_404(LogDef,pk=logdef_id)
	rt = get_object_or_404(RoundType, pk=lgdf.rt_id)
	context = {'dict' : lgdf,
				'round' : rt,
				'lgdf' : lgdf,
	}
	return render(request, 'logrounds/logdef_detail.html', context)

@login_required
def edit_logdef(request, logdef_id):
	h1 = 'Edit one of more Log Properties'
	regex = re.compile('^.*(/logrounds/logdef/[0-9]+/)edit')
	redir = regex.match(request.path).group(1)

	instance = LogDef.objects.get(pk=logdef_id)
	if request.method == "POST":
		form = LogDefForm(request.POST, instance=instance)
		test = request.POST
		
		if(form.is_valid()):
			post = form.save()
		
			return HttpResponseRedirect(redir)
		
		form = LogDefForm(instance=instance)

	else:
		form = LogDefForm(instance=instance)
	context = {'form': form, 'h1' : h1, 'redir' : redir}
	return render(request, 'logrounds/edit_logdef.html', context)

@login_required
def add_period(request): 
	h1 = ' Welcome to Period Creation, please fill out this form'
	req = request.get_full_path()
	regex = re.compile('^.*\?next=(/.*)')
	match = regex.match(req)
	# STRIGN SANITIZATION NEEDED, TESTING ONLY
	redir=match.group(1)
	if request.method == "POST":
		form = PeriodForm(request.POST)
		if(form.is_valid()):
			
			post = form.save()		
			return HttpResponseRedirect(redir)
	else:
		form = PeriodForm()
	context = {
		'form': form, 
		'h1': h1,
		'redir' : redir,
		'now' : timezone.now,
	} 
	return render(request, 'logrounds/add_period.html', context)

@login_required
def create_entry(request, round_id, ld_id, ls_id):
	h1 = ' Welcome to Data Entry, please fill out this form'
	h2 = ''
	logdef = get_object_or_404(LogDef, pk=ld_id)
	logset = get_object_or_404(LogSet, pk=ls_id)
	if request.method == "POST":
		form = LogEntryForm(request.POST)
		if(form.is_valid()):
			# see if it is outside the absolute bounds
			# it shouod not throw a validation error normally
			# beacuse the 'form is valid' has already been checked
			# the only validation error thrown should be the one
			# that was created in the models
			try:
				post = form.save()
			except ValidationError:

				newPost = request.POST.copy()
				newPost['log_time'] = timezone.now()
				form = LogEntryForm(newPost)

			
				context = {
					'form': form, 
					'h1': h1, 
					'h2': 'Value is not with absolute bounds',
					'logdef': logdef,
					'round_id':round_id
				}
				return render(
					request, 
					'logrounds/logentry_form_create.html', 
					context
				)

			else:
				return redirect('logrounds:activities',round_id)
	else:
		form = LogEntryForm(initial={
			'lg_set': logset,
			'lg_def': logdef,
			'parent': None,
			'log_time': timezone.now
		})
	context = {
		'form': form, 
		'h1': h1, 
		'h2':h2, 
		'logdef' : logdef,
		'round_id':round_id
	} 
	return render(request, 'logrounds/logentry_form_create.html', context)


class LogEntryDetailView(DetailView):
	model = LogEntry

	def get_context_data(self, **kwargs):
		context = super(LogEntryDetailView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context

@login_required
def entry_update(request, round_id, ld_id, ls_id, parent):
	h1 = ' Welcome to Data Entry, please fill out this form'
	if request.method == "POST":
		form = LogEntryForm(request.POST)
		if(form.is_valid()):
			
			post = form.save()
		
			return redirect('logrounds:activities',round_id)
	else:
		form = LogEntryForm(initial={
			'lg_set': LogSet.objects.get(pk=ls_id),
			'lg_def': LogDef.objects.get(pk=ld_id),
			'parent': parent,
			'log_time': timezone.now
		})
	context = {'form': form, 'h1': h1, 'round_id' : round_id} 
	return render(request, 'logrounds/logentry_form_create.html', context)

### custom methods

def update_logsets(get_round):
	period = get_round.period.parse_period()
	phase = get_round.period.parse_phase()
	logdef_qs = LogDef.objects.filter(rt=get_round)
	# set current logset to the original logset, then iterate to find all missing
	#first_lgst = LogSet.objects.filter(rt=get_round.id, \
	#		start_time=(get_round.start_date + phase),\
	#		next_time=get_round.start_date + phase + period)
	first_lgst = LogSet.objects.filter(rt=get_round.id).order_by('-start_time')
	curr_lgst = None

	if (not first_lgst):
		# if first logset doesnt exist, create it and set the current to it
		orig_lgst = LogSet(rt=get_round, 
				start_time=get_round.start_date + phase,
				next_time=get_round.start_date + phase + period,
				log_time= None,
				status = LogSet.IN_PROGRESS,)
		orig_lgst.save()
		curr_lgst=orig_lgst
	else:
		# A logset with the original time is there so we set our 
		# curr_lgst at the original (as a starting point for 
		# iteration
		curr_lgst = first_lgst[0]

	curr_time = timezone.now()

	while (curr_time > curr_lgst.next_time):
		nxt = curr_lgst.next_time

		# update old status to missed if it was in progress
		# if it was completed do nothing  to it			
		if (curr_lgst.status is None) \
			or (curr_lgst.status ==	LogSet.IN_PROGRESS) \
			or (curr_lgst.status == LogSet.IN_PROGRESS_LATE):
			# if it is one of these 3 statuses, it must be updated!
			# 3 lines to update status
			curr_lgst.log_time = LogSet.objects.latest_logtime(curr_lgst)
			curr_lgst.status = LogSet.objects.status_update(curr_lgst, logdef_qs)
			curr_lgst.save()

			# 2 lines to create next 'curr_lgst' in iteration
			curr_lgst = LogSet(rt=get_round, start_time=curr_lgst.next_time\
				, next_time=curr_lgst.next_time + period,\
				log_time=None, status=None)
			curr_lgst.save()
	
		else:
			# if it is not None status, or inprogress we can just
			# go to the next logset in the iteration
			try:
				curr_lgst= LogSet.objects.get(rt=get_round, \
					start_time=curr_lgst.next_time, \
					next_time=curr_lgst.next_time + period)
			except LogSet.DoesNotExist:
				curr_lgst = LogSet(
								rt=get_round,\
								start_time=curr_lgst.next_time,\
								next_time=curr_lgst.next_time+period,\
								log_time=None, status=None)

		# Now we have to give the most recent one a status!
		# This can only be complete/complete(late)/inprogress/inprogress(late)
		# because we know that the curr_time < curr_lgst.next_time

	newstatus =LogSet.objects.status_update(curr_lgst,logdef_qs)

	if (newstatus != LogSet.COMPLETE) \
		and (newstatus != LogSet.COMPLETE_LATE):
		# if it is considered 'missed'
		my_duedate = LogSet.objects.duedate(curr_lgst)
		if my_duedate is None:
			newstatus = LogSet.IN_PROGRESS
		elif (curr_time <= my_duedate):
			newstatus = LogSet.IN_PROGRESS
		else:
			newstatus = LogSet.IN_PROGRESS_LATE
	curr_lgst.log_time = LogSet.objects.latest_logtime(curr_lgst)
	curr_lgst.status = newstatus
	curr_lgst.save()
	return curr_lgst