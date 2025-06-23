from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

# Concern은 accounts에서 import!
from accounts.models import UserProfile, Concern

from mentor.models import Question, Answer, MentorRequest, Message, ChatRoom, ChatMessage

User = get_user_model()  # accounts.User 커스텀 유저 모델

# Concern 관리
@admin.register(Concern)
class ConcernAdmin(admin.ModelAdmin):
    list_display = ('name',)

# UserProfile을 User에 붙이기 위한 Inline
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '프로필 정보'

class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

# 이미 등록된 User 모델이면 해제 후 다시 등록
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)

# 나머지 모델 등록
# admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(MentorRequest)
admin.site.register(Message)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
