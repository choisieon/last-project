from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist



class User(AbstractUser):
    # 여기에 추가 필드 넣을 수 있음
    pass
    @property
    def mentor_profile(self):
        try:
            return self.profile  # related_name 없으면 기본값은 소문자 모델명
        except ObjectDoesNotExist:
            return None    

class Concern(models.Model):
    name = models.CharField(max_length=50)  # ex) 대학생활, 스펙, 인생, 연애 등

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('mentor', '멘토'), ('mentee', '멘티'), ('both', '둘다')], null=True, blank=True)
    interests = models.TextField(blank=True)
    keywords = models.CharField(max_length=255, blank=True)

    # 👇 mentor 앱에서 쓰던 필드
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=True)
    onboarding_complete = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    concerns = models.ManyToManyField(Concern, blank=True)
    job = models.CharField(max_length=50, blank=True)  # ✅ 새로 추가
    tagline = models.CharField(max_length=100, blank=True)  # ✅ 새로 추가

    # 👇 여기부터 새로 추가되는 부분
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    avatar_image = models.ImageField(upload_to='avatar/', blank=True, null=True)
    avatar_edit_count = models.IntegerField(default=0)

    sido = models.ForeignKey('youth_policy.Sido', on_delete=models.SET_NULL, null=True, blank=True)
    sigungu = models.ForeignKey('youth_policy.Sigungu', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.nickname or self.user.username


class LifeEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    note = models.TextField()
    feeling = models.CharField(max_length=20)
    score = models.CharField(max_length=20)
    detail = models.TextField()