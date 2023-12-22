from django import forms
from my_project.models import Store
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('number', 'name', 'cost', 'location', 'literature')