from django.urls import path
from .views import LoginView, IndexView

app_name = 'workplace_violation_app'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index'),
]
