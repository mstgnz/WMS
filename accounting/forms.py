from django import forms
from firm.models import Worksite, Subcontractor
from .models import Waybill, WaybillMaterial, Worker, Tally, Order, OrderMaterial


class DateInput(forms.DateInput):
    input_type = 'date'


# İRSALİYE FORM
class WaybillForm(forms.ModelForm):
    class Meta:
        model = Waybill
        fields = ['worksite','vendor','waybill_no','date_of_issue','date_of_shipment','invoice_no','consigner','recipient','note']
        widgets = {
            'date_of_issue': DateInput(),
            'date_of_shipment': DateInput()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WaybillForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['worksite'].disabled = True



# İRSALİYE MATERIAL FORM
class WaybillMaterialForm(forms.ModelForm):
    class Meta:
        model = WaybillMaterial
        fields = ['waybill','name','unit','amount','price','total']

    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user', None)
        super(WaybillMaterialForm, self).__init__(*args, **kwargs)
        #if self.user:
        #    self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['waybill'].disabled = True


# İŞÇİ FORM
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['worksite','subcontractor','full_name','title','phone','input_date','output_date','id_number','mother_name','father_name','place_of_birth','birth_date','marital_status']
        widgets = {
            'input_date': DateInput(),
            'output_date': DateInput(),
            'birth_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WorkerForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
            self.fields['subcontractor'].queryset = Subcontractor.objects.filter(worksite__in=self.user.worksite.filter(active=True))
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['id_number'].disabled = True
            self.fields['worksite'].disabled = True
            self.fields['subcontractor'].disabled = True


# PUANTAJ FORM
class TallyForm(forms.ModelForm):
    class Meta:
        model = Tally
        fields = ['worker','year','month','wage','permit','overtime','sunday','notch','shift']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TallyForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worker'].queryset = Worker.objects.filter(subcontractor__in=Subcontractor.objects.filter(worksite__in=self.user.worksite.filter(active=True)))
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['worker'].widget.attrs['readonly'] = True
            self.fields['year'].widget.attrs['readonly'] = True
            self.fields['month'].widget.attrs['readonly'] = True
            self.fields['wage'].widget.attrs['readonly'] = True
            self.fields['permit'].widget.attrs['readonly'] = True
            self.fields['overtime'].widget.attrs['readonly'] = True
            self.fields['sunday'].widget.attrs['readonly'] = True            


# SİPARİŞ FORM
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['worksite','orderer','deadline','note','status']
        widgets = {
            'deadline': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['worksite'].queryset = self.user.worksite.filter(active=True)
            self.fields['orderer'].initial  = self.user.get_full_name
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['orderer'].disabled = True
        if instance.pk:
            self.fields['worksite'].disabled = True




# SİPARİŞ MATERIAL FORM
class OrderMaterialForm(forms.ModelForm):
    class Meta:
        model = OrderMaterial
        fields = ['order','name','unit','amount']

    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user', None)
        super(OrderMaterialForm, self).__init__(*args, **kwargs)
        # INSTANCE
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['order'].disabled = True