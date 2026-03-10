# yourapp/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, label="Имя", required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(max_length=20, label="Телефон", required=False)
    message = forms.CharField(widget=forms.Textarea, label="Сообщение", required=True)
