from django import forms
from .models import AnonReportInfo

class AnonymousForm(forms.Form):
     report_date = forms.DateField()
     report_text = forms.CharField()
     report_image = forms.ImageField()


