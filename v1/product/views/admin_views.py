from django.db import transaction
from django.db.models import F, Q

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from v1.product.models import Product
from v1.product.tasks import upload_image_to_minio
from v1.services.minio_connect import upload_images
from v1.utilis.querysets.get_active_querysets import (
    get_active_ads_product_items, get_active_barcode, get_active_brands, get_active_category_queryset,
    get_active_character_items, get_active_countries, get_active_main_banner, get_active_models, get_active_sellers,
    get_active_sku, get_active_top_category, get_active_top_product
)
from v1.product.sql_query.admin_query import (
    get_products, search_ikpu_sql
)
from v1.product.serializers.admin_serializers import (
    AdsProductItemSerialzier, BarcodeSerialzier, BrandSerialzier, CategoryChildrenSerialzer, CategoryCreateSerialzier,
    CharacterItemSerializer, CountrySerialzier, MainBannerSerializer, ModelSerializer, ProductCreateSerializer,
    ProductDetailSerialzier, ProductItemSerialzier, ProductItemUpdateSerialzier, ProductItemsApiSerializer,
    TopCategorySerializer, TopProductItemSerializer
)
from v1.utilis.custom_responses import (
    error_response, params_error_repsonse, serializer_error_response, serializer_without_paginator_res,
    success_response
)
from v1.utilis.mixins.generic_mixins import (
    CustomCreateAPIView, CustomListAPIView, CustomModelViewSet, CustomRetrieveAPIView, CustomDeleteAPIView,
    CustomUpdateAPIView
)
from v1.utilis.querysets.get_active_querysets import (
    get_active_product_queryset, get_active_product_items
)


class AdsProductItemsAPi(CustomModelViewSet):
    queryset = get_active_ads_product_items()
    serializer_class = AdsProductItemSerialzier


class ProductItemsApi(CustomListAPIView):
    queryset = get_active_product_items()
    serializer_class = ProductItemsApiSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")
        queryset = super().get_queryset()
        if q:
            return queryset.filter(
                Q(artikul_ln__icontains=q) | Q(artikul_ru__icontains=q) | Q(barcode__icontains=q) |
                Q(ikpu__code__icontains=q) | Q(ikpu__title_ln__icontains=q) | Q(ikpu__title_ru__icontains=q)
            )
        return queryset


class MainBannerApi(ModelViewSet):
    queryset = get_active_main_banner()
    pagination_class = PageNumberPagination
    serializer_class = MainBannerSerializer

    def upload_and_save_path(self, obj):
        files = self.request.FILES.getlist("file")
        if not files:
            raise ValidationError({"status": False, "message": "No files provided for upload"})
        images = upload_images(files[:1], "BUCKET3")
        if not images:
            raise ValidationError({"status": False, "message": "Failed to upload images"})
        obj.images+=images
        obj.save()
        return {"status": True}

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = super().create(request, *args, **kwargs)
            obj = self.get_queryset().get(id=data.data['id'])
            result = self.upload_and_save_path(obj)
        if result["status"]:
            return Response(result)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        obj = self.get_queryset().get(id=data.data['id'])
        result = self.upload_and_save_path(obj)
        if result["status"]:
            return Response(result)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class TopProductItemApi(CustomModelViewSet):
    queryset = get_active_top_product()
    serializer_class = TopProductItemSerializer
    pagination_class = PageNumberPagination


class TopCategoryUploadImagesApi(ModelViewSet):
    queryset = get_active_top_category()
    serializer_class = TopCategorySerializer
    pagination_class = PageNumberPagination

    def upload_and_save_path(self, obj):
        files = self.request.FILES.getlist("file")
        if not files:
            return {"status": False, "message": "No files provided for upload"}
        images = upload_images(files[:1], "BUCKET2")
        if not images:
            return {"status": False, "message": "Failed to upload images"}
        obj.images += images
        obj.save()
        return {"status": True}

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        obj = get_active_top_category().get(id=data.data['id'])
        result = self.upload_and_save_path(obj)
        if result["status"]:
            return Response(result)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        obj = get_active_top_category().get(id=data.data['id'])
        result = self.upload_and_save_path(obj)
        if result["status"]:
            return Response(result)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ProductUploadMainImageApi(APIView):
    parser_classes = (MultiPartParser,)

    def upload_items_images_and_save_path(self, product, files):
        pass

    def post(self, request, pk, *args, **kwargs):
        try:
            product = get_active_product_queryset().get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"status": False, "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        files = self.request.FILES.getlist("file")
        if not files:
            return Response(
                {"status": False, "message": "No files provided for upload"},
                status=status.HTTP_400_BAD_REQUEST
            )
        upload_image_to_minio.delay([
            {'name': file.name, 'file': file.read()}
            for file in files
        ], product.id)

        return Response({
            "message": "Images are uploading."
        }, status=status.HTTP_200_OK)

# class ProductUploadMainImageApi(APIView):
#     parser_classes = (MultiPartParser,)

#     def upload_and_save_path(self, product):
#         files = self.request.FILES.getlist("file")
#         if not files:
#             return {"status": False, "message": "No files provided for upload"}

#         images = upload_images(files, "BUCKET1")
#         if not images:
#             return {"status": False, "message": "Failed to upload images"}

#         product.images+=images
#         product.save()
#         return {"status": True, "message": "Image uploaded successfully"}

#     def post(self, request, pk, *args, **kwargs):
#         try:
#             product = get_active_product_queryset().get(id=pk)
#         except Product.DoesNotExist:
#             return Response(
#                 {"status": False, "message": "Product not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         result = self.upload_and_save_path(product)
#         if result["status"]:
#             return Response(result)
#         else:
#             return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ProductAPi(CustomCreateAPIView, CustomListAPIView):
    """Product create for seller"""
    serializer_class = ProductCreateSerializer
    queryset = get_active_product_queryset()

    def create_serializer_response(self):
        return True

    def get(self, request, *args, **kwargs):
        page = self.request.query_params.get("page", 1)
        q = self.request.query_params.get("q")
        return Response(get_products(q, page))


class ProductDetailApi(CustomDeleteAPIView, CustomRetrieveAPIView, CustomUpdateAPIView):
    queryset = get_active_product_queryset()
    serializer_class = ProductDetailSerialzier

    def patch(self, request, pk, *args, **kwargs):
        obj = self.get_object()
        serializer = ProductCreateSerializer(data=request.data, instance=obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": True    
        })


class ProductItemAPI(CustomRetrieveAPIView):
    """
    Get product items after creating product card
    """
    def get(self, request, pk: int, *args, **kwargs):
        product_items = get_active_product_items().filter(product_id=pk)
        serializer = ProductItemSerialzier(product_items, many=True)
        sku = get_active_sku().filter(product_id=pk).first()
        res = {
            "sku": None if not sku else sku.sku,
            "seller_id": product_items.first().product.seller.id,
            "items": serializer.data,
            "images": [image['url'] for image in product_items.first().product.images] if len(product_items.first().product.images) > 0 else None
        }
        return Response(serializer_without_paginator_res(res))
    
    def patch(self, request, pk: int, *args, **kwargs):
        serializer = ProductItemUpdateSerialzier(data=request.data, context={"pk": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(success_response())


class CharacterItemAPI(CustomListAPIView):
    queryset = get_active_character_items().annotate(
        title=F("title_ln")
    )
    serializer_class = CharacterItemSerializer

    def get_queryset(self):
        parent_id = self.request.query_params.get("parent_id")
        if parent_id:
            return self.queryset.all().filter(parent_id=parent_id)
        return self.queryset.all().filter(parent__isnull=True)
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs, context={'queryset': self.queryset})


class CategoryAPi(CustomCreateAPIView, APIView):
    serializer_class = CategoryCreateSerialzier

    # @swagger_auto_schema(request_body=CategoryRetrieveSerialzer)
    @swagger_auto_schema(manual_parameters=[openapi.Parameter(
        'HTTP-ACCEPR-LANGUAGE', openapi.IN_HEADER, description='Custom header description',
        type=openapi.TYPE_STRING,
    ),])
    def get(self, request, *args, **kwargs):
        categories = get_active_category_queryset()
        parent_id = request.query_params.get('parent_id')
        if parent_id:
            
            parent = categories.filter(id=parent_id).first()
            categories = parent.children.filter(is_deleted=False, is_active=True).order_by('-id').annotate(
                title=F("title_ln")
            )
            serializer = CategoryChildrenSerialzer(categories, many=True)
            return Response({
                'status': True,
                'data': serializer.data,
                'parent': {
                    'id': parent_id,
                    'title_ln': parent.title_ln,
                }
            })
        else:
            categories = categories.filter(parent__isnull=True).annotate(
                title=F("title_ln")
            )
            serializer = CategoryChildrenSerialzer(categories, many=True)
            return Response(serializer_without_paginator_res(serializer.data))

    def patch(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        category = get_active_category_queryset().filter(id=category_id).first()
        if not category: return Response(params_error_repsonse())
        serializer = CategoryCreateSerialzier(data=request.POST, instance=category, partial=True)
        if not serializer.is_valid(): return Response(serializer_error_response(serializer.errors))
        serializer.save()
        return Response(success_response())

    def delete(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        category = get_active_category_queryset().filter(id=category_id).first()
        if not category: return Response(params_error_repsonse())
        category.is_active = False
        category.is_deleted = True
        category.save()
        return Response(success_response())


class ModelAPI(CustomListAPIView):
    serializer_class = ModelSerializer
    queryset = get_active_models().annotate(
        title=F("title_ln")
    )

    def get_queryset(self):
        try:
            brand_id = self.request.query_params["brand_id"]
        except:
            return None
        return self.queryset.all().filter(brand_id=brand_id)


class BrandApi(CustomListAPIView):
    serializer_class = BrandSerialzier
    queryset = get_active_brands().annotate(
        title=F("title_ln")
    )


class CountryApi(CustomListAPIView):
    serializer_class = CountrySerialzier
    queryset = get_active_countries().annotate(
        title=F("title_ln")
    )


class BarcodeApi(CustomListAPIView):
    queryset = get_active_barcode()
    serializer_class = BarcodeSerialzier

    def get_queryset(self):
        code = self.request.query_params.get("code")
        if code:
            return self.queryset.all().filter(code=code)
        return None


@api_view(['GET'])
def ikpu_list(request):
    q = request.query_params.get("q")
    if q:
        return Response(search_ikpu_sql(q))
    return Response(None)


class SkuApi(CustomListAPIView):
    queryset = get_active_sku()

    def get_queryset(self):
        seller = self.request.query_params.get("seller")
        sku = self.request.query_params.get("sku")
        sku_obj = self.queryset.all().filter(seller_id=seller, sku=sku).first()
        if sku_obj:
            return True
        return False
    
    def list_custom_response(self):
        if not self.get_queryset():
            return {
                "status": True,
                "exists": False
            }
        return {
            "status": True,
            "exists": True
        }
    
    def get(self, request, *args, **kwargs):
        seller = self.request.query_params.get("seller")
        sku = self.request.query_params.get("sku")
        seller_obj = get_active_sellers().filter(id=seller)
        if not sku or not seller:
            return Response(params_error_repsonse("sku", "seller"))
        if not seller_obj:
            return Response(error_response(seller="Not found"))
        response = self.list_custom_response()
        return Response(response)

