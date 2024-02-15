from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workplace_violation_app/', include('workplace_violation_app.urls')),
]
