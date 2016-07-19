from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from datetime import date, datetime, time, timedelta
import re

# Create your models here.


@python_2_unicode_compatible

class RoundType(models.Model):
		""" This defines a series of columns. """
		rt_name = models.CharField(max_length=50, unique = True)

		#describe the purpose of the round etc.
		rt_desc = models.TextField(max_length=None)
		start_date = models.DateTimeField()

		def __str__(self):
			return self.rt_name

class Period (models.Model):
	""" TThis defines the periodicity of the Round """
	name = models.CharField(max_length=12)
	scale = models.IntegerField(null=False, blank=False)
	unit = models.CharField(max_length=10)
	phase = models.CharField(max_length=12)

	def parse_period(self):
		lower = self.unit.lower()
		if (lower == 'day'or lower =='d'):
			return timedelta(self.scale)
		elif (lower =='hour' or lower =='h'):
			return timedelta(0,0,0,0,0,self.scale)
		elif (lower =='minutes' or lower =='min' \
				or lower =='m'):
			return timedelta(0,0,0,0,scale,0)
		else:
			raise Exception ("uncaught unit type")


	def parse_phase(self):
		regex = re.compile('^([0-9]+)d,([0-9]+)h,([0-9]+)m?$')
		match = regex.match(self.phase)
		# timedelta([days[,sec[,micro[,mill[,min[,hour[,weels]]]]]]])
		days = match.group(1)
		hours = match.group(2)
		mins = match.group(3)

		phase = timedelta(int(days),0,0,0,int(mins),int(hours))
		return phase

	def __str__(self):
		return self.name


class LogSet(models.Model):
	""" This represents a 'row' in a log """
	rt = models.ForeignKey(RoundType, on_delete=models.CASCADE, \
						related_name='row')

	parent_ls = models.OneToOneField('self', null=True, blank=True, related_name='parent')

	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	log_time = models.TimeField(null=True, blank=True)

	def __str__(self):
		rt_name = RoundType.objects.get(pk=self.rt.id).rt_name
		return 	"Round Name: " + rt_name \
				+ " Start Time:    " + str(self.start_time) \
				+ " End Time:    " + str(self.end_time)


class LogDef(models.Model):
	""" This represents a 'column' of data """
	rt = models.ForeignKey(RoundType, on_delete=models.CASCADE,\
			related_name = 'col')
	# This is the frequency to generate new LogSets
	period = models.ForeignKey(Period, on_delete = models.CASCADE,\
			related_name = 'prd')
	name = models.CharField(max_length=20)

	# Give info about the data being collected, location, safety etc.
	desc = models.TextField(max_length=None)

	# Link the LogDef to the logset with the intermediate being the Entry
	logset = models.ManyToManyField(LogSet, through='LogEntry')

	is_qual_data = models.BooleanField(default=False)
	units = models.CharField(null=True, max_length=8, blank=True)
	# units might be moved to 'data types class'
	low_low = models.FloatField(null=True, blank=True)
	high_high = models.FloatField(null=True, blank=True)
	low = models.FloatField(null=True, blank=True)
	high = models.FloatField(null=True, blank=True)

	def create_first_logset(self):
		# to do this we need to check if there is alreay a Logset in existence
		# Perform this step first.

		logsets = LogSet.objects.filter(rt=self.rt)
		# if empty create new LogSet
		if (not logsets): # python 'style' for checking empty list
			start_time = self.rt.start_date + self.period.parse_phase()
			end_time = start_time + self.period.parse_period()

			first_logset = LogSet(rt=self.rt, parent_ls=None,\
									start_time = start_time,\
									end_time = end_time,\
									log_time = None)
			first_logset.save()

	def save(self,  *args, **kwargs):
		# we need to create the first LogSet that is the parent to all the data
		self.create_first_logset()
		super(LogDef, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class LogEntry(models.Model):
	lg_set = models.ForeignKey(LogSet, on_delete=models.CASCADE)
	lg_def = models.ForeignKey(LogDef, on_delete=models.CASCADE)

	parent = models.OneToOneField('self', null=True, blank=True, \
				related_name='prev_edit')
	num_value = models.FloatField(null=True, blank=True)
	select_value = models.TextField(null=True, blank=True)
	note = models.TextField(null=True, blank=True)
	log_time = models.DateTimeField(null=False, blank=False, \
				default=datetime.now())


	def check_data(self):
		""" Checks if the data is within the boundaries defined in LogDef.
			Raises Exception if outside the absolute range, 
			If within soft bounds, flag 'outside normal range' is false,
			if outside bounds, flag 'outside normal range' is true """
		low_low = self.lg_def.low_low
		high_high = self.lg_def.high_high
		val = self.num_value

		if(val <= low_low):
			raise Exception('low')
		elif (val >= high_high):
			raise Exception('high')
	

	def create_flags(self):
		low = self.lg_def.low
		high = self.lg_def.high
		val = self.num_value
		# for outside range
		boolean = 0
		if(val < low or val > high):
			boolean = 1

		flag_type = FlagTypes.objects.get(flag_name = "Outside Range")
		exists_already = Flags.objects.filter(log_entry = self,flag=flag_type)
		if (not exists_already):
			new_flag = Flags(log_entry=self, flag=flag_type, flag_value=boolean)
			new_flag.save()
		else:
			temp = Flags.objects.get(log_entry = self,flag=flag_type)
			temp.flag_value=boolean
			temp.save()

	def create_next_logset (self):
		""" If this logset already has a child do nothing, if it doesnt create
			The logset may already have a child if a LogEntry for a different
			LogDef has already been created. If one hasnt been then a new logset
			A must be created for the next set of entries!! """

		is_parent = LogSet.objects.filter(parent_ls=self.lg_set)
		if (not is_parent):
			time_delta = self.lg_def.period.parse_period()
			new_logset = LogSet(rt=self.lg_set.rt,\
								parent_ls=self.lg_set,\
								start_time=self.lg_set.end_time,\
								end_time=self.lg_set.end_time+time_delta,\
								log_time=None)
			new_logset.save()


	def save(self, *args, **kwargs):
		# create next logset if possible
		try:
			self.check_data()
		except Exception as inst:
			if (inst.args == 'high' or inst.args =='low'):
				raise Exception('Outside of Absolute Range, check your data')
			else: 
				raise inst
		else:	
			self.create_next_logset()
			super(LogEntry,self).save(*args,**kwargs)
			self.create_flags()	

	def __str__(self):
		return 'LogSet Id: ' + str(self.lg_set.id) + ' LogDef Id: '\
				+ str(self.lg_def.id)

class FlagTypes(models.Model):
	LogEntry = models.ManyToManyField(LogEntry, through="Flags")
	flag_name = models.CharField(max_length=24, null=False, blank=False)

	def __str__(self):
		return self.flag_name

class Flags(models.Model):
	log_entry = models.ForeignKey(LogEntry, on_delete=models.CASCADE, \
					related_name='logentry')
	flag = models.ForeignKey(FlagTypes, on_delete=models.CASCADE,\
					related_name='flagtype')
	flag_value = models.IntegerField(null=False, blank=False)

	def __str__(self):
		return 'Entry Id: ' + str(self.log_entry.id) + ' FlagType Id: '\
		 		+ str(self.flag.id) + ' name: ' + str(self.flag)