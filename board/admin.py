from django.contrib import admin
from .models import Post, PostImage, Notification, Profile


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_notice')
    list_filter = ('is_notice', 'category')
    search_fields = ('title', 'content')
    fields = ('category', 'author', 'title', 'content', 'thumbnail', 'is_blinded', 'is_notice')

# Profile 관리용 Admin 클래스 추가
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'bio')
    search_fields = ('user__username', 'nickname')
    list_filter = ('user',)

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
admin.site.register(Notification)
admin.site.register(Profile, ProfileAdmin)
