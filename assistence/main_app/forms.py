# your_project/your_app/forms.py
from django import forms


class TextToSpeechForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Enter Text')
