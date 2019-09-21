from django.urls import path
from progress import views

app_name = 'progress'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.ProgressCreateView.as_view(), name='progress_add'),
    path('list/', views.ProgressListView.as_view(), name='progress_list'),
    path('add/sub/', views.ProgressSubCreateView.as_view(), name='progress_add_sub'),
    path('discovery/', views.DiscoveryIndexView.as_view(), name='discovery'),
    path('discovery/add/', views.DiscoveryCreateView.as_view(), name='discovery_add'),
    path('discovery/detail/', views.DiscoveryDetailView.as_view(), name='discovery_detail'),
    path('discovery/detail/<int:pk>/', views.DiscoveryAnalysisView.as_view(), name='discovery_analysis'),

]
