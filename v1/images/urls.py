from django.urls import path
from v1.images.views import get_image


urlpatterns = [
    path('<str:bucket>/<str:image_name>/', get_image)
]
