from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views import View
from .forms import AnonymousForm
from .models import AnonReportInfo

class LoginView(AuthLoginView):
    template_name = 'workplace_violation_app/login.html'

class IndexView(generic.View):
    form = AnonymousForm()
    template_name = 'workplace_violation_app/index.html'
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})
    
    def post(self,request):
        form = AnonymousForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['report_date']
            text = form.cleaned_data['report_text']
            image = form.cleaned_data['report_image']

            anonymous_user = AnonReportInfo.objects.create(report_date =date,report_text=text,report_image=image)

            anonymous_user.save()

            return HttpResponse("The data is saved. Thank you for your submission")
        
        form = AnonymousForm()
        return render(request, self.template_name, {'form': self.form})
        
class SubmissionsTableView(View):
    template_name = 'workplace_violation_app/submissions_table.html'
    def get(self, request):
        return render(request, self.template_name)
