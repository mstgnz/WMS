from django.views.generic import View, FormView, TemplateView, UpdateView, CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from django.core import serializers
from .models import User
from .forms import LoginForm, ProfileUpdateForm, RegisterForm, StaffUpdateForm
from firm.models import Worksite


class IndexView(TemplateView):
    template_name = 'user/index.html'

    # admin view site bu url ye geliyor ve eğer firması yoksa siteyi göremez. farklı url lere elle girerek girer ama zaten firma atanmadığı için ekleme yapamaz.
    def get(self, request, *args, **kwargs):
        if(not request.user.firm):
            return redirect('/admin')
        return render(request, self.template_name, {})

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['request_dir'] = dir(self.request.user)
        context['userWorksiteAll'] =  self.request.user.worksite.all # countUserWorksite = Worksite.objects.filter(user=user).count()
        return context


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'user/login.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user:
                if user.is_superuser:
                    login(request, user)
                    return redirect('/admin')
                if user.firm and user.firm.active:
                    login(request, user)
                    return redirect('user:index')
                messages.warning(request, "Firmanız Aktif Değil!")
                return redirect('/')
        return render(request, self.template_name, {'form': form})


class PasswordView(FormView):
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form':form, 'title':'Password Change'})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Parola Güncellendi.")
            return redirect('user:index')
        return render(request, self.template_name, {'form':form, 'title':'Password Change'})


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = User
    form_class = ProfileUpdateForm
    success_url = '/user/'
    success_message = "Güncelleme işlemi başarılı!"

    def get(self, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if user != self.request.user:
            return redirect('/')
        return super(ProfileUpdateView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Profile Update'
        return context


class PasswordResetView(FormView):
    pass



class StaffCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'form.html'
    success_url = '/user/staff/list/'
    success_message = "Kayıt işlemi başarılı!"
    permission_required = 'user.add_user'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.firm = self.request.user.firm
        obj.set_password(form.cleaned_data.get('password1'))
        obj.save()
        return super(StaffCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(StaffCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'User Create'
        return context


class StaffListView(ListView):
    template_name = 'user/staff_list.html'
    context_object_name = "staff"

    def get_queryset(self):
        return User.objects.filter(firm=self.request.user.firm)


class StaffUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = StaffUpdateForm
    template_name = 'form.html'
    success_url = '/user/staff/list/'
    success_message = "Güncelleme işlemi başarılı!"
    permission_required = 'user.change_user'

    def get_context_data(self, *args, **kwargs):
        context = super(StaffUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Staff Update'
        return context


class StaffPermissionView(PermissionRequiredMixin, TemplateView):
    template_name = 'user/staff_permission.html'
    permission_required = 'user.change_user'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            user = User.objects.get(email=self.request.POST.get('user', None))
            data = serializers.serialize('json', Permission.objects.filter(user=user).exclude(content_type_id__in=[1,2,3,4,5,6]))
            return JsonResponse(data, safe=False)
        if request.method=='POST':
            if request.POST.get('user'):
                select = request.POST.getlist('select')
                selected = request.POST.getlist('selected')
                user = User.objects.get(email=request.POST.get('user'))
                if select:
                    for x in select:
                        user.user_permissions.add(Permission.objects.get(name=x))
                elif selected:
                    for y in selected:
                        user.user_permissions.remove(Permission.objects.get(name=y))
                messages.success(request, 'Personel izin hakları güncellendi.')
                return redirect('/user/staff/permission/')
        return super(StaffPermissionView, self).render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(StaffPermissionView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Personel İzin Hakları'
        context['users'] = User.objects.filter(firm_id=self.request.user.firm_id)
        context['permission'] = Permission.objects.all().exclude(content_type_id__in=[1,2,3,4,5,6])
        return context


class StaffWorksiteView(PermissionRequiredMixin, TemplateView):
    template_name = 'user/staff_worksite.html'
    permission_required = 'user.change_user'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.is_ajax():
            user = User.objects.get(email=self.request.POST.get('user', None))
            data = serializers.serialize('json', Worksite.objects.filter(user=user))
            return JsonResponse(data, safe=False)
        if request.method=='POST':
            if request.POST.get('user'):
                select = request.POST.getlist('select')
                selected = request.POST.getlist('selected')
                user = User.objects.get(email=request.POST.get('user'))
                if select:
                    for x in select:
                        user.worksite.add(Worksite.objects.get(name=x))
                elif selected:
                    for y in selected:
                        user.worksite.remove(Worksite.objects.get(name=y))
                messages.success(request, 'Personel şantiye izin hakları güncellendi.')
                return redirect('/user/staff/worksite/')
        return super(StaffWorksiteView, self).render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(StaffWorksiteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Personel Worksite Hakları'
        context['users'] = User.objects.filter(firm_id=self.request.user.firm_id)
        context['worksite'] = Worksite.objects.filter(firm=self.request.user.firm)
        return context
