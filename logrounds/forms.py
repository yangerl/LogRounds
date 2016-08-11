from django import forms
from django.contrib.admin import widgets
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
        fields = ('rt_name', 'period', 'rt_desc', 'start_date','phase_days', 'phase_hours', "phase_min")

class DataGridForm(forms.Form):
    start_date = forms.DateField(
        label='Starting Date:',

    )
    start_time = forms.TimeField(
        label = 'Starting Time:',
    )
    widgets = {
        'start_date': forms.DateInput()
    }




class PeriodForm(forms.ModelForm):
    MY_CHOICES = (
        ('d', 'Days'),
        ('h', 'Hours'),
        ('m', 'Minutes'),
    )
    unit = forms.ChoiceField(choices=MY_CHOICES)
    class Meta:
        model = Period
        fields = ('name', 'scale','unit', )


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
