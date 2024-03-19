from django.db import models
from django.contrib.auth.models import AbstractUser, User
from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class CustomS3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
class Report(models.Model):
    report_date = models.DateField()
    report_text = models.TextField(null=False, blank= False)
    report_file = models.FileField(storage=CustomS3Storage())    #Should save in Amazon s3 bucket

    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Report from {self.report_date}"