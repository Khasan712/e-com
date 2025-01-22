from django.urls import path
from v1.product.views.api_views import (
    MainBannerApi, TopProductItemApi, TopCategoryApi, get_all_categories, NewProductsApi,
    AdsProductItemsApi, GetProductDetailApi, SideBarFilters, GetProductApi,
    CartApi
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cart', CartApi)


urlpatterns = [
    path('side-bar/', SideBarFilters.as_view()),
    path('', GetProductApi.as_view()),
    path('<int:pk>/', GetProductDetailApi.as_view()),
    path('ads/', AdsProductItemsApi.as_view()),
    path('new/', NewProductsApi.as_view()),
    path('main-banner/', MainBannerApi.as_view()),
    path('top/', TopProductItemApi.as_view()),
    path('top-category/', TopCategoryApi.as_view()),
    path('all-categories/', get_all_categories),
]+router.urls
