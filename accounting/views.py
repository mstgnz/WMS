import calendar
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
from user.models import User
from firm.models import Worksite, Subcontractor
from worksite.custom import get_or_none
from .models import Waybill, WaybillMaterial, Worker, Tally, Order, OrderMaterial
from .forms import WaybillForm, WaybillMaterialForm, WorkerForm, TallyForm, OrderForm, OrderMaterialForm


# ANASAYFA
class IndexView(TemplateView):
    template_name = 'accounting/index.html'


# İRSALİYE
class WaybillCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/waybill_add.html'
    permission_required = 'accounting.add_waybill'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            if Waybill.objects.filter(vendor=request.POST.get('vendor'),waybill_no=request.POST.get('waybill_no')).exists():
                messages.warning(request, '{} ait {} nolu irsaliye zaten kayıtlı!'.format(request.POST.get('vendor'),request.POST.get('waybill_no')))
            else:
                obj = context["form"].save()
                name = request.POST.getlist('name[]')
                unit = request.POST.getlist('unit[]')
                amount = request.POST.getlist('amount[]')
                price = request.POST.getlist('price[]')
                total = request.POST.getlist('total[]')
                for i in range(len(name)):
                    WaybillMaterial.objects.create(waybill_id=obj.pk, name=name[i], unit=unit[i], amount=amount[i], price=price[i], total=total[i])
                messages.success(request, 'İrsaliye Kaydı Yapıldı!')
                return redirect('/accounting/waybill/add/')
        return super(WaybillCreateView, self).render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(WaybillCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = WaybillForm(self.request.POST or None, user=self.request.user)
        context['title'] = 'Waybill Create'
        return context


# İRSALİYE LİSTE
class WaybillListView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/waybill_list.html'
    permission_required = 'accounting.view_waybill'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Waybill.objects.filter(worksite__in=Worksite.objects.filter(pk=self.request.POST.get('worksite'))))
            return JsonResponse(data, safe=False)
        
    def get_context_data(self, *args, **kwargs):
        context = super(WaybillListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Waybill List'
        context['form'] = WaybillForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        return context


# İRSALİYE DETAY
class WaybillDetailView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/waybill_detail.html'
    permission_required = 'accounting.view_waybill'

    def get_context_data(self, *args, **kwargs):
        context = super(WaybillDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Waybill Update'
        context['waybill'] = WaybillForm(self.request.POST or None, instance=get_or_none(Waybill, pk=self.kwargs['pk']))
        context['materials'] = WaybillMaterial.objects.filter(waybill=self.kwargs['pk'])
        return context


# Worksite.objects.get(pk=Contract.objects.get(pk=Discovery.objects.get(pk=self.kwargs['pk']).contract.pk).worksite.pk)


# İDARİ İŞLER ANA SAYFA
class AdministrativeView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/administrative.html'
    permission_required = 'accounting.view_waybill'


# İŞÇİ GİRİŞİ
class WorkerCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = WorkerForm
    template_name = 'form.html'
    success_url = '/accounting/worker/create/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'accounting.add_worker'
    redirect_field_name = '/accounting/worker/create/'

    def get_context_data(self, *args, **kwargs):
        context = super(WorkerCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Worker Create'
        context['form'] = WorkerForm(user=self.request.user)
        return context


# İŞÇİ LİSTE
class WorkerListView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/worker_list.html'
    permission_required = 'accounting.view_worker'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            if self.request.POST.get('type') == 'sub_select':
                data = {
                    'sub' : serializers.serialize('json', Subcontractor.objects.filter(worksite=self.request.POST.get('worksite')))
                }
            else:
                data = {
                    'worker' : serializers.serialize('json', Worker.objects.filter(worksite=self.request.POST.get('worksite'), subcontractor=self.request.POST.get('subcontractor')))
                }
            return JsonResponse(data, safe=False)
        
    def get_context_data(self, *args, **kwargs):
        context = super(WorkerListView, self).get_context_data(*args, **kwargs)
        context['worksites'] = self.request.user.worksite.filter(active=True) # Şantiye listesi bu şekilde kullanıcı üzerinden yapılmalıdır.
        return context


# İŞÇİ GÜNCELLE
class WorkerUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = 'form.html'
    success_url = '/accounting/worker/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'accounting.change_worker'

    # url adresinden id değiştirilirse diye kontrolü sağlanıyor.
    def get(self, *args, **kwargs):
        worker = Worker.objects.get(pk=self.kwargs['pk'])
        if worker.subcontractor not in Subcontractor.objects.filter(worksite__in=self.request.user.worksite.filter(active=True)):
            return redirect('/')
        return super(WorkerUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(WorkerUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Worker Update'
        context['form'] = WorkerForm(user=self.request.user, instance=Worker.objects.get(pk=self.kwargs['pk']))
        return context


# PUANTAJ
class TallyCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/tally_add.html'
    permission_required = 'accounting.add_tally'
   
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            if self.request.POST.get('type') == 'sub_select':
                data = {
                    'sub' : serializers.serialize('json', Subcontractor.objects.filter(worksite=self.request.POST.get('worksite')))
                }
            else:
                # input_date ve output_date göre işçiler listelenecektir. çıkış tarihi olmayanlar için iki ayrı queryset oluşturularak birleştirildi.
                output_date = Worker.objects.filter(
                    worksite=self.request.POST.get('worksite'), 
                    subcontractor=self.request.POST.get('subcontractor'),
                    input_date__year__lte=self.request.POST.get('year'),
                    input_date__month__lte=self.request.POST.get('month'),
                    output_date__isnull=False,
                    output_date__year__gte=self.request.POST.get('year'),
                    output_date__month__gte=self.request.POST.get('month')
                )
                output_date_isnull = Worker.objects.filter(
                    worksite=self.request.POST.get('worksite'), 
                    subcontractor=self.request.POST.get('subcontractor'),
                    input_date__year__lte=self.request.POST.get('year'),
                    #input_date__month__lte=self.request.POST.get('month'),
                    output_date__isnull=True
                )
                worker_filter = output_date | output_date_isnull
                data = {
                    'worker' : serializers.serialize('json', worker_filter.distinct()),
                    # kayıtlı puantaj forma doldurulacaktır. yıl ve aya göre filtrelenecektir.
                    'tally' : serializers.serialize('json', Tally.objects.filter(worker__in=self.request.POST.getlist('worker[]'), year=self.request.POST.get('year'), month=self.request.POST.get('month')))
                }
            return JsonResponse(data, safe=False)

        # GET POST
        year = request.POST.get('year')
        month = request.POST.get('month')
        worker = request.POST.getlist('worker[]')
        wage = request.POST.getlist('wage[]')
        permit = request.POST.getlist('permit[]')
        sunday = request.POST.getlist('sunday[]')
        overtime = request.POST.getlist('overtime[]')
        notch = request.POST.getlist('notch[]')
        shift = request.POST.getlist('shift[]')
        # ay kaç gün çekiyor.
        get_day = calendar.monthrange(int(year),int(month))[1]
        # kayıt yapıalacak
        a = 0
        row = get_day
        for i in range(len(worker)):
            if(Tally.objects.filter(worker_id=worker[i], year=year, month=month)).exists():
                Tally.objects.filter(worker_id=worker[i], year=year, month=month).update(wage=wage[i], permit=permit[i], overtime=overtime[i], sunday=sunday[i], notch=','.join(notch[a:row]), shift=','.join(shift[a:row]))
            else:
                Tally.objects.create(worker_id=worker[i], year=year, month=month, wage=wage[i], permit=permit[i], overtime=overtime[i], sunday=sunday[i], notch=','.join(notch[a:row]), shift=','.join(shift[a:row]))
            a=row
            row+=get_day
        messages.success(request, 'Pauntaj Kaydı Yapıldı')
        return super(TallyCreateView, self).render_to_response(context)
        
    def get_context_data(self, *args, **kwargs):
        context = super(TallyCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = TallyForm(user=self.request.user)
        context['worksites'] = self.request.user.worksite.filter(active=True) # Şantiye listesi bu şekilde kullanıcı üzerinden yapılmalıdır.
        return context


# PUANTAJ LİSTE
class TallyListView(ListView):
    template_name = 'accounting/tally_list.html'
    context_object_name = "tallies"

    def get_queryset(self):
        return Tally.objects.filter(worker__in=Worker.objects.filter(subcontractor__in=Subcontractor.objects.filter(worksite__in=self.request.user.worksite.filter(active=True))))


# PUANTAJ GÜNCELLE
class TallyUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tally
    form_class = TallyForm
    template_name = 'form.html'
    success_url = '/accounting/worker/tally/list'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'accounting.change_tally'

    # url adresinden id değiştirilirse diye kontrolü sağlanıyor.
    def get(self, *args, **kwargs):
        worker = Tally.objects.get(pk=self.kwargs['pk'])
        if worker.subcontractor not in Subcontractor.objects.filter(worksite__in=self.request.user.worksite.filter(active=True)):
            return redirect('/')
        return super(TallyUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TallyUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Tally Update'
        context['form'] = TallyForm(user=self.request.user, instance=Tally.objects.get(pk=self.kwargs['pk']))
        return context


# SİPARİŞ ANASAYFA
class OrderView(TemplateView):
    template_name = 'accounting/order.html'


# SİPARİŞ
class OrderCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/order_add.html'
    permission_required = 'accounting.add_order'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            obj = context["form"].save()
            order = Order.objects.get(pk=obj.pk)
            name = request.POST.getlist('name[]')
            unit = request.POST.getlist('unit[]')
            amount = request.POST.getlist('amount[]')
            for i in range(len(name)):
                OrderMaterial.objects.create(order=order, name=name[i], unit=unit[i], amount=amount[i])
            messages.success(request, 'Sipariş Kaydı Yapıldı!')
            return redirect('/accounting/order/list/')
        return super(OrderCreateView, self).render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(OrderCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = OrderForm(self.request.POST or None, user=self.request.user)
        context['title'] = 'Siperiş Ekle'
        return context


# SİPARİŞ LİSTE
class OrderListView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/order_list.html'
    permission_required = 'accounting.view_order'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Order.objects.filter(worksite__in=Worksite.objects.filter(pk=self.request.POST.get('worksite'))))
            return JsonResponse(data, safe=False)
        
    def get_context_data(self, *args, **kwargs):
        context = super(OrderListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Sipariş Liste'
        context['form'] = OrderForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        return context


# SİPARİŞ DETAY
class OrderDetailView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounting/order_detail.html'
    permission_required = 'accounting.view_order'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Sipariş Güncelle'
        context['order'] = OrderForm(self.request.POST or None, instance=get_or_none(Order, pk=self.kwargs['pk']))
        context['materials'] = OrderMaterial.objects.filter(order=self.kwargs['pk'])
        return context