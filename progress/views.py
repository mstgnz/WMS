from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
from firm.models import Firm, Worksite, Subcontractor, Contract
from .models import Analysis, AnalysisDetail, Discovery, Progress, Synopsis
from .forms import AnalysisForm, AnalysisDetailForm, DiscoveryForm, ProgressForm, SynopsisForm
from user.models import User
from worksite.custom import get_or_none


# HAKEDİŞ ANASAYFA
class IndexView(TemplateView):
    template_name = 'progress/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        return context    


# HAKEDİŞ EKLE
class ProgressCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'progress/progress_add.html'
    permission_required = 'progress.add_progress'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data={
                'worksite' : serializers.serialize('json', Worksite.objects.filter(pk=self.request.POST.get('worksite'))),
                'progress' : serializers.serialize('json', Progress.objects.filter(worksite=self.request.POST.get('worksite'), subcontractor__isnull=True)),
                'discovery' : serializers.serialize('json', Discovery.objects.filter(worksite=self.request.POST.get('worksite'))),
                'synopsis' : serializers.serialize('json', Synopsis.objects.filter(progress=Progress.objects.filter(worksite=self.request.POST.get('worksite'), subcontractor__isnull=True).order_by('-id')[:1]))
            }
            return JsonResponse(data, safe=False)
        
        if context["form"].is_valid():
            # HAKEDİŞ
            progress = context["form"].save()
            # İCMAL
            pose_no = request.POST.getlist('pose_no[]')
            name = request.POST.getlist('name[]')
            unit = request.POST.getlist('unit[]')
            unit_price = request.POST.getlist('unit_price[]')
            total_quantity = request.POST.getlist('total_quantity[]')
            previous_quantity = request.POST.getlist('previous_quantity[]')
            this_quantity = request.POST.getlist('this_quantity[]')
            total_price = request.POST.getlist('total_price[]')
            previous_price = request.POST.getlist('previous_price[]')
            this_price = request.POST.getlist('this_price[]')
            
            for i in range(len(pose_no)):
                Synopsis.objects.create(progress=progress, pose_no=pose_no[i], name=name[i], unit=unit[i], unit_price=unit_price[i], total_quantity=total_quantity[i], previous_quantity=previous_quantity[i], this_quantity=this_quantity[i], total_price=total_price[i], previous_price=previous_price[i], this_price=this_price[i])
            messages.success(request, 'Hakediş Kaydedildi')
        return redirect('/progress/list/')
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProgressCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = ProgressForm(self.request.POST or None, user=self.request.user)
        context['title'] = 'Hakediş Ekle'
        return context


# HAKEDİŞ LİSTE
class ProgressListView(PermissionRequiredMixin, TemplateView):
    template_name = 'progress/progress_list.html'
    permission_required = 'progress.view_progress'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data={
                'progress' : serializers.serialize('json', Progress.objects.filter(worksite=self.request.POST.get('worksite')).order_by('-id')[:1]),
                'discovery' : serializers.serialize('json', Discovery.objects.filter(worksite=self.request.POST.get('worksite'))),
                'synopsis' : serializers.serialize('json', Synopsis.objects.filter(progress=Progress.objects.filter(worksite=self.request.POST.get('worksite')).order_by('-id')[:1]))
            }
            return JsonResponse(data, safe=False)

    def get_context_data(self, *args, **kwargs):
        context = super(ProgressListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Hakediş'
        context['form'] = ProgressForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        return context


# HAKEDİŞ EKLE
class ProgressSubCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'progress/progress_add_sub.html'
    permission_required = 'progress.add_progress'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            if self.request.POST.get('type') == 'sub_select':
                data={
                    'progress' : serializers.serialize('json', Progress.objects.filter(worksite=self.request.POST.get('worksite'), subcontractor=self.request.POST.get('subcontractor'))),
                    'discovery' : serializers.serialize('json', Discovery.objects.filter(worksite=self.request.POST.get('worksite'))),
                    'synopsis' : serializers.serialize('json', Synopsis.objects.filter(progress=Progress.objects.filter(worksite=self.request.POST.get('worksite'), subcontractor=self.request.POST.get('subcontractor')).order_by('-id')[:1]))
                }
            else:
                data={
                    'worksite' : serializers.serialize('json', Worksite.objects.filter(pk=self.request.POST.get('worksite'))),
                    'subcontractor' : serializers.serialize('json', Subcontractor.objects.filter(worksite=self.request.POST.get('worksite')))
                }
            return JsonResponse(data, safe=False)
        
        if context["form"].is_valid():
            # HAKEDİŞ
            progress = context["form"].save()
            # İCMAL
            pose_no = request.POST.getlist('pose_no[]')
            name = request.POST.getlist('name[]')
            unit = request.POST.getlist('unit[]')
            unit_price = request.POST.getlist('unit_price[]')
            total_quantity = request.POST.getlist('total_quantity[]')
            previous_quantity = request.POST.getlist('previous_quantity[]')
            this_quantity = request.POST.getlist('this_quantity[]')
            total_price = request.POST.getlist('total_price[]')
            previous_price = request.POST.getlist('previous_price[]')
            this_price = request.POST.getlist('this_price[]')
            
            for i in range(len(pose_no)):
                if(pose_no[i] and name[i] and unit[i] and unit_price[i] and total_quantity[i]):
                    Synopsis.objects.create(progress=progress, pose_no=pose_no[i], name=name[i], unit=unit[i], unit_price=float(unit_price[i]), total_quantity=float(total_quantity[i]), previous_quantity=float(previous_quantity[i]), this_quantity=float(this_quantity[i]), total_price=float(total_price[i]), previous_price=float(previous_price[i]), this_price=float(this_price[i]))
            messages.success(request, 'Hakediş Kaydedildi')
        return redirect('/progress/list/')
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProgressSubCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = ProgressForm(self.request.POST or None, user=self.request.user)
        context['title'] = 'Taşeron Hakediş Ekle'
        return context



# KEŞİF ANASAYFA
class DiscoveryIndexView(TemplateView):
    template_name = 'progress/discovery.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DiscoveryIndexView, self).get_context_data(*args, **kwargs)
        return context   


# KEŞİF EKLE
class DiscoveryCreateView(PermissionRequiredMixin, TemplateView):
    template_name = 'progress/discovery_add.html'
    permission_required = 'progress.add_discovery'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Discovery.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        worksite = request.POST.get('worksite')
        no = request.POST.getlist('no[]')
        name = request.POST.getlist('name[]')
        unit = request.POST.getlist('unit[]')
        amount = request.POST.getlist('amount[]')
        price = request.POST.getlist('price[]')
        total = request.POST.getlist('total[]')
        error_list = []
        success_list = []
        for i in range(len(no)):
            if Discovery.objects.filter(no=no[i].strip(), worksite=worksite).exists():
                error_list.append(no[i])
            else:
                Discovery.objects.create(worksite_id=worksite, no=no[i].strip(), name=name[i].strip(), unit=unit[i], amount=amount[i], price=price[i], total=total[i])
                success_list.append(no[i])
        if len(error_list)>0:
            messages.warning(request, 'Poz numaraları zaten mevcut -> {}'.format(error_list))
        if len(success_list)>0:
            messages.success(request, 'Poz numaraları kaydedildi -> {}'.format(success_list))
        return redirect('/progress/discovery/detail/')

    def get_context_data(self, *args, **kwargs):
        context = super(DiscoveryCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = DiscoveryForm(user=self.request.user)
        context['title'] = 'Discovery Create'
        return context


# KEŞİF LİSTE
class DiscoveryDetailView(PermissionRequiredMixin, TemplateView):
    template_name = 'progress/discovery_detail.html'
    permission_required = 'progress.change_discovery'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Discovery.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        worksite = request.POST.get('worksite')
        no = request.POST.getlist('no[]')
        name = request.POST.getlist('name[]')
        unit = request.POST.getlist('unit[]')
        amount = request.POST.getlist('amount[]')
        total = request.POST.getlist('total[]')
        for i in range(len(no)):
            Discovery.objects.filter(worksite=worksite, no=no[i]).update(name=name[i].strip(), unit=unit[i], amount=amount[i], total=total[i])
        messages.success(request, 'Poz numaraları güncellendi')
        return redirect('/progress/discovery/detail/')
        
    def get_context_data(self, *args, **kwargs):
        context = super(DiscoveryDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Discovery Detail'
        context['form'] = DiscoveryForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        return context



# ANALİZ EKLE LİSTE GÜNCELLE
class DiscoveryAnalysisView(PermissionRequiredMixin, TemplateView):
    template_name = 'progress/analysis.html'
    permission_required = 'progress.create_analysis'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            if Analysis.objects.filter(discovery=self.kwargs['pk']).exists():
                obj = context["form"].save() # get_context_data da instance tanımlaması yapıldı.
                # Keşif tablosundaki birim fiyat analize göre güncelleniyor.
                Discovery.objects.filter(pk=self.kwargs['pk']).update(price=obj.tender, total=round(context['discovery'].amount*obj.tender,2))
                pk = request.POST.getlist('pk[]')
                category = request.POST.getlist('category[]')
                definition = request.POST.getlist('definition[]')
                amount = request.POST.getlist('amount[]')
                price = request.POST.getlist('price[]')
                total = request.POST.getlist('total[]')
                for i in range(len(definition)):
                    # Analiz tablosunda var olan kayıtları güncelliyor olmayanları ekliyor.
                    if pk[i]:
                        AnalysisDetail.objects.filter(pk=pk[i]).update(category=category[i], definition=definition[i].strip(), amount=amount[i], price=price[i], total=total[i])
                    else:
                        AnalysisDetail.objects.create(analysis_id=obj.pk, category=category[i], definition=definition[i].strip(), amount=amount[i], price=price[i], total=total[i])
                messages.success(request, '{} kaydı güncellendi!.'.format(context["discovery"]))
                return redirect('/progress/discovery/detail/'+str(self.kwargs['pk']))
            else:
                obj = context["form"].save(commit=False)
                obj.discovery = context["discovery"]
                obj.save()
                # Keşif tablosundaki birim fiyat analize göre güncelleniyor.
                Discovery.objects.filter(pk=self.kwargs['pk']).update(price=obj.tender, total=round(context['discovery'].amount*obj.tender,2))
                category = request.POST.getlist('category[]')
                definition = request.POST.getlist('definition[]')
                amount = request.POST.getlist('amount[]')
                price = request.POST.getlist('price[]')
                total = request.POST.getlist('total[]')
                for i in range(len(definition)):
                    AnalysisDetail.objects.create(analysis_id=obj.pk, category=category[i], definition=definition[i].strip(), amount=amount[i], price=price[i], total=total[i])
                messages.success(request, 'Kayıt İşlemi Başarılı')
                return redirect('/progress/discovery/detail/')
        return super(DiscoveryAnalysisView, self).render_to_response(context)
    
    def get_context_data(self, *args, **kwargs):
        context = super(DiscoveryAnalysisView, self).get_context_data(*args, **kwargs)
        context['form'] = AnalysisForm(self.request.POST or None, instance=get_or_none(Analysis, discovery=self.kwargs['pk']))
        context['discovery'] = Discovery.objects.get(pk=self.kwargs['pk'])
        context['worksite'] = Worksite.objects.get(pk=Discovery.objects.get(pk=self.kwargs['pk']).worksite.pk)
        if Analysis.objects.filter(discovery=self.kwargs['pk']).exists():
            analysis = Analysis.objects.get(discovery=self.kwargs['pk'])
            context['material'] = AnalysisDetail.objects.filter(category="material", analysis=analysis)
            context['workmanship'] = AnalysisDetail.objects.filter(category="workmanship", analysis=analysis)
            context['overheads'] = AnalysisDetail.objects.filter(category="overheads", analysis=analysis)
        return context
        

