from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from datetime import date, datetime, time, timedelta

# Create your models here.


@python_2_unicode_compatible

class RoundType(models.Model):
	"""This defines a series of columns."""
	rt_name = models.CharField(max_length=50, unique=True)
	rt_desc = models.TextField(max_length=None)
	start_date = models.DateField()
	period = models.IntegerField()

	def create_logsets(self):
		for i in range(0, 24, self.period):
			end_val = 0 if (i + self.period == 24) else (i + self.period)
			
			to_be_added = LogSet(start_time=time(i), end_time=time(end_val),
							log_time=None, rt=self, log_date=self.start_date)
			
			num_results = LogSet.objects.filter(\
				rt=to_be_added.rt, \
				start_time=to_be_added.start_time, \
				end_time=to_be_added.end_time, \
				log_date = to_be_added.log_date).count()
			
			if num_results == 0:
				to_be_added.save()
			else:
				if to_be_added.log_time is not None:
					to_be_added.save()
				else:
					pass
	
	def save(self, *args, **kwargs):
		# looks like if is not needed. kept in just in case...
		super(RoundType, self).save(*args, **kwargs)
		self.create_logsets()

	def __str__(self):
		return self.rt_name


class LogSet(models.Model):
	"""This represents a "row" """
	rt = models.ForeignKey(RoundType, on_delete=models.CASCADE, \
						related_name='row')
	start_time = models.TimeField()
	end_time = models.TimeField()
	log_date = models.DateField()
	log_time = models.TimeField(null=True, blank=True)

	def __str__(self):
		rt_name = RoundType.objects.get(pk=self.rt.id).rt_name
		return 	"Round Name: " + rt_name \
				+ " Date:    "+ str(self.log_date)\
				+ " Start Time:    " + str(self.start_time) \
				+ " End Time:    " + str(self.end_time)

class Selection_value_choices(models.Model):
	choice_name = models.CharField(max_length=24)
	# Default false
	# if true then supply text options
	# if false supply numeric values
	has_qualatative_data = models.BooleanField(default=False)

	units = models.CharField(null=True, max_length=8, blank=True)
	low_low = models.FloatField(null=True, blank=True)
	high_high = models.FloatField(null=True, blank=True)
	low = models.FloatField(null=True, blank=True)
	high = models.FloatField(null=True, blank=True)

	def save(self, *args, **kwargs):
		if (self.has_qualatative_data):
			self.units = None
			self.low_low = None
			self.low = None
			self.high = None
			self.high_high = None

		super(Selection_value_choices,self).save(*args, **kwargs)

	def __str__(self):
		return self.choice_name

class LogDef(models.Model):

	rt = models.ForeignKey(RoundType, on_delete=models.CASCADE,\
							related_name='col')
	#LogSet = models.ForeignKey(LogSet, on_delete=models.CASCADE, \
				#	to_field='LogSet')
	# = models.ManyToManyField(LogSet, related_name='columns')

	LogDef_name = models.CharField(max_length=20)
	
	## Specify the type of input eg:
	## On/Off, Yes/No, Descrpition of Status, Numeric etc
	## Describe Location and activity needed to be taken
	LogDef_desc =  models.TextField(max_length=None)

	LogSet = models.ManyToManyField(LogSet, through='LogEntry')
	## Links to selection value choice
	selection_value = models.ForeignKey(Selection_value_choices,\
						on_delete=models.CASCADE, related_name='selection')

	
	def __str__(self):
		rt_name = RoundType.objects.get(pk=self.rt.id).rt_name
		return "Round Name: " + rt_name + " Col Name: " + self.LogDef_name


	


class LogEntry(models.Model):
	Entry = models.AutoField(primary_key=True)
	
	# LogSet = models.ForeignKey(LogSet, on_delete=models.CASCADE,\
	# 			related_name='xVal')
	# LogDef = models.ForeignKey(LogDef, on_delete=models.CASCADE,\
	# 					related_name='yVal')
	LogSet = models.ForeignKey(LogSet, on_delete=models.CASCADE)
	LogDef = models.ForeignKey(LogDef, on_delete=models.CASCADE)

	num_value = models.FloatField(null=True, blank=True)
	select_value = models.TextField(null=True, blank=True)
	note = models.TextField(null=True, blank=True)
	log_time = models.TimeField(null=False, blank=False, \
				default=datetime.time(datetime.now()))
	log_date = models.DateField(null=False, blank=False,\
				default=timezone.now)
	irregular_data = models.BooleanField(default=False)
	anachronistic_entry = models.BooleanField(default=False)
	
	def save(self, *args, **kwargs):
		irregular_value = False
		anachronistic = False
		try:
			irregular_value = self.has_irreg_data()
			anachronistic = self.check_anachron()
		except Exception as e:
			raise e
			#raise Exception("SelectionValue does not have range constraints"+
			#				"when range constraints were expected")
		else:
			# no errors so set the logtime of the LogSet
			self.set_logtime()

			if (self.has_qual_data()):
				self.num_value = None
			else:
				self.select_value = None

			self.irregular_data = irregular_value
			self.anachronistic_entry = anachronistic
			super(LogEntry, self).save(*args, **kwargs)

	def check_anachron(self):
		answer = False
		lset = LogSet.objects.get(pk=self.LogSet.id)
		this_logtime = self.log_time
		this_logdate = self.log_date
		expected_logdate = lset.log_date
		expected_logtime_s = lset.start_time
		expected_logtime_e = lset.end_time
		if(this_logdate != expected_logdate):
			answer = True
		elif (this_logtime < expected_logtime_s) or \
				(this_logtime > expected_logtime_e):
				answer = True
		return answer

	def has_qual_data(self):
		ld_obj = LogDef.objects.get(pk=self.LogDef.id)
		sv = Selection_value_choices.objects.get(pk=ld_obj.selection_value.id)
		return sv.has_qualatative_data
		
			

	def has_irreg_data(self):
		irregular_data = False
		num_value = self.num_value
		ld_obj = LogDef.objects.get(pk=self.LogDef.id)
		sv = Selection_value_choices.objects.get(pk=ld_obj.selection_value.id)
		if (sv.has_qualatative_data):
			self.num_value is None
		else:
			self.select_value is None

		if self.num_value is None:
			# for qualatative data
			pass
		elif (self.select_value is None) or (self.select_value ==""):
			# for quantatative data check if it is within bounds
			try:
				low_low = sv.low_low
				high_high = sv.high_high
				low = sv.low
				high = sv.high
			except AttributeError as ae:
				print ae
				raise Exception("Field not present in current" +\
								"selection value for logdef")
			else:
				if (num_value > high_high) or (num_value < low_low):
					raise Exception("num_value out of absolute bounds")
				elif (num_value <= low) or (num_value >= high):
					irregular_data = True
				else:
					pass
		else:
			pass
		return irregular_data


	def set_logtime(self):
		id_changethis = self.LogSet.id
		curr = LogSet.objects.get(pk=id_changethis)
		curr.log_time = self.log_time
		curr.save()

	def __str__(self):
		str1 = str(self.num_value)
		str2 = self.select_value
		if (str1 is None) or (str1 == "None"):
			str1 = "no num_value"
		else:
			pass
		if (str2 is None) or (str2 is ""):
			str2 = "no qual_value"
		else:
			pass
		lgst = LogSet.objects.get(pk=self.LogSet.id)
		start_time = lgst.start_time
		end_time = lgst.end_time
		lgdf_name = LogDef.objects.get(pk=self.LogDef.id).LogDef_name
		rt_name = RoundType.objects.get(pk=lgst.rt.id).rt_name
		return  ("Round_Name: "+ rt_name + "__Attribute: " + lgdf_name 
				+ "__Start: " + str(start_time) + "__End: " + str(end_time)
				+ "__Num_val: " + str1 + "__Qual_val: " + str2)

	class Meta:
		ordering = ['-log_time']


	
	

