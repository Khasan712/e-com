from django.urls import path, include


urlpatterns = [
    path("api/v1/user/", include("v1.user.urls.api_urls")),
    path("api/v1/proposal/", include("v1.proposal.urls.api_urls")),
    path("api/v1/product/", include("v1.product.urls.api_urls")),
    path("api/v1/order/", include("v1.order.urls.api_urls")),
]
