from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class AnonReportInfo(models.Model):
    report_date = models.DateField()
    report_text = models.TextField(null=False, blank= False)
    report_image = models.ImageField()