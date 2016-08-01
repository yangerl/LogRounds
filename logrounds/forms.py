from django import forms

from .models import *

class RoundTypeForm(forms.ModelForm):
	def clean(self):
		cleaned_data = super(RoundTypeForm, self).clean()
		pd = cleaned_data.get("period")
		name = cleaned_data.get("rt_name")
		try:
			exists_already = RoundType.objects.get(
				rt_name=name,
				period=pd,
			)
		except RoundType.DoesNotExist:
			pass
		else:
			raise forms.ValidationError(
				"This Round name and Period is not unique. \n"
				"If you are try adding LogDefs to this existing round "
				"or create a new round with a different period"
			)

	class Meta:
		model = RoundType
		fields = ('rt_name', 'period', 'rt_desc', 'start_date')

class PeriodForm(forms.ModelForm):
	BAD_LIFE_CHOICES = (
		('Days', 'd'),
		('Hours', 'h'),
		('Minutes', 'm'),
	)
	scale = models.CharField(max_length=5, choices=BAD_LIFE_CHOICES)
	class Meta:
		model = Period
		fields = ('name', 'scale','unit', 'phase_days', 'phase_hours', "phase_min")


class LogDefForm(forms.ModelForm):
	class Meta:
		model = LogDef
		fields = ('rt','name','desc','is_qual_data',\
					'units','low_low','high_high','low','high')
		widgets = {
			'rt': forms.HiddenInput(),
		}

class LogEntryForm(forms.ModelForm):
	
	class Meta:
		model = LogEntry
		fields = ('lg_set','lg_def','parent','log_time','num_value'\
			, 'select_value', 'note')
		widgets = {
			'lg_set': forms.HiddenInput(),
			'lg_def': forms.HiddenInput(),
			'parent': forms.HiddenInput(),
			'log_time': forms.HiddenInput(),
		}
