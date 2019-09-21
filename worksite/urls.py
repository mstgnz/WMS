from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import ajax
from . import views
from rest_framework import routers

# REST FRAMEWORK
router = routers.DefaultRouter()
router.register('firms', views.FirmView)
router.register('worksites', views.WorksiteView)
router.register('subcontractors', views.SubcontractorView)
router.register('contracts', views.ContractView)

# URL
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/',include(router.urls)), # REST FRAMEWORK URL REST MİMARİ TAMAMLANDIĞINDA AKTİF EDİLECEKTİR
    path('user/', include('user.urls')),
    path('firm/', include('firm.urls')),
    path('progress/', include('progress.urls')),
    path('document/', include('document.urls')),
    path('accounting/', include('accounting.urls')),
    path('ajax/', ajax.AjaxView.as_view(), name='ajax'),
    path('', TemplateView.as_view(template_name="index.html"), name='index')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
