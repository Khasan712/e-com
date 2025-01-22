from django.conf import settings
import datetime
import requests
import base64
from v1.product.models import Cart


username = settings.MOY_SKLAD_USERNAME
password = settings.MOY_SKLAD_PASSWORD
basic_auth = base64.b64encode(f"{username}:{password}".encode()).decode()

headers = {
    'Authorization': f'Basic {basic_auth}',
}


def push_orders_to_moysklad_head():
    return {
        "name": f"{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%f')}",
        "code": settings.PUSH_ORDERS_CODE,
        "applicable": True,
        "vatEnabled": False,
        "agent": {
            "meta": {
                "href": settings.AGENT_HREF,
                "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/organization/metadata",
                "type": "organization",
                "mediaType": "application/json",
                "uuidHref": settings.AGENT_UUID_HREF
            }
        },
        "organization": {
            "meta": {
                "href": settings.ORGANIZATION_HREF,
                "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/organization/metadata",
                "type": "organization",
                "mediaType": "application/json",
                "uuidHref": settings.ORGANIZATION_UUID_HREF
            }
        }
    }


def push_orders_to_moysklad(carts: Cart):
    data = push_orders_to_moysklad_head()
    positions = [
        {
            "quantity": cart.quantity,
            "price": cart.price,
            "discount": 0,
            "vat": 0,
            "assortment": {
                "meta": {
                    "href": f"https://api.moysklad.ru/api/remap/1.2/entity/product/{cart.product.moy_sklad_id}",
                    "type": "product",
                    "mediaType": "application/json"
                }
            },
            "reserve": cart.quantity
        } for cart in carts
    ]
    data['positions'] = positions
    try:
        res = requests.post(
            url=settings.PUSH_ORDERS_ENDPOINT,
            headers=headers,
            json=data
        )
    except Exception as e:
        print(str(e))
    else:
        if res.status_code != 200:
            return False
        return res.json()
