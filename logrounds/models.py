from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from datetime import date, datetime, time, timedelta
from django.core.exceptions import ValidationError
import re

# Create your models here.


@python_2_unicode_compatible
class Period (models.Model):
	""" This defines the periodicity of the Round """
	name = models.CharField(max_length=100,unique=True)
	scale = models.IntegerField(null=False, blank=False, help_text="Time between Sets")
	unit = models.CharField(max_length=10, help_text="Units for the scale (days, hours, or minutes)")
	#phase = models.CharField(max_length=12, default="0d,0h,0m", help_text= \
	#						"Input in form XXd,XXh,XXm. default 0d,0h,0m")
	phase_days = models.IntegerField()
	phase_hours = models.IntegerField()
	phase_min = models.IntegerField()

	def parse_period(self):
		lower = self.unit.lower()
		if (re.match('^d', lower)):
			return timedelta(self.scale)
		elif (re.match('^h', lower)):
			return timedelta(0,0,0,0,0,self.scale)
		elif (re.match('^m', lower)):
			return timedelta(0,0,0,0,scale,0)
		else:
			raise Exception ("uncaught unit type")

	def parse_phase(self):
		return timedelta(self.phase_days,0,0,0,self.phase_min,self.phase_hours)
		"""
		def parse_phase(self):
			regex = re.compile('^([0-9]+)d,([0-9]+)h,([0-9]+)m$',re.UNICODE)
			dddd= self.phase
			match1 = re.match(regex, dddd)
			# timedelta([days[,sec[,micro[,mill[,min[,hour[,weels]]]]]]])
			""
			days = match1.group(1)
			hours = match1.group(2)
			mins = match1.group(3)

			phase = timedelta(int(days),0,0,0,int(mins),int(hours))
			return phase
		"""
	def __str__(self):
		return self.name

class RoundType(models.Model):
		""" This defines a series of columns. """
		rt_name = models.CharField(max_length=50)

		#describe the purpose of the round etc.
		rt_desc = models.TextField(max_length=None)
		start_date = models.DateTimeField()
		period = models.ForeignKey(Period, on_delete = models.CASCADE,\
			related_name = 'prd')

		def get_absolute_url(self):
			return reverse('logrounds:detail', args=[str(self.pk)])

		def __str__(self):
			return self.rt_name


class LogDef(models.Model):
	""" This represents a 'column' of data """
	rt = models.ForeignKey(RoundType, on_delete=models.CASCADE,\
			related_name = 'col')
	# This is the frequency to generate new LogSets
	
	name = models.CharField(max_length=100)

	# Give info about the data being collected, location, safety etc.
	desc = models.TextField(max_length=None, null=True, blank=True)



	is_qual_data = models.BooleanField(default=False)
	units = models.CharField(null=True, max_length=20, blank=True)
	# units might be moved to 'data types class'
	low_low = models.FloatField(null=True, blank=True)
	high_high = models.FloatField(null=True, blank=True)
	low = models.FloatField(null=True, blank=True)
	high = models.FloatField(null=True, blank=True)

	# def create_first_logset(self):
	# 	# to do this we need to check if there is alreay a Logset in existence
	# 	# Perform this step first.

	# 	logsets = LogSet.objects.filter(rt=self.rt)
	# 	# if empty create new LogSet
	# 	if (not logsets): # python 'style' for checking empty list
	# 		start_time = self.rt.start_date + self.period.parse_phase()
	# 		end_time = start_time + self.period.parse_period()

	# 		first_logset = LogSet(rt=self.rt, parent_ls=None,\
	# 								start_time = start_time,\
	# 								end_time = end_time,\
	# 								log_time = None)
	#		first_logset.save()

	def save(self,  *args, **kwargs):
		# change the period to match this logdef
		
		super(LogDef, self).save(*args, **kwargs)
		"""
		edit = self.period.name 
		regex = re.compile('^(.*)/(.*)/(.*)$')
		match = re.match(regex, edit)
		self.period.name = match.group(3)
		#str(self.rt.rt_name) + '/' + str(self.name) + '/' \
			#+ match.group(3)
		self.period.save()"""

	def __str__(self):
		return self.name

class LogSetManager(models.Manager):

	def duedate(self, logset):
		return (logset.next_time-logset.start_time)/2 + logset.start_time

	def latest_logtime(self, logset):
		logentry_qs = LogEntry.objects.filter(lg_set=logset).order_by('-log_time')
		if not logentry_qs:
			return None
		else:
			return logentry_qs[0].log_time

	def status_update(self, logset,logdef_qs):
		logentry_qs = LogEntry.objects.filter(lg_set=logset)
		this_lgdf_set  = logentry_qs.values_list('lg_def', flat=True)

		due_date = LogSet.objects.duedate(logset)
		latest_logtime = LogSet.objects.latest_logtime(logset)
		newstatus = None

		# True if completed, False if incomplete
		complete = False
		# True if empty, false if non-empty
		empty = False

		if this_lgdf_set.count() == 0:
			empty = True
		elif logdef_qs.count() >= this_lgdf_set.count():

			# if number of LogEntries w/ distinct LogDefs == total number
			# of LogDefs, then the LogSet has all values filled, hence
			# partial = False

			# >= because if there are 5 hourly logdefs, and 10 daily logdefs
			# this_lgdf_set will only have 5 if working with hourly, while
			# logdef_qs will have 15 (5+10). 
			
			complete = True

		if (not empty) and (complete) and (latest_logtime <= due_date):
			# set status to Complete (ontime) (3)
			newstatus = LogSet.COMPLETE
		elif (not empty) and (complete) and (latest_logtime > due_date):
			# set status to Complete (late) (4)
			newstatus = LogSet.COMPLETE_LATE
		elif (empty) and (not complete):
			# set status to missed (full) (0)
			newstatus = LogSet.MISSED
		elif (not empty) and (not complete):
			# set status to missed (partial) (-1)
			newstatus = LogSet.MISSED_PARTIAL
		else:
			raise Exception('something went wrong with status settings')

		return newstatus


class LogSet(models.Model):
	MISSED_PARTIAL = -1
	MISSED = 0
	IN_PROGRESS = 1
	IN_PROGRESS_LATE = 2
	COMPLETE = 3
	COMPLETE_LATE = 4
	Status = (
		(MISSED_PARTIAL, 'Missed (Partial)'),
		(MISSED, 'Missed'),
		(IN_PROGRESS,'In Progress'),
		(IN_PROGRESS_LATE, 'In Progress (Late)'),
		(COMPLETE, 'Complete'),
		(COMPLETE_LATE, 'Complete (Late)')
	)
	#  This represents a 'row' in a log 
	rt = models.ForeignKey(RoundType, on_delete=models.CASCADE, \
						related_name='row')

	# Link the LogDef to the logset with the intermediate being the Entry
	# logdef = models.ManyToManyField(LogDef, through='LogEntry')
	start_time = models.DateTimeField()
	next_time = models.DateTimeField()
	log_time = models.TimeField(null=True, blank=True)
	# 0 is missed, 1 is in-progress, 2 is complete, -1 for something else
	status = models.IntegerField(null=True, choices=Status)
	objects = LogSetManager()
	def __str__(self):
		rt_name = RoundType.objects.get(pk=self.rt.id).rt_name
		return 	"Round Name: " + rt_name \
				+ "\tStart:\t" + str(self.start_time) \
				+ "\tNext:\t" + str(self.next_time) 


class LogEntry(models.Model):
	lg_set = models.ForeignKey(LogSet, on_delete=models.CASCADE)
	
	lg_def = models.ForeignKey(LogDef, on_delete=models.CASCADE)

	parent = models.OneToOneField('self', null=True, blank=True, \
				related_name='prev_edit')
	num_value = models.FloatField(null=True, blank=True)
	select_value = models.TextField(null=True, blank=True)
	note = models.TextField(null=True, blank=True)
	log_time = models.DateTimeField(null=False, blank=False, \
				default=timezone.now)

	def create_flags(self):
		# Create Flags to determine if it is out of bounds
		# If flag exists already toggle the boolean
		self.check_bounds()

		# Create flags determining the Timelyness of the entry
		# Missed and Not Started entries don't exist in DB so
		# they do not have flags. Late flags (0 is not late, 1 is late .
		# In-progress is not-applcable b/c an entry is either completed
		# or has not been started, no such thing so doesnt have flag

		self.check_tardy()

	def check_tardy(self):
		this_logset = self.lg_set
		this_start = self.lg_set.start_time
		this_next = this_logset.next_time
		this_duedate = (this_next - this_start)/2 + this_start
		is_late = 0
		
		note = 'if entry is on-time value=0, if late value=1'
		if (self.log_time > this_duedate):
			is_late = 1

		try:
		   flag_type = FlagTypes.objects.get(flag_name = "Late")
		except FlagTypes.DoesNotExist:
		   flag_type = FlagTypes(flag_name="Late")
		   flag_type.save()

		try:
			exists_already = Flags.objects.get(log_entry=self, flag=flag_type)
		except Flags.DoesNotExist:
			#if doesnt exist, create it
			new_flag=Flags(
				log_entry=self, 
				flag=flag_type, 
				flag_value=is_late,
				note=note
			)
			new_flag.save()
		else:
			#this should never happen, but just in case....
			temp = Flags.objects.get(log_entry=self, flag=flag_type)
			temp.flag_value= is_late
			temp.note=note
			temp.save()





	def check_bounds(self):
		low = self.lg_def.low
		high = self.lg_def.high
		val = self.num_value
		note = 'if inside range value=0,if outside range value=1'
		boolean = 0
		if(val < low or val > high):
			boolean = 1
			
		
		try:
		   flag_type = FlagTypes.objects.get(flag_name = "Outside Range")
		except FlagTypes.DoesNotExist:
		   flag_type = FlagTypes(flag_name = "Outside Range")
		   flag_type.save()

		try:
			exists_already = Flags.objects.get(log_entry=self,flag=flag_type)
		except Flags.DoesNotExist:
			new_flag = Flags(
				log_entry=self, 
				flag=flag_type, 
				flag_value=boolean,
				note=note,
			)
			new_flag.save()
		else:	
			#this should never happen, but just in case
			#if flag exists, update it so that the boolean value is correct
			temp = Flags.objects.get(log_entry = self,flag=flag_type)
			temp.flag_value=boolean
			temp.note=note
			temp.save()
			
		

	def save(self, *args, **kwargs):
		# create next logset if possible
		try:
			self.check_data()
			self.check_unique()
		
		except Exception as inst:
			if (inst.args == ('high',) or inst.args ==('low',)):
				raise ValidationError('Outside of Absolute Range, check your data')
			elif inst.args == ('nuts',):
				raise inst
			else: 
				raise inst
		else:	
			super(LogEntry,self).save(*args,**kwargs)
			self.lg_set.log_time = self.log_time
			self.lg_set.save()
			self.create_flags()

	def check_data(self):
		""" Checks if the data is within the boundaries defined in LogDef.
			Raises Exception if outside the absolute range, 
			If within soft bounds, flag 'outside normal range' is false,
			if outside bounds, flag 'outside normal range' is true """
		low_low = self.lg_def.low_low
		high_high = self.lg_def.high_high
		val = self.num_value
		if low_low and high_high:
			if(val <= low_low):
				raise Exception('low')
			elif (val >= high_high):
				raise Exception('high')

	def check_unique(self):
		is_unique = LogEntry.objects.filter(
			lg_set = self.lg_set,
			lg_def = self.lg_def,
			parent = self.parent,
			num_value = self.num_value,
			select_value = self.select_value,
			note = self.note,
		)
		if is_unique.exists():	
			raise Exception('nuts')
		else:
			pass
	
	def __str__(self):
		if self.parent:
			prev_id = str(self.parent.id)
		else:
			prev_id = 'None'
		return 'LS Id: ' + str(self.lg_set.id) + ' LD Id: '\
				+ str(self.lg_def.id) + ' Prev ID: ' + prev_id

class FlagTypes(models.Model):
	flag_name = models.CharField(max_length=24, null=False, blank=False)

	def __str__(self):
		return self.flag_name

class Flags(models.Model):
	log_entry = models.ForeignKey(LogEntry, on_delete=models.CASCADE, \
					related_name='logentry')
	flag = models.ForeignKey(FlagTypes, on_delete=models.CASCADE,\
					related_name='flagtype')
	flag_value = models.IntegerField(null=False, blank=False)
	note = models.CharField(max_length=50)

	def __str__(self):
		return 'Entry Id: ' + str(self.log_entry.id) + ' FlagType Id: '\
		 		+ str(self.flag.id) + ' name: ' + str(self.flag)