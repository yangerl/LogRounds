from django import forms
from django.contrib.admin import widgets
from .models import *

class RoundTypeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(RoundTypeForm, self).clean()
        pd = cleaned_data.get("period")
        name = cleaned_data.get("name")
        try:
            exists_already = RoundType.objects.get(
                name=name,
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
        fields = ('name', 'period', 'desc', 'start_date','phase_days', 'phase_hours', "phase_min")


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
        ('Days', 'Days'),
        ('Hours', 'Hours'),
        ('Minutes', 'Minutes'),
    )
    unit = forms.ChoiceField(choices=MY_CHOICES)
    class Meta:
        model = Period
        fields = ('name', 'scale','unit', )



class LogDefForm(forms.ModelForm):
    def clean_units(self):
        is_q = self.cleaned_data['is_qual_data']
        data = self.cleaned_data['units']
        if is_q:
            return None
        else:
            return data

    def clean_low_low(self):
        is_q = self.cleaned_data['is_qual_data']
        data = self.cleaned_data['low_low']
        if is_q:
            return None
        else:
            return data

    def clean_high_high(self):
        is_q = self.cleaned_data['is_qual_data']
        data = self.cleaned_data['high_high']
        if is_q:
            return None
        else:
            return data

    def clean_low(self):
        is_q = self.cleaned_data['is_qual_data']
        data = self.cleaned_data['low']
        if is_q:
            return None
        else:
            return data

    def clean_high(self):
        is_q = self.cleaned_data['is_qual_data']
        data = self.cleaned_data['high']
        if is_q:
            return None
        else:
            return data

    def clean(self):
        cleaned_data = super(LogDefForm, self).clean()
        is_q = cleaned_data.get('is_qual_data')
        if is_q:
            # check that all the other ones are None
            if cleaned_data.get('units') is None and \
                cleaned_data.get('low_low') is None and \
                cleaned_data.get('high_high') is None and \
                cleaned_data.get('low') is None and \
                cleaned_data.get('high') is None:
                pass
            else:
                raise forms.ValidationError('The for fields should be None, but isnt')
        else:
            if cleaned_data.get('units') is not None and \
                cleaned_data.get('low_low') is not None and \
                cleaned_data.get('high_high') is not None and \
                cleaned_data.get('low') is not None and \
                cleaned_data.get('high') is not None:
                
                if not (cleaned_data.get('low_low') 
                    <= cleaned_data.get('low') 
                    <= cleaned_data.get('high') 
                    <= cleaned_data.get('high_high')):
                    raise forms.ValidationError('The range is incorrect')
            else:
                raise forms.ValidationError('The for fields should be not None')



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
