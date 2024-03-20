from django import forms
from .models import Report

class AnonymousForm(forms.Form):
     report_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Enter date here.', 'class': 'form-control'}))
     report_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter detailed report here.', 'style': 'height: 300px;', 'class': 'form-control'}))
     report_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))


     # def cleaned_data(self):
     #    cleaned_data = super().clean()
     #    file = cleaned_data.get("report_file")
     
     #    if form.is_valid():

