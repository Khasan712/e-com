import boto3, datetime, base64
from django.conf import settings
from botocore.exceptions import NoCredentialsError


def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY
    )


def upload_images(files, bucket):
    minio_client = get_minio_client()
    bucket = getattr(settings, bucket)
    images = []
    for file in files:
        f_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%f')
        object_name = f"{f_time}.{file.name.split('.')[-1]}" if len(file.name.split('.')) > 1 else f"{f_time}"
        minio_client.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=file
        )
        images.append({
            "bucket": bucket,
            "image": object_name,
            'url': f'{settings.IMAGE_PATH}/{bucket}/{object_name}'
        })
    return images


def product_upload_images(files, bucket):
    minio_client = get_minio_client()
    bucket = getattr(settings, bucket)
    images = []
    for file in files:
        f_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%f')
        object_name = f"{f_time}.{file['name'].split('.')[-1]}" if len(file['name'].split('.')) > 1 else f"{f_time}"
        minio_client.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=file['file']
        )
        images.append({
            "bucket": bucket,
            "image": object_name,
            'url': f'{settings.IMAGE_PATH}/{bucket}/{object_name}'
        })
    return images


def get_image_from_minio(bucket, image_name):
    minio_client = get_minio_client()
    response = minio_client.get_object(Bucket=bucket, Key=image_name)
    image_data = response['Body'].read()
    return image_data


def get_bucket_images(images):
    minio_client = get_minio_client()
    images_list = []
    for file in images:
        try:
            response = minio_client.get_object(Bucket=file['bucket'], Key=file['image'])
            image_data = response['Body'].read()
            image_base64 = base64.b64encode(image_data).decode()
            images_list.append({
                "image": image_base64,
                "image_name": file['image']
            })
        except NoCredentialsError:
            # print("No credentials provided to access MinIO.")
            pass
        except Exception as e:
            # print(f"Error fetching object '{file}' from MinIO: {e}")
            pass
    return images_list


def get_client_bucket_images(images):
    minio_client = get_minio_client()
    images_list = []
    for file in images:
        try:
            response = minio_client.get_object(Bucket=file['bucket'], Key=file['image'])
            image_data = response['Body'].read()
            image_base64 = base64.b64encode(image_data).decode()
            images_list.append(image_base64)
        except NoCredentialsError:
            # print("No credentials provided to access MinIO.")
            pass
        except Exception as e:
            # print(f"Error fetching object '{file}' from MinIO: {e}")
            pass
    return images_list
