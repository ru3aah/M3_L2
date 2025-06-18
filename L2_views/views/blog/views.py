from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Avg, F
from django.db.models.aggregates import Count, Min, Max
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .models import Post, Comment, Author


# Create your views here.
class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats =  Post.objects.aggregate(
            total_posts=Count('pk'),
            average_views = Avg('views'),
            min_views = Min('views'),
            max_views = Max('views'),
            unique_authors = Count('author',distinct=True)
        )
        stats['average_views'] = round(stats['average_views'], 2)
        context['stats'] = stats
        context['categories'] = Post.objects.values('category__title')
        return context



class PostDetailView(DetailView):
    template_name = 'blog/post_details.html'
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.annotate(annotaded_views=F('views')+1)


    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        obj.views = F('views') + 1
        obj.save()
        return obj


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    ordering = ['-created_at']

    #def get_queryset(self) -> QuerySet:
    #    return Post.objects.filter(is_published=True)
    # ordering = ['-created_at']

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content', 'status', 'author']
    #success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content', 'status']
    pk_url_kwarg = 'id'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')

def create_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(content=request.POST.get('content'),
                                     post=post, author=Author.objects.first())
    return redirect('blog:post_details',post.id)


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('posts').annotate(
            post_count = Count('posts')
        )
