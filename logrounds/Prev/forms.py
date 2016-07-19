from django import forms

from .models import *

class RoundTypeForm(forms.ModelForm):

	class Meta:
		model = RoundType
		fields = ('rt_name', 'rt_desc', 'start_date')

class PeriodForm(forms.ModelForm):
	class Meta:
		model = Period
		fields = ('name', 'scale','unit', 'phase')


class LogDefForm(forms.ModelForm):

	class Meta:
		model = LogDef
		fields = ('rt','period','name','desc','is_qual_data',\
					'units','low_low','high_high','low','high')