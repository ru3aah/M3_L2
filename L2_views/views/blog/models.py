from django.contrib.auth import get_user_model
from django.db import models
from .validators import validate_spam, CommentMaxLengthValidator
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    PUBLISHED = 'published'
    DRAFT = 'draft'
    ARCHIVED = 'archived'
    DELETED = 'deleted'

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=PUBLISHED)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(get_user_model(),
                               related_name='posts',
                               on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='posts',
                                 on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'id': self.pk})

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    content = models.TextField(validators=[validate_spam, 
                                           CommentMaxLengthValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), related_name='comments',
                                on_delete=models.CASCADE)
    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']





class Tag(models.Model):
    title = models.CharField(max_length=100, validators=[validate_spam])
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.title