from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workplace_violation_app/', include('workplace_violation_app.urls')),
    path('accounts/', include('allauth.urls')),
]
