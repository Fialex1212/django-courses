import boto3
from django.apps import AppConfig
from django.conf import settings
from django.core.files.storage import default_storage


class CoursesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "courses"

    def ready(self):
        # Берём конфиг из STORAGES (если используешь django-storages / S3Boto3Storage)
        storage_settings = getattr(settings, "STORAGES", {}).get("default", {}).get("OPTIONS", {})

        endpoint_url = storage_settings.get("endpoint_url")
        bucket_name = storage_settings.get("bucket_name")
        aws_access_key_id = storage_settings.get("access_key")
        aws_secret_access_key = storage_settings.get("secret_key")

        if not bucket_name or not endpoint_url:
            return 

        s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        try:
            s3.create_bucket(Bucket=bucket_name)
        except s3.exceptions.BucketAlreadyOwnedByYou:
            pass
        except s3.exceptions.BucketAlreadyExists:
            pass
