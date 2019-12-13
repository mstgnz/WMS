from django import forms
from firm.models import Worksite
from .models import Minutes, Writing


class DateInput(forms.DateInput):
    input_type = 'date'


# TUTANAK FORM
class MinutesForm(forms.ModelForm):
    class Meta:
        model = Minutes
        fields = ['worksite','no','subject','note','date','labor_cost','material_cost','total_cost','file','status']
        widgets = {
            'date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MinutesForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['worksite'].disabled = True


# ÜST YAZI FORM
class WritingForm(forms.ModelForm):
    class Meta:
        model = Writing
        fields = ['worksite','no','subject','note','date','file']
        widgets = {
            'date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WritingForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['worksite'].disabled = True
