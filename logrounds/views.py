from django.shortcuts import get_object_or_404, render, redirect 

# Create your views here.
from django.utils import *
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
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
	fields = ['rt_name', 'rt_desc', 'start_date']

	def get_context_data(self, **kwargs):
		ans = super(RoundCreate, self).get_context_data(**kwargs)
		ans['curr_time'] = timezone.now()
		return ans

	def get_success_url(self):
		return reverse_lazy('logrounds:new_logdef',kwargs={'round_id':self.object.id})

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
	logset_qs = set()
	start_date = get_round.start_date


	# MOM'S SPAGHETTI CODE WARMING
	# THE DRAGON LIES BELOW, ONLY THE BRAVE SHOULD READ
	# Can I make this into a helper function? Who knows? it will probably
	# only be used in this section anyways


	# curr_lgst_dict = {period: curr_logset}
	# for each period, match it to the most recent logset of the entries

	curr_lgst_dict={}

	for lgdf in logdef_qs:
		phase = lgdf.period.parse_phase()
		period = lgdf.period.parse_period()
		# get the originally logset. If this doesnt exist, then this process 
		# has not been run before so it will iterate up until the current 
		# logset and create all missing entries. If it does exist then we still
		# must verify  that it is the logset using the next_time. If this is 
		# not verified, create a new logset w/ corresponding start/next times
		# If this is verified, use this as the starting point for while loop to
		# iteratively find missing logsets
		lgst_qs  = LogSet.objects.filter(rt=get_round.id, \
			start_time=(get_round.start_date + phase),\
			next_time=get_round.start_date + phase + period)

		curr_lgst = None
		if (not lgst_qs):
			# The 'original' LogSet is missing, so this process has not been 
			# run before. Create the original logset, then loop to find
			# missing logsets.
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
			curr_lgst = lgst_qs[0]

		# we will only do the iteration if this logset has not been processed
		# yet during this page load. So if Steam and Temp are both hourly, and
		# Temp has already been processed, we don't need to check Steam b/c
		# Temp should have already made sure there are no missing LogSets

		curr_time = timezone.now()
		if (curr_lgst not in logset_qs):
			logset_qs.add(curr_lgst)
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
				if (curr_time <= LogSet.objects.duedate(curr_lgst)):
					newstatus = LogSet.IN_PROGRESS
				else:
					newstatus = LogSet.IN_PROGRESS_LATE
			curr_lgst.log_time = LogSet.objects.latest_logtime(curr_lgst)
			curr_lgst.status = newstatus
			curr_lgst.save()
			
				# if (curr_lgst.status == 1):
				# 	curr_lgst.status = 0
				# 	curr_lgst.log_time=None
				# 	curr_lgst.save()
				# 	# create new 'curr_lgst' 1 period away
				# 	curr_lgst = LogSet(rt=get_round, start_time=curr_lgst.next_time\
				# 		, next_time=curr_lgst.next_time + period,\
				# 		log_time=timezone.now(), status=1)
				# 	curr_lgst.save()
				# else:
				# 	curr_lgst= LogSet.objects.get(rt=get_round, \
				# 		start_time=curr_lgst.next_time, \
				# 		next_time=curr_lgst.next_time + period)
				# iteration checks if this new logset was missed
		
		else:	
			# if we are in this code block, then all the missing LogSets have
			# already been validated when it was run for a different LogDef
			# This means that we should be able to assume that there is an
			# existing compatible LogSet for this LogDef. Find it by 
			# iterating until we are less than the next_time
			iterations = 0
			while(curr_time > curr_lgst.next_time + (period * iterations)):
				# No database interaction so hopefully loads faster than above!
				# finds number of iterations to reach the start_time
				iterations += 1

			start_time = curr_lgst.start_time + (period * iterations)
			next_time = start_time + period
			curr_lgst = LogSet.objects.get(rt=get_round, \
				start_time=start_time, next_time=next_time)

		curr_lgst_dict[lgdf.period] = curr_lgst

	# If you are reading at this point, great, to update on what has happened
	# 1) All missing logsets for the current logdef have been updated 
	# 2) If LogDefs share logsets, skips the updating process (waste of time)
	# 3) All logdefs that were missed are now marked with as missed (status=1)
	# 4) the 'curr_lgst' variable is the logset that the logentry should be
	# created with. This status=0, in progress

	# We now want to get the data that we want to show the user and put it
	# into the entry_tuple List. Where the tuple is a (logdef, {})

	# The page is organized by each period -> attributes
	# Under each Period, all its LogDefs will be listed
	# We need to get the unique set of Periods for this Round
	pd_set = set()
	pd_lgdf = {} #pd_lgdf = {period: {logdef:logentry}}

	for lgdf in logdef_qs:
		pd_set.add(lgdf.period)

		# key = (period, most_recent_logset_for_period) Value = [logdef1, logdef2,...]
		# temp1 is the most recent logset for the period
		temp_lgst = curr_lgst_dict[lgdf.period]
		curr_entry = LogEntry.objects.filter(lg_set=temp_lgst,lg_def=lgdf).\
			order_by('-log_time')
		if curr_entry:

			curr_entry = LogEntry.objects.get(pk=curr_entry[0].id)
		else:
			curr_entry = None 

		if lgdf.period in pd_lgdf.keys():
			pd_lgdf[lgdf.period].append({lgdf:curr_entry})
		else:
			pd_lgdf[lgdf.period] = [{lgdf:curr_entry}]

		#use the current logdef for this period temporarily to find the entry


	time = timezone.now()



	context = {
		'round': get_round,
		'logdef_qs' : logdef_qs,
		'pd_lgdf_keys' : pd_lgdf.keys(),
		'pd_lgdf' : pd_lgdf,
		'time' : time,
		'curr_lgst_dict': curr_lgst_dict
	
	}
	return render(request, 'logrounds/activities.html', context)
	
class LogDefCreate(CreateView):

	template_name_suffix = '_form_create'
	model = LogDef
	fields = ['rt','period','name','desc','is_qual_data',
				'units','low_low','high_high','low','high']

	def get_success_url(self):
 	   return reverse_lazy('logrounds:new_logdef')+'?next='+str(self.object.rt.id)

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
	success_url = reverse_lazy('logrounds:index')


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
		lgdf = get_object_or_404(LogDef, pk=logdef_id)
		context = {'dict' : lgdf_dict,
					'round' : rt,
					'lgdf' : lgdf,
					'pd' : pd }
		return render(request, 'logrounds/logdef_detail.html', context)

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
	context = {
		'form': form, 
		'h1': h1,
		'redir' : redir,
		'now' : timezone.now,
	} 
	return render(request, 'logrounds/add_period.html', context)


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

def get_next(request):
	req = request.get_full_path()
	regex = re.compile('^.*\?next=(/.*)')
	match = regex.match(req)
	# STRIGN SANITIZATION NEEDED, TESTING ONLY
	return match.group(1)

#

def periods(request):
	return HttpResponse("Hello World")
	
