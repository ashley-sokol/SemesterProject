from django.db import models

# Create your models here.

class User(models.Model):
    google_auth_token = models.CharField(max_length=100, default="")
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=50, blank=False, default="")

    def __str__(self):
        return self.username
    
    def is_authenticated(self):
        return not self.google_auth_token == ""
