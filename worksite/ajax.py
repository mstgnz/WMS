from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from firm.models import Firm, Worksite, Subcontractor
from progress.models import Progress, Discovery, Synopsis


# AJAX
class AjaxView(TemplateView):
    template_name = 'user/index.html'
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            # ŞANTİYEYE GÖRE TAŞERON LİSTELEME
            if self.request.POST.get('type') == 'sub_select':
                data = {
                    'firm' : serializers.serialize('json', Firm.objects.filter(pk=self.request.user.firm.id)),
                    'sub' : serializers.serialize('json', Subcontractor.objects.filter(worksite=self.request.POST.get('worksite')))
                }
                return JsonResponse(data, safe=False)

    def get(self, *args, **kwargs):
        return redirect('/')