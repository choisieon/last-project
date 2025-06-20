from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Question, Answer, MentorRequest, Message, Concern

# Concern 관리
@admin.register(Concern)
class ConcernAdmin(admin.ModelAdmin):
    list_display = ('name',)

# UserProfile을 User에 붙이기
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# ✅ 오류 방지: 먼저 등록됐는지 모르니 try-except로 감싸기
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# User + UserProfile 같이 등록
admin.site.register(User, CustomUserAdmin)

# 나머지 모델 등록
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(MentorRequest)
admin.site.register(Message)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from mentor.models import UserProfile  # UserProfile은 mentor.models에 있음

User = get_user_model()  # 👉 이게 accounts.User를 가져옴!

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '프로필 정보'

class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

# 이미 등록돼 있을 수 있으니 안전하게 try-except
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
