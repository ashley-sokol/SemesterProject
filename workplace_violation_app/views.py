from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views import View

class LoginView(AuthLoginView):
    template_name = 'workplace_violation_app/login.html'

class IndexView(generic.View):
    template_name = 'workplace_violation_app/index.html'
    def get(self, request):
        return render(request, self.template_name)

class SubmissionsTableView(View):
    template_name = 'workplace_violation_app/submissions_table.html'
    def get(self, request):
        return render(request, self.template_name)
