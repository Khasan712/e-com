from django.db import transaction
from v1.product.models import Characteristic, ProductItem
from v1.utilis.querysets.get_active_querysets import get_active_characteristics
from django.db import connection

