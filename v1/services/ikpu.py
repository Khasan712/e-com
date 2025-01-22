from rest_framework.views import APIView
from v1.product.models import Ikpu
import requests, time
from rest_framework.response import Response

class IkpuSave(APIView):
    def post(self, request):
        flag = True
        page_no = 0
        page_size = 10
        while flag:
            url = f"https://tasnif.soliq.uz/api/cls-api/attribute/web-katalog?lang=uz_cyrl&pageNo={page_no}&pageSize={page_size}"
            res = requests.get(url)
            res = res.json()
            if res['data'] == []:
                flag = False
                break
            list_data=[]
            for item in res['data']:
                list_data.append(
                    Ikpu(
                        code=item['mxikCode'],
                        group=item['group'],
                        class_group=item['class_'],
                        position=item['position'],
                        sub_position=item['subPosition'],
                        brand=item['brand'],
                        title_ln=item['name']
                    )
                )
            time.sleep(5)
            Ikpu.objects.bulk_create(list_data)
            page_no+=1
            list_data = []
            time.sleep(10)
        return Response(
            {
                "status": True,
            }
        )

