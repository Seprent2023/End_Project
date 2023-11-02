from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['to_reg_user', 'category', 'headline', 'text']