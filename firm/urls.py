from django.urls import path
from firm import views

app_name = 'firm'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('<slug:slug>/update/', views.FirmUpdateView.as_view(), name='firm_update'),

    path('worksite/', views.WorksiteView.as_view(), name='worksite'),
    path('worksite/add/', views.WorksiteCreateView.as_view(), name='worksite_add'),
    path('worksite/list/', views.WorksiteListView.as_view(), name='worksite_list'),
    path('worksite/<slug:slug>/update/', views.WorksiteUpdateView.as_view(), name='worksite_update'),

    path('subcontractor/', views.SubcontractorView.as_view(), name='subcontractor'),
    path('subcontractor/add/', views.SubcontractorCreateView.as_view(), name='subcontractor_add'),
    path('subcontractor/list/', views.SubcontractorListView.as_view(), name='subcontractor_list'),
    path('subcontractor/list/<int:pk>/update/', views.SubcontractorUpdateView.as_view(), name='subcontractor_update'),

    path('contract/', views.ContractView.as_view(), name='contract'),
    path('contract/add/', views.ContractCreateView.as_view(), name='contract_add'),
    path('contract/list/', views.ContractListView.as_view(), name='contract_list'),
    path('contract/specification/add/', views.ContractSpecificationCreateView.as_view(), name='contract_specification_add'),
    path('contract/specification/list/', views.ContractSpecificationListView.as_view(), name='contract_specification_list'),
    path('contract/list/<int:pk>/update/', views.ContractUpdateView.as_view(), name='contract_update'),
    path('contract/specification/list/<int:pk>/update/', views.ContractSpecificationUpdateView.as_view(), name='contract_specification_update'),

    path('project/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('project/list/', views.ProjectListView.as_view(), name='project_list'),
    path('project/list/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),


]
