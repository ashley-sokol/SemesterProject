from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView

class LoginView(AuthLoginView):
    template_name = 'workplace_violation_app/login.html'

class LogoutView(AuthLogoutView):
    template_name = 'workplace_violation_app/login.html'

class IndexView(generic.View):
    template_name = 'workplace_violation_app/index.html'
    def get(self, request):
        return render(request, self.template_name)
