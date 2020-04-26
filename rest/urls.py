from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'firm', views.FirmViewSet)
router.register(r'worksite', views.WorksiteViewSet)
router.register(r'subcontractor', views.SubcontractorViewSet)
router.register(r'contract', views.ContractViewSet)
router.register(r'specification', views.SpecificationViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'discovery', views.DiscoveryViewSet)
router.register(r'analysis', views.AnalysisViewSet)
router.register(r'analysisdetail', views.AnalysisDetailViewSet)
router.register(r'progress', views.ProgressViewSet)
router.register(r'synopsis', views.SynopsisViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('/', include('rest_framework.urls', namespace='rest_framework'))
]
