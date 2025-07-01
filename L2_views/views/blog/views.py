from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.db.models import Avg, F
from django.db.models.aggregates import Count, Min, Max
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .forms import ContactForm, PostForm, CommentForm
from .models import Post, Comment
from .mixins import MessageHandlerFormMixin, IsAuthorMixin

# Get the User model dynamically
User = get_user_model()


# Create your views here.
class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Post.objects.aggregate(
            total_posts=Count('pk'),
            average_views=Avg('views'),
            min_views=Min('views'),
            max_views=Max('views'),
            unique_authors=Count('author', distinct=True)
        )
        avg_views = stats.get('average_views', 0)
        if avg_views:
            avg_views = round(avg_views, 2)
        stats['average_views'] = avg_views
        
        context['stats'] = stats
        context['categories'] = Post.objects.values('category__title')
        return context


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # Add user's posts and comments to context if needed
        context['posts'] = user.posts.all().order_by('-created_at')
        context['comments'] = user.comments.all().order_by('-created_at')
        return context


class PostDetailView(DetailView):
    template_name = 'blog/post_details.html'
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.annotate(annotaded_views=F('views')+1)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views = F('views') + 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    ordering = ['-created_at']


class PostCreateView(LoginRequiredMixin, CreateView, MessageHandlerFormMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:post_details',
                       kwargs={'pk': self.object.pk})


class PostUpdateView(UpdateView, LoginRequiredMixin,
                     IsAuthorMixin, MessageHandlerFormMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'files': self.request.FILES,
            })
        return kwargs
    
    def get_success_url(self):
        return reverse('blog:post_details',
                       kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            raise PermissionError('You are not allowed to edit this post')
        return super().get(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class PostDeleteView( DeleteView, LoginRequiredMixin, IsAuthorMixin):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')


@login_required
def create_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_details', pk=post.id)
    return redirect('blog:post_details', pk=post.id)


def contacts(request: HttpRequest) -> HttpResponse:
    print(request.method)
    print(request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors)
            form.add_error(None, 'Form is not valid')
    else:
        form = ContactForm(request.GET)

    return render(request, 'blog/contacts.html',
                  {'form': form})


class DeleteCommentView(DeleteView, LoginRequiredMixin, IsAuthorMixin):
    model = Comment
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_details',
                            kwargs={'pk': self.object.post.id})