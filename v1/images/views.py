from rest_framework.decorators import api_view
from v1.services.minio_connect import get_image_from_minio
from django.http import HttpResponse
from django.core.cache import cache


@api_view(['GET'])
def get_image(request, bucket, image_name):
    image = cache.get(f'{bucket}_{image_name}')
    if not image:
        image = get_image_from_minio(bucket, image_name)
        cache.set(f'{bucket}_{image_name}', image)

    content_type = cache.get(f"content_type_{bucket}_{image_name}")
    if not content_type:
        content_type = image_name.split('.')[-1] if len(image_name.split('.')) > 1 else image_name
        cache.set(f"content_type_{bucket}_{image_name}", content_type)

    response = HttpResponse(image, content_type=f"image/{content_type}")
    return response
