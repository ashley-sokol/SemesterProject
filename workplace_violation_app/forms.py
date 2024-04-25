from django import forms
from .models import Report

class ReportForm(forms.Form):
     report_date = forms.DateField(help_text = "<small><em>Format: MM/DD/YYYY</small></em>", widget=forms.DateInput(attrs={'placeholder': 'Enter date here.', 'class': 'form-control'}))
     report_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter detailed report here.', 'style': 'height: 200px;', 'class': 'form-control'}))
     report_file = forms.FileField(help_text = "<small><em>Supported file extensions: .txt, .pdf, .jpg</em></small>", required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
     report = forms.BooleanField(widget=forms.HiddenInput, initial=True)

     # def cleaned_data(self):
     #    cleaned_data = super().clean()
     #    file = cleaned_data.get("report_file")
     
     #    if form.is_valid():

class SearchForm(forms.Form):
     case_number = forms.CharField(widget=forms.DateInput(attrs={'placeholder': 'Enter case number', 'class': 'mt-1'}))
     search = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class AdminNotesForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['admin_notes']
        widgets = {
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter notes here...'}),
        }
   
   
   
   
   

