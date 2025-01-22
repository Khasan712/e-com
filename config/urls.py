from django.urls import path, include

urlpatterns = [
    # API V1
    path('api/v1/user/', include("v1.user.urls.admin_urls")),
    path('api/v1/product/', include("v1.product.urls.admin_urls")),
    path('api/v1/proposal/', include("v1.proposal.urls.admin_urls")),
    path('api/v1/order/', include("v1.order.urls.admin_urls")),
]
