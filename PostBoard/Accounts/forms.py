from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, mail_managers
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site

from PostBoard_main.models import RegUsers


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cleaned_data = None
            for field in self.fields:
                self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте свой ник'})
                self.fields['email'].widget.attrs.update({"placeholder": 'Введите свое мыло'})
                self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте свой пароль'})
                self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите придуманный пароль'})
                self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

        def clean_username(self):
            username = self.cleaned_data.get('username')
            try:
                User.objects.get(username=username)
                raise forms.ValidationError(
                    self.error_messages['Пользователь существует'],
                    code='Пользователь существует',
                )
            except User.DoesNotExist:
                return username


class ActivstionCodeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ActivstionCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!',
                                           'max_length': 'Максимальное количество символов 6'})

    # def save(self, commit=True):
    #     reg_user = super(ActivstionCodeForm, self).save(commit=False)
    #     user = RegUsers.objects.create(reg_user=reg_user)
    #     common_users = Group.objects.get(name='Зарегистрированные пользователи')
    #     user.groups.add(common_users)
    #     reg_user.code = self.cleaned_data['code']
    #
    #     if commit:
    #         common_users = Group.objects.get(name='Зарегистрированные пользователи')
    #         reg_user.groups.add(common_users)
    #         reg_user.save()
    #         return reg_user

    def save(self, request):
        user = super().save(request)
        user.code = self.cleaned_data['code']
        user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
            self.fields['username'].lable = 'Логин'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
