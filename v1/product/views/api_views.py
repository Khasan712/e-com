from v1.product.serializers.api_serialziers import (
    ClientBrandSerializer, ClientMainBannerSerializer, ClientModelSerializer, ClientTopCategorySerializer,
    GetProductItemSerializer, CartDetailSerializer
)
from v1.product.sql_query.admin_query import get_all_active_category
from v1.product.sql_query.api_query import (
    get_products, get_carts, get_ads_products, get_new_products, get_top_products, get_product_detail
)
from v1.product.tasks import mass_create_cart, mass_delete_carts
from v1.services.full_filter import (
    category_children_tree, get_category_and_children_id, get_product_items_full_filter
)
from v1.user.permissions import IsClientAuthenticated
from v1.utilis.mixins.generic_mixins import (
    CustomListAPIView, CustomModelViewSet
)
from v1.utilis.querysets.get_active_querysets import (
    get_active_brands, get_active_category_queryset, get_active_character_items,
    get_active_main_banner, get_active_models, get_active_product_item_sell_price, get_active_product_items,
    get_active_top_category, get_active_cart
)
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import F, OuterRef, Subquery, FloatField, Min, Max
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from django.db.models.functions import Coalesce
from django.core.cache import cache


class CartApi(CustomModelViewSet):
    queryset = get_active_cart()
    serializer_class = CartDetailSerializer
    permission_classes = (IsClientAuthenticated,)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.id != obj.user.id:
            raise ValidationError({"status": False, "error": "No cart found!"})
        return obj

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            mass_create_cart.delay(data, request.user.id)
            return Response({"status": True})
        elif isinstance(data, dict):
            mass_create_cart.delay([data], request.user.id)
            return Response({"status": True})
        else:
            return Response({
                "status": False,
                "error": "Data type not supported."
            })

    def list(self, request, *args, **kwargs):
        carts = get_carts(request.user.id)
        return Response({
            "status": True,
            "data": carts
        }, status=200)

    @action(methods=['DELETE'], url_path='many-delete', detail=False)
    def many_delete(self, request, *args, **kwargs):
        carts_id = request.data.get('carts_id')
        if not carts_id or not isinstance(carts_id, list):
            return Response({"status": False, "error": "there is no carts_id in request body or carts_id not list!"})
        mass_delete_carts.delay(carts_id, request.user.id)
        return Response({"status": True}, status=204)


class GetProductApi(APIView):

    def get_filters(self):
        filters = self.request.data.get("filters")
        if filters:
            return {
                key: value
                for key, value in filters.items()    
            }
        return None

    def post(self, request, *args, **kwargs):
        return Response(
            get_products(self.get_filters())
        )


class GetProductDetailApi(APIView):

    def get(self, request, pk: int):
        try:
            product_item = get_active_product_items().get(id=pk)
        except:
            return Response({"status": False, "error": "Product not found!"})
        return Response({
            "status": True,
            "data": get_product_detail(product_item.product.id)
        })


class GetProductItemsApi(CustomListAPIView):
    queryset = get_active_product_items()
    serializer_class = GetProductItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        q = params.get("q")
        category_id = params.get("category_id")
        brand_id = params.get("brand_id")
        model_id = params.get("model_id")
        character_id = params.get("character_id")

        prices = get_active_product_item_sell_price().filter(product_item_id=OuterRef('id')).values('price')[:1]
        items = queryset.annotate(
            price=Subquery(prices),
            brand=F("product__brand"),
            model=F("product__model"),
        )
        if q:
            items = get_product_items_full_filter(q, items)
        
        if category_id:
            category = get_active_category_queryset().filter(id=category_id).first()
            if not category:
                return False
            items = items.filter(product__category_id__in=get_category_and_children_id(category))
        
        if brand_id:
            items = items.filter(brand=brand_id)
        if model_id:
            items = items.filter(model=model_id)
        if character_id:
            items = items.filter(characteristics__title__id=character_id)

        return items


class SideBarFilters(APIView):
    
    def get_min_max_prices(self, items):
        return items.aggregate(
            min_price=Coalesce(Min("price"), 0.0, output_field=FloatField()),
            max_price=Coalesce(Max('price'), 0.0, output_field=FloatField()),
        )
    
    def get_characteristics(self, characteristics):
        item_characteristics = get_active_character_items().filter(
            characteristic_items__id__in=characteristics
        ).distinct().annotate(parent_title_ln=F("parent__title_ln"))
        characteristics = {}
        for item_characteristic in item_characteristics:
            if item_characteristic.parent_title_ln not in characteristics:
                characteristics[item_characteristic.parent_title_ln] = []
            characteristics[item_characteristic.parent_title_ln].append({
                "id": item_characteristic.id,
                "title_ln": item_characteristic.title_ln,
                "title_ru": item_characteristic.title_ru,
            })
        return characteristics

    def get_models(self, model):
        models = get_active_models().filter(id__in=model).distinct()
        return ClientModelSerializer(models, many=True).data
    
    def get_brands(self, brands):
        brands = get_active_brands().filter(id__in=brands).distinct()
        return ClientBrandSerializer(brands, many=True).data
    
    def get_category_tree(self):
        params = self.request.query_params
        category_id = params.get("category_id")
        if category_id:
            category = get_active_category_queryset().filter(id=category_id).first()
            return category_children_tree(category)
        return "All"

    def get_queryset(self):
        queryset = get_active_product_items()
        params = self.request.query_params
        q = params.get("q")
        category_id = params.get("category_id")

        prices = get_active_product_item_sell_price().filter(product_item_id=OuterRef('id')).values('price')[:1]
        items = queryset.annotate(
            price=Subquery(prices),
            brand=F("product__brand"),
            model=F("product__model"),
        )
        if q:
            items = get_product_items_full_filter(q, items)
        
        if category_id:
            category = get_active_category_queryset().filter(id=category_id).first()
            if not category:
                return False
            items = items.filter(product__category_id__in=get_category_and_children_id(category))
        return items

    def get(self, request):
        items = self.get_queryset()

        # category_tree
        category_tree = self.get_category_tree()

        # min price & max price
        price = self.get_min_max_prices(items.values("price"))

        # characteristics
        characteristics = self.get_characteristics(items.values('characteristics'))

        # models
        models = self.get_models(items.values('model'))

        # brands
        brands = self.get_brands(items.values('brand'))
        
        response = {
            "category_tree": category_tree if isinstance(category_tree, list) else category_tree,
            "min_price": price['min_price'],
            "max_price": price['max_price'],
            "brands": brands,
            "models": models,
            "characteristics": characteristics,
        }
        return Response(response)


class AdsProductItemsApi(APIView):

    def get(self, request):
        return Response({
            "status": True,
            "results": get_ads_products()
        })


class NewProductsApi(APIView):

    def get(self, request):
        return Response({
            "status": True,
            "results": get_new_products()
        })


class TopProductItemApi(APIView):

    def get(self, request):
        return Response({
            "status": True,
            "results": get_top_products()
        })


@api_view(['GET'])
def get_all_categories(request, *args, **kwargs):
    # categories = cache.get('all_categories')
    # if not categories:
    categories = get_all_active_category()
        # cache.set('all_categories', categories)
    return Response(categories)


class MainBannerApi(CustomListAPIView):
    queryset = get_active_main_banner()
    serializer_class = ClientMainBannerSerializer


class TopCategoryApi(CustomListAPIView):
    queryset = get_active_top_category()
    serializer_class = ClientTopCategorySerializer
