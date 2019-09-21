from django import forms
from firm.models import Worksite, Subcontractor, Contract
from .models import Discovery, Analysis, AnalysisDetail, Progress, Synopsis

class DateInput(forms.DateInput):
    input_type = 'date'
    

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['detail','profit','material','workmanship','overheads','tender','year','note']
    
    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['material'].widget.attrs['readonly'] = True
            self.fields['workmanship'].widget.attrs['readonly'] = True
            self.fields['overheads'].widget.attrs['readonly'] = True
            self.fields['tender'].widget.attrs['readonly'] = True
        
            


class AnalysisDetailForm(forms.ModelForm):
    class Meta:
        model = AnalysisDetail
        fields = ['category','definition','amount','price','total']



# KEŞİF FORM
class DiscoveryForm(forms.ModelForm):
    class Meta:
        model = Discovery
        fields = ['worksite','no','name','unit','amount','price','total']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DiscoveryForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
    

# HAKEDİŞ FORM
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['worksite','employer','subcontractor','no','date','cumulative','acquisition','additional','total','previous_amount','this_amount','vat','progress_amount','total_warrant','previous_warrant','this_warrant','total_advance','previous_advance','this_advance','total_stoppage','previous_stoppage','this_stoppage','total_tax_cut','previous_tax_cut','this_tax_cut','total_penalty','previous_penalty','this_penalty','total_deduction','previous_deduction','this_deduction','amount_paid']
        widgets = {
            'date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProgressForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['no'].widget.attrs['readonly'] = True
            self.fields['total'].widget.attrs['readonly'] = True
            self.fields['this_amount'].widget.attrs['readonly'] = True
            self.fields['progress_amount'].widget.attrs['readonly'] = True
            self.fields['total_warrant'].widget.attrs['readonly'] = True
            self.fields['this_warrant'].widget.attrs['readonly'] = True
            self.fields['total_advance'].widget.attrs['readonly'] = True
            self.fields['this_advance'].widget.attrs['readonly'] = True
            self.fields['total_stoppage'].widget.attrs['readonly'] = True
            self.fields['this_stoppage'].widget.attrs['readonly'] = True
            self.fields['total_tax_cut'].widget.attrs['readonly'] = True
            self.fields['this_tax_cut'].widget.attrs['readonly'] = True
            self.fields['this_penalty'].widget.attrs['readonly'] = True
            self.fields['this_deduction'].widget.attrs['readonly'] = True
            self.fields['amount_paid'].widget.attrs['readonly'] = True
            self.fields['previous_amount'].widget.attrs['readonly'] = True
            self.fields['previous_warrant'].widget.attrs['readonly'] = True
            self.fields['previous_advance'].widget.attrs['readonly'] = True
            self.fields['previous_stoppage'].widget.attrs['readonly'] = True
            self.fields['previous_tax_cut'].widget.attrs['readonly'] = True
            self.fields['previous_penalty'].widget.attrs['readonly'] = True
            self.fields['previous_deduction'].widget.attrs['readonly'] = True
            self.fields['cumulative'].widget.attrs['readonly'] = True


class SynopsisForm(forms.ModelForm):
    class Meta:
        model = Synopsis
        fields = ['progress','pose_no','name','unit','unit_price','total_quantity','previous_quantity','this_quantity','total_price','previous_price','this_price']

    def __init__(self, *args, **kwargs):
        super(SynopsisForm, self).__init__(*args, **kwargs)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['pose_no'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['unit'].widget.attrs['readonly'] = True
            self.fields['unit_price'].widget.attrs['readonly'] = True
            self.fields['previous_quantity'].widget.attrs['readonly'] = True
            self.fields['this_quantity'].widget.attrs['readonly'] = True
            self.fields['previous_price'].widget.attrs['readonly'] = True
            self.fields['this_price'].widget.attrs['readonly'] = True