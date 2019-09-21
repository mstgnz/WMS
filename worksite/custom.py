import re
from django.conf import settings
from django.shortcuts import redirect

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginControl:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_URL)
        elif request.user.is_authenticated or url_is_exempt:
            return None
        else:
            return redirect('/')


# return GET objects or NONE 
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None