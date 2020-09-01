from django import forms

from discussion.models import Theme


class CreateThemeForm(forms.ModelForm):
    
    class Meta:
        model = Theme
        fields = ('theme', 'description')