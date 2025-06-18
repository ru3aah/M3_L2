from django.contrib import admin
from .models import Post, Comment, Author, Tag, Category

class InlineCommentAdmin(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('content', 'author')

class TagInline(admin.TabularInline):
    model = Tag.posts.through
    extra = 1
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'title', 'category', 'author', 'created_at',
                    'updated', 'display_tags')    
    list_display_links = ('id',)
    list_editable = ('title', 'category', 'author', 'status')
    list_filter = ('status', 'author', 'category')
    list_select_related = ('author', 'category')
    search_fields = ('title', 'content')
    actions = ['publish', 'make_draft']
    inlines = [InlineCommentAdmin, TagInline]

    fieldsets = (
            ('Basic data', {
                'fields': ('title', 'category', 'author', 'status')
            }),
            ('Post content', {
                'fields': ('content', 'views'),
                'classes': ('collapse',),
                'description': 'Post content'
            }),
            ('Dates', {
                'fields': ('created_at', 'updated_at', 'updated'),
                'classes': ('collapse',)
            }),
    )
    readonly_fields = ('created_at', 'updated_at', 'updated', 'display_tags')

    @admin.display(description='Last Updated')
    def updated(self, post: Post):
        is_updated = (post.updated_at.isoformat(timespec='minutes') !=
                      post.created_at.isoformat(timespec='minutes'))
        return post.updated_at if is_updated else 'not updated'

    @admin.display(description='Tags')
    def display_tags(self, post: Post):
        if not post.tags.exists():
            return 'No tags'    
        return '|'.join([tag.title for tag in post.tags.all()])

    def publish(self, request, queryset):
        count = queryset.count()
        queryset.update(status=Post.PUBLISHED)
        self.message_user(request,
                          f"{count} post{'s' if count != 1 else ''} " 
                                   f"{'have' if count != 1 else 'has'} been "
                                   f"published")

    def make_draft(self, request, queryset):
        count = queryset.count()
        queryset.update(status=Post.DRAFT)
        self.message_user(request,
                          f"{count} post{'s' if count != 1 else ''} "
                          f"{'have' if count != 1 else 'has'} been unpublished")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    filter_horizontal = ('posts',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'post', 'created_at')
    list_display_links = ('id', 'content')
    search_fields = ('content',)
    list_filter = ('author', 'post')

    def get_queryset(self, request):
        return (super().get_queryset(request).
                select_related('author', 'post'))

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'joined_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', )

#admin.site.register(Comment)
#admin.site.register(Author)
#admin.site.register(Category)