from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '프로필'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# 그냥 바로 등록
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'age', 'job', 'points', 'interests', 'tagline']
    search_fields = ['nickname', 'user__username']
    list_filter = ['age', 'role', 'is_mentor']