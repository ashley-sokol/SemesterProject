from django import forms
from .models import AnonReportInfo

class AnonymousForm(forms.Form):
     report_date = forms.DateField()
     report_text = forms.CharField()
     report_file = forms.FileField(required=False)


     # def cleaned_data(self):
     #    cleaned_data = super().clean()
     #    file = cleaned_data.get("report_file")

     #    if form.is_valid():



