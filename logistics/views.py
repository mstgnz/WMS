from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from user.models import User

# ANASAYFA
class IndexView(TemplateView):
    template_name = 'progress/index.html'