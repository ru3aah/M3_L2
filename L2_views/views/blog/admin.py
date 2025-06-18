from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Author, Tag, Category


class InlineCommentAdmin(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('content', 'author')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'created_at',
                    'updated')
    list_display_links = ('id',)
    list_editable = ('title', 'category', 'author')
    list_filter = ('status', 'author', 'category')
    search_fields = ('title', 'content')
    actions = ['publish', 'make_draft']
    inlines = [InlineCommentAdmin]

    fieldsets = (
            ('Basic data', {
                'fields': ('title', 'author', 'status', 'category', 'tags')
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
    readonly_fields = ('created_at', 'updated_at', 'updated')


    @admin.display(description='updated')
    def updated(self, post: Post):
        return 'not updated' if (post.updated_at.isoformat(timespec='minutes')
                                 ==
                                 post.created_at.isoformat(
                                     timespec='minutes')) else post.updated_at


    def publish(self, request, queryset):
        self.message_user(request, "Post has been published")
        queryset.update(status=Post.PUBLISHED)



    def make_draft(self, request, queryset):
        self.message_user(request, "Post has been unpublished")
        queryset.update(status=Post.DRAFT)


admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)





