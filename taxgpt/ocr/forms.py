# forms.py
from django import forms
from .models import ExtractedText

class ExtractedTextForm(forms.ModelForm):
    class Meta:
        model = ExtractedText
        fields = ['pdf_file']
