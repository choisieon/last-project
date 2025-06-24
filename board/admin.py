from django.contrib import admin
from .models import Post, PostImage, Notification


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_notice')
    list_filter = ('is_notice', 'category')
    search_fields = ('title', 'content')
    fields = ('category', 'author', 'title', 'content', 'thumbnail', 'is_blinded', 'is_notice')

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Notification)
