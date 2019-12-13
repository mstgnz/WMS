from django.urls import path
from logistics import views

app_name = 'logistics'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
