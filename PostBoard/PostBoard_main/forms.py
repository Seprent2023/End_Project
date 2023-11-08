from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['category', 'headline', 'text']
        widgets = {'to_reg_user': forms.HiddenInput()}
