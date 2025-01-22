from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from v1.user.views.api_views import (
    ClientTokenObtainPairView,
    get_users
)


urlpatterns = [
    path("", get_users),
    path('token/', ClientTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
