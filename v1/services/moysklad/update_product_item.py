from django.conf import settings
import base64, requests

url = settings.MOY_SKLAD_ENDPOINT
username = settings.MOY_SKLAD_USERNAME
password = settings.MOY_SKLAD_PASSWORD
basic_auth = base64.b64encode(f"{username}:{password}".encode()).decode()

headers = {
    'Authorization': f'Basic {basic_auth}',
}


def update_product_item(product):
    data = {
        "salePrices": [
            {
                "value": product['price']*100,
                "priceType": {
                    "meta": {
                        "href": "https://online.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/b1293af6-3b4e-11ee-0a80-0e9600094508",
                        "type": "pricetype",
                        "mediaType": "application/json"
                    },
                    "id": "b1293af6-3b4e-11ee-0a80-0e9600094508",
                    "name": "Цена продажи",
                    "externalCode": "cbcf493b-55bc-11d9-848a-00112f43529a"
                }
            }
        ]
    }
    requests.put(url=f"{url}/{product['moy_sklad_id']}", headers=headers, json=data)