class LanguageMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        method_name = request.META.get('HTTP_ACCEPT_METHOD')
        request.lang = language
        request.method_name = method_name
        response = self.get_response(request)
        return response

