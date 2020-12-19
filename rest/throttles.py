from rest_framework.throttling import SimpleRateThrottle

class PostThrottle(SimpleRateThrottle):
    scope = "toManyPost"

    def get_cache_key(self, request, view):
        if request.method == "GET":
            return None
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }