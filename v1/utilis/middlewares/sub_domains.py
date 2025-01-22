from debug_toolbar.middleware import DebugToolbarMiddleware
from django.http import HttpResponseNotFound


class SubdomainRoutingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        subdomain = self.get_subdomain(request)
        match subdomain:
            case 'panel':
                request.urlconf = 'config.panel_urls'
                response = self.get_response(request)
                return response

            case 'api':
                request.urlconf = 'config.api_urls'
                response = self.get_response(request)
                return response

            case 'admin':
                request.urlconf = 'config.urls'
                response = self.get_response(request)
                return response
            
            case 'image':
                request.urlconf = 'v1.images.urls'
                response = self.get_response(request)
                return response

            case 'msklad':
                request.urlconf = 'v1.msklad.urls'
                response = self.get_response(request)
                return response

        return HttpResponseNotFound()

    def add_debug_toolbar_middleware(self):
        self.get_response = DebugToolbarMiddleware(self.get_response)

    def get_subdomain(self, request):
        subdomain = request.get_host().split('.')[0]
        if not subdomain in ("api", "panel", "admin", "image", "msklad"):
            subdomain = request.META.get('HTTP_SUBDOMAIN')
            if not subdomain:
                return 'panel'
        return subdomain
