import base64

import boto3
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views import View
from .forms import AnonymousForm
from .models import AnonReportInfo
from django.http import FileResponse
from django.shortcuts import get_object_or_404

class LoginView(AuthLoginView):
    template_name = 'workplace_violation_app/login.html'

class IndexView(generic.View):
    form = AnonymousForm()
    template_name = 'workplace_violation_app/index.html'
    def get(self, request):
        form = AnonymousForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = AnonymousForm(request.POST,request.FILES)
        if form.is_valid():
            date = form.cleaned_data['report_date']
            text = form.cleaned_data['report_text']
            file = form.cleaned_data['report_file']

            anonymous_user = AnonReportInfo.objects.create(report_date =date,report_text=text,report_file=file)

            anonymous_user.save()

            return render(request, 'workplace_violation_app/submission.html')
        
        else:
            print("Form is not valid")
            print("Errors:", form.errors)
            
            return render(request, self.template_name, {'form':form})


class SubmissionsTableView(View):
    template_name = 'workplace_violation_app/submissions_table.html'
    def get(self, request, *args, **kwargs):
        file_path = kwargs.get('file_path')

        if file_path:
            report_file = get_object_or_404(AnonReportInfo, report_file=file_path)
            s3_url = report_file.url
            return HttpResponseRedirect(s3_url)

        submissions = AnonReportInfo.objects.all().order_by('-report_date')
        context = {'submissions': submissions}
        return render(request, self.template_name, context)