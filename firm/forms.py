from django import forms
from .models import Firm, Worksite, Subcontractor, Contract, Specification, Project

class DateInput(forms.DateInput):
    input_type = 'date'
    

# FİRMA FORM
class FirmForm(forms.ModelForm):
    class Meta:
        model = Firm
        fields = ['tax','name','full_name','phone','fax','web','email','address','image']

    def __init__(self, *args, **kwargs):
        super(FirmForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].disabled = True
            self.fields['tax'].disabled = True


# ŞANTİYE FORM
class WorksiteForm(forms.ModelForm):
    class Meta:
        model = Worksite
        fields = ['name','employer','name_of_job','control','construction_area','threader_no','island_no','parcel_no','phone','fax','address','image','start_date','end_date','active']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(WorksiteForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].disabled = True
                                

# TAŞERON FORM
class SubcontractorForm(forms.ModelForm):
    class Meta:
        model = Subcontractor
        fields = ['worksite','name','email','phone','subject','address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SubcontractorForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].disabled = True


# SÖZLEŞME FORM
class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['worksite','category','no','date','name','price','guarantee','advance','progress','note','file']
        widgets = {
            'date': DateInput(),
            'file': forms.FileInput(attrs={'accept': '.pdf'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContractForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
            # Seçim listesini manuel ayarlamak için kullanılır
            #worksites = [(i.id, i.name) for i in self.user.worksite.filter(active=True)]
            #self.fields['worksite'] = forms.ChoiceField(choices=worksites)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['worksite'].disabled = True
       

# ŞARTNAME FORM
class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ['contract','name','file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SpecificationForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['contract'].queryset = Contract.objects.filter(worksite__in=self.user.worksite.filter(active=True))


# PROJE FORM
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['worksite','no','date','name','category','file']
        widgets = {
            'date': DateInput(),
            'file': forms.FileInput(attrs={'accept': '.dwg'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)

