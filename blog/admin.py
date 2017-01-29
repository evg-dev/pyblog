from django.contrib import admin
from blog.models import Post, Category, Tag, Comment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
    list_display = ('name', 'slug')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
    list_display = ('name', 'slug')


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }
    list_display = ('title', 'category', 'get_tags', 'draft', 'created_at',
                    'published_at')
    list_display_links = ('title',)
    list_filter = ('created_at', 'published_at', 'draft')
    date_hierarchy = 'created_at'  # need install pytz!
    search_fields = ('title', 'tease', 'body')
    exclude = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'user_name': ('user_name',),
    }
    list_display = ('id', 'user_name', 'user_email',
                    'is_approved', 'post', 'created')
    date_hierarchy = 'created'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
