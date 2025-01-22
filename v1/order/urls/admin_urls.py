from v1.order.views.admin_views import OrderApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderApi)

urlpatterns = []+router.urls
