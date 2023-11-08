from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Category, Posts, RegUsers, Subscriptions
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import User, Group
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views import View
# from .tasks import hello, printer
from django.utils.translation import gettext as _
from ckeditor_uploader.fields import RichTextUploadingField


class PostsList(ListView):
    raise_exception = True
    model = Posts
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now', 'is_reg'] = datetime.utcnow(), \
            self.request.user.groups.filter(name='Зарегистрированные пользователи').exists()
        return context


# class TanksList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'tanks.html'
#     context_object_name = 'tanks'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tanks'] = Posts.objects.filter(type_post='TK')
#         return context
#
#
# class HealersList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'healers.html'
#     context_object_name = 'healers'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['healers'] = Posts.objects.filter(type_post='HL')
#         return context
#
#
# class DDList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'DD.html'
#     context_object_name = 'DD'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['DD'] = Posts.objects.filter(type_post='DD')
#         return context
#
#
# class MerchantsList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'merchants.html'
#     context_object_name = 'merchants'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['merchants'] = Posts.objects.filter(type_post='MR')
#         return context
#
#
# class GMList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'GM.html'
#     context_object_name = 'GM'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['GM'] = Posts.objects.filter(type_post='GM')
#         return context
#
#
# class QuestGiveList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'quest.html'
#     context_object_name = 'quest'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['quest'] = Posts.objects.filter(type_post='QG')
#         return context
#
#
# class SmithsList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'smiths.html'
#     context_object_name = 'smiths'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['smiths'] = Posts.objects.filter(type_post='SM')
#         return context
#
#
# class LeatherList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'leather.html'
#     context_object_name = 'leather'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['leather'] = Posts.objects.filter(type_post='LW')
#         return context
#
#
# class PotionList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'potion.html'
#     context_object_name = 'potion'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['potion'] = Posts.objects.filter(type_post='PM')
#         return context
#
#
# class EnchantersList(ListView):
#     raise_exception = True
#     model = Posts
#     ordering = '-time_in'
#     template_name = 'enchanters.html'
#     context_object_name = 'enchanters'
#     paginate_by = 20
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['enchanters'] = Posts.objects.filter(type_post='EH')
#         return context


class SearchResults(ListView):
    raise_exception = True
    model = Posts
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    raise_exception = True
    model = Posts
    template_name = 'post_detail.html'
    context_object_name = 'post'


# class HealersDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'healers_detail.html'
#     context_object_name = 'healers'
#
#
# class DDDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'DD_detail.html'
#     context_object_name = 'DD'
#
#
# class MerchantsDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'merchants_detail.html'
#     context_object_name = 'merchants'
#
#
# class GMDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'GM_detail.html'
#     context_object_name = 'GM'
#
#
# class QuestGiveDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'quest_detail.html'
#     context_object_name = 'quest'
#
#
# class SmithsDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'smiths_detail.html'
#     context_object_name = 'smiths'
#
#
# class LeatherDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'leather_detail.html'
#     context_object_name = 'leather'
#
#
# class PotionDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'potion_detail.html'
#     context_object_name = 'potion'
#
#
# class EnchantersDetail(LoginRequiredMixin, DetailView):
#     raise_exception = True
#     model = Posts
#     template_name = 'enchanters_detail.html'
#     context_object_name = 'enchanters'


class PostCreate(CreateView):
    permission_required = ('PostBoard_main.add_post')
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_create.html'

    def form_valid(self, form):

        news_detail = form.save(commit=False)
        return super().form_valid(form)

    def post_create(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST, initial={'to_reg_user': self.request.user})
            if form.is_valid():
                form.to_reg_user = self.request.user
                form = form.save()
                return redirect(f'/posts/post_detail/')
            else:
                return render(request, 'posts/post_create.html', {'form': form})
        else:
            form = PostForm()
            return render(request, 'posts/post_create.html', {'form': form})


class PostUpdate(UpdateView):
    permission_required = ('PostBoard_main.change_post')
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    raise_exception = True
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
