from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)
from v1.user.views.admin_views import (
    MyTokenObtainPairView,
    SellerApi,
    ClientListAPI,
    ClientConfirmAPI
)
app_name = 'v1_user_admin_urls'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('seller/', SellerApi.as_view()),
    path('clients/', ClientListAPI.as_view()),
    path('client/<int:pk>/', ClientConfirmAPI.as_view()),
]
