from django import forms

from .models import *

class RoundTypeForm(forms.ModelForm):

	class Meta:
		model = RoundType
		fields = ('rt_name', 'rt_desc', 'start_date')

class PeriodForm(forms.ModelForm):
	class Meta:
		model = Period
		fields = ('name', 'scale','unit', 'phase_days', 'phase_hours', "phase_min")


class LogDefForm(forms.ModelForm):
	class Meta:
		model = LogDef
		fields = ('rt','period','name','desc','is_qual_data',\
					'units','low_low','high_high','low','high')

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
