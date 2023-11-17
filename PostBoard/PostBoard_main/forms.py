from django import forms
from .models import Posts, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['category', 'headline', 'text']
        widgets = {'to_reg_user': forms.HiddenInput()}


class ResponseForm(forms.ModelForm):
    parent_response = forms.IntegerField(
        widget=forms.HiddenInput, required=False
    )

    class Meta:
        model = Response
        fields = ['text']
        widgets = {'res_user': forms.HiddenInput()}
