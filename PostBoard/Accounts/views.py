from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm
# from PostBoard_main.models import RegUsers
# from django.shortcuts import redirect, render, get_object_or_404


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/Accounts/login'
    template_name = 'registration/signup.html'


# def register(request):
#     if request.methof == 'POST':
#         user_form = SignUpForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             RegUsers.objects.create(reg_user=new_user)
#             common_users = Group.objects.get(name='Зарегистрированные пользователи')
#             new_user.groups.add(common_users)
#             new_user.save()
#             return redirect(f'/posts/')
