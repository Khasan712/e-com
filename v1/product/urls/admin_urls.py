from django.urls import path
from v1.product.views.admin_views import (
    CategoryAPi, ProductAPi, BrandApi, CountryApi, ProductItemAPI, CharacterItemAPI, ModelAPI,
    BarcodeApi, SkuApi, ProductDetailApi, ikpu_list, ProductUploadMainImageApi, TopCategoryUploadImagesApi,
    TopProductItemApi, MainBannerApi, ProductItemsApi, AdsProductItemsAPi
)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register('ads', AdsProductItemsAPi)
router.register('top-category', TopCategoryUploadImagesApi)
router.register('top', TopProductItemApi)
router.register('main-banner', MainBannerApi)


urlpatterns = [
    path("items/", ProductItemsApi.as_view()),
    path("images/<int:pk>/", ProductUploadMainImageApi.as_view()),
    path("", ProductAPi.as_view()),
    path("<int:pk>/", ProductDetailApi.as_view()),
    path("<int:pk>/items/", ProductItemAPI.as_view()),
    path("character/items/", CharacterItemAPI.as_view()),
    path("category/", CategoryAPi.as_view()),
    path("country/", CountryApi.as_view()),
    path("brand/", BrandApi.as_view()),
    path("model/", ModelAPI.as_view()),
    path("barcode/", BarcodeApi.as_view()),
    path("ikpu/", ikpu_list),
    path("sku/", SkuApi.as_view()),
]+router.urls



