from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import auth
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Posts, Response
from .filters import PostFilter, ResponseFilter
from .forms import PostForm, ResponseForm
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
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
    response_form = ResponseForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.kwargs['pk']
    #     form = ResponseForm()
    #     resp = get_object_or_404(Response, pk=pk)
    #     responses = resp.res_post
    #     context['resp'] = resp
    #     context['responses'] = responses
    #     context['form'] = form
    #     return context

    def post_detail(self, request, response, **kwargs):
        response = get_object_or_404(Response, id=self.kwargs['res_post'])
        responses = response.responses.filter(active=True)
        response_form = ResponseForm
        return render(request, 'posts/post_detail.html',
                      {'response': response, 'responses': responses, 'response_form': response_form})

    # def post_detail(self, request, post, **kwargs):
    #     post = get_object_or_404(Posts, id=self.kwargs['res_post'])
    #     responses = post.reply.filter(active=True)
    #
    #     if request.method == 'POST':
    #         response_form = ResponseForm(data=request.POST)
    #         if response_form.is_valid():
    #             new_response = response_form.save(commit=False)
    #             new_response.post = post
    #             new_response.save()
    #     else:
    #         response_form = ResponseForm()
    #     return render(request, 'posts/post_detail.html', {'post': post, 'responses': responses,
    #     'response_form': response_form})

    # def get(self, request, **kwargs):
    #     post = get_object_or_404(Posts, id=self.kwargs['post_id'])
    #     context = {}
    #     context.update(csrf(request))
    #     user = auth.get_user(request)
    #     context = {'responses': post.response_set.all().order_by('path'), 'next': post.get_absolute_url()}
    #     if user.is_authenticated:
    #         context['form'] = self.response_form
    #     return render(template_name=self.template_name, context=context)


# @require_http_methods(["POST"])
# def post_response(request, res_post):
#     form = ResponseForm(request.POST)
#     post = get_object_or_404(Posts, id=res_post)
#
#     if form.is_valid():
#         response = Response()
#         response.path = []
#         response.res_post = post
#         response.res_user = auth.get_user(request)
#         response.text = form.cleaned_data['text']
#         response.save()
#         try:
#             response.path.extend(Posts.objects.get(id=form.cleaned_data['parent_response']).path)
#             response.path.append(response.id)
#         except ObjectDoesNotExist:
#             response.path.append(response.id)
#
#         response.save()
#
#     return redirect(post.get_absolute_url())


class PostCreate(CreateView):
    permission_required = ('PostBoard_main.add_post')
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_create.html'

    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST or None)
            if form.is_valid():
                f = form.save(commit=False)
                f.to_reg_user_id = self.request.user.id
                form.save()
                return redirect(f'/posts/')
            else :
                return render(request, 'posts/post_create.html', {'form': form})
        else :
            form = PostForm()
            return render(request, 'posts/post_create.html', {'form': form})


class ResponseCreate(CreateView):
    permission_required = ('PostBoard_main.add_response')
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            form = ResponseForm(request.POST or None)
            post_to_res = get_object_or_404(Posts, id=pk)
            if form.is_valid():
                f = form.save(commit=False)
                f.res_user_id = self.request.user.id
                f.res_post_id = post_to_res.id
                form.save()
                return redirect(f'/posts/')
            else:
                return render(request, 'posts/response_create.html', {'form': form})
        else:
            form = ResponseForm()
            return render(request, 'posts/response_create.html', {'form': form})


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
