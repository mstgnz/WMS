from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Firm, Worksite, Subcontractor, Contract, Specification, Project
from .forms import FirmForm, WorksiteForm, SubcontractorForm, ContractForm, SpecificationForm, ProjectForm
from user.models import User

# ANASAYFA
class IndexView(TemplateView):
    template_name = 'firm/index.html'


# FİRMA GÜNCELLE
class FirmUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Firm
    form_class = FirmForm
    template_name = 'form.html'
    success_url = '/firm/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'firm.change_firm'

    def get(self, *args, **kwargs):
        firm = Firm.objects.get(slug=self.kwargs['slug'])
        if firm != self.request.user.firm:
            return redirect('/')
        return super(FirmUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(FirmUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Firm Update'
        return context


# ŞANTİYE ANASAYFA
class WorksiteView(TemplateView):
    template_name = 'firm/worksite.html'


# ŞANTİYE LİSTE
class WorksiteListView(ListView):
    template_name = 'firm/worksite_list.html'
    context_object_name = "worksites"

    def get_queryset(self):
        return self.request.user.firm.worksites.all()


# ŞANTİYE EKLE
class WorksiteCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = WorksiteForm
    template_name = 'form.html'
    success_url = '/firm/worksite/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'firm.add_worksite'
    redirect_field_name = '/firm/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.firm = self.request.user.firm
        obj.save()
        return super(WorksiteCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(WorksiteCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Worksite Create'
        return context


# ŞANTİYE GÜNCELLE
class WorksiteUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Worksite
    form_class = WorksiteForm
    template_name = 'form.html'
    success_url = '/firm/worksite/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'firm.change_worksite'

    def get(self, *args, **kwargs):
        worksite = Worksite.objects.get(slug=self.kwargs['slug'])
        if worksite not in self.request.user.worksite.all():
            return redirect('/')
        return super(WorksiteUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(WorksiteUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Worksite Update'
        return context


# TAŞERON ANASAYFA
class SubcontractorView(TemplateView):
    template_name = 'firm/subcontractor.html'


# TAŞERON EKLE
class SubcontractorCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = SubcontractorForm
    template_name = 'form.html'
    success_url = '/firm/subcontractor/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'firm.add_subcontractor'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.firm = self.request.user.firm
        obj.save()
        return super(SubcontractorCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(SubcontractorCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = SubcontractorForm(user=self.request.user) # forms.py dosyasında kullanıcı bazlı listeleme yapılıyor.
        context['title'] = 'Subcontractor Create'
        return context


# TAŞERON LİSTE
class SubcontractorListView(PermissionRequiredMixin, TemplateView):
    template_name = 'firm/subcontractor_list.html'
    permission_required = 'firm.view_subcontractor'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Subcontractor.objects.filter(worksite__in=[self.request.POST.get('worksite')]))
            return JsonResponse(data, safe=False)
        return redirect('/firm/subcontractor/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(SubcontractorListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Taşeron'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context


# TAŞERON GÜNCELLE
class SubcontractorUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subcontractor
    form_class = SubcontractorForm
    template_name = 'form.html'
    success_url = '/firm/subcontractor/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'firm.change_subcontractor'

    # url adresinden farklı id ile giriş yapılırsa kontrolü sağlanıyor.
    def get(self, *args, **kwargs):
        subcontractor = Subcontractor.objects.get(pk=self.kwargs['pk'])
        if subcontractor not in Subcontractor.objects.filter(firm=self.request.user.firm):
            return redirect('/')
        return super(SubcontractorUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SubcontractorUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Subcontractor Update'
        context['form'] = SubcontractorForm(user=self.request.user, instance=Subcontractor.objects.get(pk=self.kwargs['pk'])) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        return context


# SÖZLEŞME ANASAYFA
class ContractView(TemplateView):
    template_name = 'firm/contract.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ContractView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Contract Anasayfa'
        return context
        

# SÖZLEŞME EKLE
class ContractCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ContractForm
    template_name = 'form.html'
    success_url = '/firm/contract/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'firm.add_contract'

    def get_context_data(self, *args, **kwargs):
        context = super(ContractCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = ContractForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        context['title'] = 'Contract Create'
        return context


# SÖZLEŞME LİSTE
class ContractListView(PermissionRequiredMixin, TemplateView):
    template_name = 'firm/contract_list.html'
    permission_required = 'firm.view_contract'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Contract.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        return redirect('/firm/contract/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(ContractListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Sözleşme'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context


# SÖZLEŞME GÜNCELLE
class ContractUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'form.html'
    success_url = '/firm/contract/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'firm.change_contract'

    # url adresinden farklı id ile giriş yapılırsa kontrolü sağlanıyor.
    def get(self, *args, **kwargs):
        contract = Contract.objects.get(pk=self.kwargs['pk'])
        if contract.worksite not in self.request.user.worksite.filter(active=True):
            return redirect('/')
        return super(ContractUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ContractUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Sözleşme Güncelle'
        context['form'] = ContractForm(user=self.request.user, instance=Contract.objects.get(pk=self.kwargs['pk']))
        return context


# ŞARTNAME EKLE
class ContractSpecificationCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = SpecificationForm
    template_name = 'form.html'
    success_url = '/firm/contract/specification/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'firm.add_specification'

    def get_context_data(self, *args, **kwargs):
        context = super(ContractSpecificationCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = SpecificationForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        context['title'] = 'Specification Create'
        return context


# ŞARTNAME LİSTE
class ContractSpecificationListView(PermissionRequiredMixin, TemplateView):
    template_name = 'firm/specification_list.html'
    permission_required = 'firm.view_specification'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Specification.objects.filter(contract__in=Contract.objects.filter(worksite=self.request.POST.get('worksite'))))
            return JsonResponse(data, safe=False)
        return redirect('/firm/specification/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(ContractSpecificationListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Şartname'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context


# ŞARTNAME GÜNCELLE
class ContractSpecificationUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Specification
    form_class = SpecificationForm
    template_name = 'form.html'
    success_url = '/firm/contract/specification/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'firm.change_specification'

    # url adresinden farklı id ile giriş yapılırsa kontrolü sağlanıyor.
    def get(self, *args, **kwargs):
        specification = Specification.objects.get(pk=self.kwargs['pk'])
        if specification.contract.worksite not in self.request.user.worksite.filter(active=True): # Güncelleme ve kayıt işlemleri aktif şantiyelerde olmalıdır.
            return redirect('/')
        return super(ContractSpecificationUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ContractSpecificationUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Specification Update'
        context['form'] = SpecificationForm(user=self.request.user, instance=Specification.objects.get(pk=self.kwargs['pk']))
        return context



# PROJE LİSTE
class ProjectListView(PermissionRequiredMixin, TemplateView):
    template_name = 'firm/project_list.html'
    permission_required = 'firm.view_project'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            data = serializers.serialize('json', Project.objects.filter(worksite=self.request.POST.get('worksite')))
            return JsonResponse(data, safe=False)
        return redirect('/firm/project/list/')
            
    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Proje'
        context['worksites'] = self.request.user.worksite.filter(active=True)
        return context


# PROJE EKLE
class ProjectCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ProjectForm
    template_name = 'form.html'
    success_url = '/firm/project/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'firm.add_project'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(*args, **kwargs)
        context['form'] = ProjectForm(user=self.request.user) #forms.py içinde kullanıcıya göre filtreleme yapılıyor.
        context['title'] = 'Project Create'
        return context


# PROJE GÜNCELLE
class ProjectUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'form.html'
    success_url = '/firm/project/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'firm.change_project'

    # url adresinden farklı id ile giriş yapılırsa kontrolü sağlanıyor.
    def get(self, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs['pk'])
        if project.worksite not in self.request.user.worksite.filter(active=True):
            return redirect('/')
        return super(ProjectUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Project Update'
        context['form'] = ProjectForm(user=self.request.user, instance=Project.objects.get(pk=self.kwargs['pk']))
        return context
