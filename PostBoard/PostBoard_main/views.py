from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Posts, Response, RegUsers, Category, Subscriptions
from .filters import PostFilter, ResponseFilter
from .forms import PostForm, ResponseForm
from django.contrib.auth.models import Group
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect


class PostsList(ListView):
    raise_exception = True
    model = Posts
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now', 'is_reg_user'] = datetime.utcnow(), \
            self.request.user.groups.filter(name='Зарегистрированные пользователи').exists()
        return context


class ResponseList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    ordering = '-time_in'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 20

    def get_queryset(self):
        queryset = Response.objects.filter(res_post__to_reg_user__reg_user=self.request.user.id).order_by('-time_in')
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_in'] = datetime.utcnow()
        context['filterset'] = self.filterset
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        form = ResponseForm()
        post = get_object_or_404(Posts, pk=pk)
        responses = post.reply.all()
        context['post'] = post
        context['responses'] = responses
        context['form'] = form
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('PostBoard_main.add_posts')
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_create.html'

    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST or None)

            if form.is_valid():
                f = form.save(commit=False)
                to_author = RegUsers.objects.get(reg_user_id=self.request.user.id)
                f.to_reg_user_id = to_author.id
                form.save()
                return redirect(f'/posts/')
            else:
                return render(request, 'posts/post_create.html', {'form': form})
        else:
            form = PostForm()
            return render(request, 'posts/post_create.html', {'form': form})


class ResponseCreate(LoginRequiredMixin, CreateView):
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
                return super().form_valid(form)
            else:
                return render(request, 'posts/response_create.html', {'form': form})
        else:
            form = ResponseForm()
            return render(request, 'posts/response_create.html', {'form': form})


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('PostBoard_main.delete_response')
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'


    def get_success_url(self):
        return self.request.GET.get('next', reverse('posts'))


class ResponseAccept(PermissionRequiredMixin, UpdateView):
    permission_required = ('PostBoard_main.change_response')
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_accept.html'

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            resp = Response.objects.get(id=pk)
            resp.status = True
            resp.save()
            return redirect(f'responses')
        else:
            return redirect(f'responses')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'PostBoard_main.change_posts'
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'PostBoard_main.delete_posts'
    raise_exception = True
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='Зарегистрированные пользователи')
    if not user.groups.filter(name='Зарегистрированные пользователи').exists():
        group.user_set.add(user)
        RegUsers.objects.create(reg_user=user)
    return redirect('posts')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)

        action = request.POST.get('action')
        if action == 'subscribe':
            Subscriptions.objects.create(user=request.user, to_category=category)
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(
                user=request.user,
                to_category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriptions.objects.filter(
                user=request.user,
                to_category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


def enter(request):
    return render(request, 'enter.html')


