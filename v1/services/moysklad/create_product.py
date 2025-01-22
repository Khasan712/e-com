from django.conf import settings
import requests
from v1.msklad.services import headers

url = settings.MOY_SKLAD_ENDPOINT


def create_product_moy_sklad(products: list):
    product_list = []
    for product in products:
        product_list.append(
            {
                "name": product['name'],
                "article": product['artikul'],
                "salePrices": [
                    {
                        "value": 0,
                        "priceType": {
                            "meta": {
                                "href": "https://online.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/b1293af6-3b4e-11ee-0a80-0e9600094508",
                                "type": "pricetype",
                                "mediaType": "application/json"
                            },
                            "id": "b1293af6-3b4e-11ee-0a80-0e9600094508",
                            "externalCode": "cbcf493b-55bc-11d9-848a-00112f43529a"
                        }
                    }
                ]
            },
        )
    id_list = []
    try:
        res = requests.post(url=url, headers=headers, json=product_list)
        for obj in res.json():
            data = {
                "id": obj['id'],
                "barcode": obj['barcodes'][0]['ean13'],
                "json_data": obj
            }
            id_list.append(data)
    except Exception as e:
        pass
    else:
        return id_list




