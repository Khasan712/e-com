from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
import jwt
from django.conf import settings
from v1.utilis.querysets.get_active_querysets import get_active_admins
from v1.user.models import Admin
from v1.utilis.not_required_token_api import get_not_required_token_api


class IsAdminMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.get_host().split(".")[0] == 'admin' and request.path.startswith("/api/"):
            if request.path not in get_not_required_token_api():
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    response = Response({
                        "detail": "Authentication credentials were not provided."
                    }, status=HTTP_401_UNAUTHORIZED)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
                    return response
                auth_token = auth_header.split(' ')[1]  # Assuming the token is in the format "Bearer <token>"
                try:
                    decoded_token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
                    user_id = decoded_token['user_id']
                    get_active_admins().get(id=user_id)
                # except jwt.exceptions.DecodeError:
                except Admin.DoesNotExist:
                    response = Response({
                        "status": False,
                        "error": "User not found"
                    }, status=HTTP_400_BAD_REQUEST)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
                    return response
                except:
                    response = Response(
                        {
                            "detail": "Given token not valid for any token type",
                            "code": "token_not_valid",
                            "messages": [
                                {
                                    "token_class": "AccessToken",
                                    "token_type": "access",
                                    "message": "Token is invalid or expired"
                                }
                            ]
                        }, status=HTTP_401_UNAUTHORIZED
                    )
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
                    return response
        
        response = self.get_response(request)
        return response

