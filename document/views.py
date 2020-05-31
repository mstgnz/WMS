import datetime
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from user.models import User
from .models import Minutes, Writing, DailyReport
from .forms import MinutesForm, WritingForm
from firm.models import Worksite

# RAPOR ANASAYFA
class IndexView(TemplateView):
    template_name = 'document/minutes.html'

# TUTANAK ANASAYFA
class MinutesView(TemplateView):
    template_name = 'document/minutes.html'

# TUTANAK EKLE
class MinutesCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MinutesForm
    template_name = 'document/minutes_add.html'
    success_url = '/document/minutes/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'document.add_minutes'

    def get_context_data(self, *args, **kwargs):
        context = super(MinutesCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = MinutesForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        context['title'] = 'Minutes Create'
        return context


# TUTANAK LİSTE
class MinutesListView(PermissionRequiredMixin, TemplateView):
    template_name = 'document/minutes_list.html'
    permission_required = 'document.view_minutes'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Minutes.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        return redirect('/document/minutes/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(MinutesListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Tutanak'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context


# TUTANAK GÜNCELLE
class MinutesUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Minutes
    form_class = MinutesForm
    template_name = 'document/minutes.html'
    success_url = '/document/minutes/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'document.change_minutes'

    def get(self, *args, **kwargs):
        minutes = Minutes.objects.get(pk=self.kwargs['pk'])
        if minutes.worksite not in self.request.user.worksite.all():
            return redirect('/')
        return super(MinutesUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MinutesUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Minutes Update'
        return context


# ÜST YAZI EKLE
class WritingCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = WritingForm
    template_name = 'document/writing.html'
    success_url = '/document/writing/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'document.add_writing'

    def get_context_data(self, *args, **kwargs):
        context = super(WritingCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = WritingForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        context['title'] = 'Writing Create'
        return context


# ÜST YAZI LİSTE
class WritingListView(PermissionRequiredMixin, TemplateView):
    template_name = 'document/writing_list.html'
    permission_required = 'document.view_writing'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Writing.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        return redirect('/document/writing/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(WritingListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Üst Yazı'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context


# ÜST YAZI GÜNCELLE
class WritingUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Writing
    form_class = WritingForm
    template_name = 'document/writing.html'
    success_url = '/document/writing/list'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'document.change_writing'

    def get(self, *args, **kwargs):
        writing = Writing.objects.get(pk=self.kwargs['pk'])
        if writing.worksite not in self.request.user.worksite.filter(active=True):
            return redirect('/')
        return super(WritingUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(WritingUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Writing Update'
        return context



# GÜNLÜK RAPOR EKLE
class DailyReportCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'document/daily_add.html'
    permission_required = 'document.add_daily'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            # Seçilen şantiye ve tarihte daha önceden kayıtlı rapor varsa ajax ile forma işlenecek olup post işlemi ile update edilecektir.
            if self.request.POST.get('worksite') and self.request.POST.get('date'):
                #getDate = datetime.datetime.strptime(self.request.POST.get('date'), "%Y-%m-%d").date()
                data = serializers.serialize('json', DailyReport.objects.filter(worksite_id=self.request.POST.get('worksite'), date=self.request.POST.get('date')))
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse(False, safe=False)
        worksite_id = self.request.POST.get('worksite')
        date = self.request.POST.get('date')
        works = self.request.POST.get('works')
        hours = self.request.POST.get('hours')
        temperature = self.request.POST.get('temperature')
        weather = self.request.POST.get('weather')
        wind = self.request.POST.get('wind')
        production = request.POST.getlist('production[]')
        production = map(str.strip, production)
        production = list(filter(None, production))
        production = ('<x>'.join(production))
        direct = request.POST.getlist('direct[]')
        direct = map(str.strip, direct)
        direct = list(filter(None, direct))
        direct = ('<x>'.join(direct))
        direct_count = request.POST.getlist('direct_count[]')
        direct_count = map(str.strip, direct_count)
        direct_count = list(filter(None, direct_count))
        direct_count = ('<x>'.join(direct_count))
        indirect = request.POST.getlist('indirect[]')
        indirect = map(str.strip, indirect)
        indirect = list(filter(None, indirect))
        indirect = ('<x>'.join(indirect))
        indirect_count = request.POST.getlist('indirect_count[]')
        indirect_count = map(str.strip, indirect_count)
        indirect_count = list(filter(None, indirect_count))
        indirect_count = ('<x>'.join(indirect_count))
        note = request.POST.getlist('note[]')
        note = map(str.strip, note)
        note = list(filter(None, note))
        note = ('<x>'.join(note))
        if DailyReport.objects.filter(worksite_id=self.request.POST.get('worksite'), date=self.request.POST.get('date')).exists():
            DailyReport.objects.filter(worksite_id=self.request.POST.get('worksite'), date=self.request.POST.get('date')).update(
                works=works,
                hours=hours,
                temperature=temperature,
                weather=weather,
                wind=wind,
                production=production,
                direct=direct,
                direct_count=direct_count,
                indirect=indirect,
                indirect_count=indirect_count,
                note=note
            )
            messages.success(request, 'Günlük Rapor Başarıyla Güncellendi!')
        else:
            DailyReport.objects.create(
                worksite_id=worksite_id,
                date=date,
                works=works,
                hours=hours,
                temperature=temperature,
                weather=weather,
                wind=wind,
                production=production,
                direct=direct,
                direct_count=direct_count,
                indirect=indirect,
                indirect_count=indirect_count,
                note=note
            )
            messages.success(request, 'Günlük Rapor Başarıyla Kaydedildi!')
        return super(DailyReportCreateView, self).render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(DailyReportCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Günlük Rapor'
        context['worksites'] = self.request.user.worksite.filter(active=True) # Şantiye listesi bu şekilde kullanıcı üzerinden yapılmalıdır.
        return context



# GÜNLÜK RAPOR LİSTE
class DailyReportListView(PermissionRequiredMixin, TemplateView):
    template_name = 'document/daily_list.html'
    permission_required = 'document.view_daily'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', DailyReport.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        return redirect('/document/report/daily/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(DailyReportListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Günlük Rapor'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context
