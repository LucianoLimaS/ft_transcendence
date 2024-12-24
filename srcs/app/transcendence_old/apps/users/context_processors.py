from django.conf import settings

def minio_settings(request):
    return {
        'MINIO_EXTERNAL_ENDPOINT': settings.MINIO_EXTERNAL_ENDPOINT,
        'MINIO_BUCKET_NAME': settings.MINIO_BUCKET_NAME,
    }