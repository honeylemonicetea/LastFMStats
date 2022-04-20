from django import forms
from .models import LastfmUser
from django.contrib.admin.widgets import AdminDateWidget

class LFMUser(forms.ModelForm):
    class Meta:
        model = LastfmUser
        fields = '__all__'
        widgets = {'date': forms.DateInput(attrs={'type':'date'})}