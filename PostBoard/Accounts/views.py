import random

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
# from django.views.generic.edit import CreateView
from django.views.generic import CreateView, TemplateView
from .forms import SignUpForm, ActivstionCodeForm, LoginForm
from django.core.mail import send_mail
from PostBoard_main.models import RegUsers
from django.shortcuts import redirect, render


def generate_code():
    random.seed()
    return str(random.randint(100000, 999999))


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/user_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        my_password1 = form.cleaned_data.get('password1')
        u_f = User.objects.get(username=username, email=email, is_active=False)
        code = generate_code()
        if RegUsers.objects.filter(code=code):
            code = generate_code()

        messages = code
        user = authenticate(username=username, email=email, password=my_password1)
        reg_user = RegUsers.objects.create(reg_user=u_f, code=code)

        send_mail(subject='Код подтверждения',
                  message=f'{username}! Для подтверждения введите код: {messages}, вы {reg_user, user}',
                  from_email=None, recipient_list=[email], fail_silently=False)

        return redirect('email_confirmation_sent')


def user_confirm_email_view(request):
    if request.method == 'POST':
        form = ActivstionCodeForm(request.POST)
        if form.is_valid():
            code_use = form.cleaned_data.get('code')
            if RegUsers.objects.filter(code=code_use):
                reg_user_code = RegUsers.objects.get(code=code_use)
            else:
                form.add_error(None, 'Код подтверждения не совпадает.')
                return render(request, 'registration/email_confirmation_sent.html', {'form': form})
            if reg_user_code.reg_user.is_active == False:
                common_users = Group.objects.get(name='Зарегистрированные пользователи')
                reg_user_code.reg_user.groups.add(common_users)
                reg_user_code.reg_user.is_active = True
                reg_user_code.reg_user.save()
                login(request, reg_user_code.reg_user, backend='django.contrib.auth.backends.ModelBackend')
                RegUsers.objects.all().update(code=None)
                return redirect('email_confirmed')
            else:
                form.add_error(None, 'Вы кто!?')
                return render(request, 'registration/email_confirmation_sent.html', {'form': form})
        else:
            return render(request, 'registration/email_confirmation_sent.html', {'form': form})
    else:
        form = ActivstionCodeForm()
        return render(request, 'registration/email_confirmation_sent.html', {'form': form})


class EmailConfirmationSentView(TemplateView):
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/user_login.html'
    next_page = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context