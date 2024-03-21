from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class CustomS3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
class Report(models.Model): #previously anonreportinfo
    report_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    report_date = models.DateField()
    report_text = models.TextField(null=True, blank= False)
    report_file = models.FileField(storage=CustomS3Storage())    #Should save in Amazon s3 bucket
    report_status = models.CharField(max_length=100, default='New')  # status of report
    report_number=models.UUIDField(primary_key=True,editable=False, default=uuid.uuid4, unique=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Report from {self.report_date}"