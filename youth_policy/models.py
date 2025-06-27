from django.db import models
from django.conf import settings


class Sigungu(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    sido_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    
class YouthPolicy(models.Model):
    정책명 = models.CharField(max_length=255, default="데이터 변경")
    정책설명 = models.TextField(blank=True, null=True)
    대상연령 = models.CharField(max_length=100, blank=True, null=True)
    정책키워드 = models.CharField(max_length=600, blank=True, null=True)
    시행지역 = models.CharField(max_length=600, blank=True, null=True)
    application_period = models.CharField("신청기간", max_length=255, blank=True, null=True)
    application_start = models.DateField("신청 시작일", blank=True, null=True)
    application_end = models.DateField("신청 마감일", blank=True, null=True)
    신청URL = models.URLField(blank=True, null=True)
    추가신청자격조건내용 = models.TextField(blank=True, null=True)
    제출서류내용 = models.TextField(blank=True, null=True)
    참여제외대상 = models.TextField(blank=True, null=True)
    생애주기단계 = models.TextField(blank=True, null=True)
    정책설명요약 =  models.TextField(blank=True, null=True)

    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_policies', blank=True)

    sido = models.ForeignKey('Sido', on_delete=models.CASCADE, null=True, blank=True)
    sigungu = models.ManyToManyField('Sigungu', blank=True)

    def __str__(self):
        return self.정책명
    
    def comment_count(self):
        return self.comments.count()
    
class Sido(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
        
class Region(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    
class PolicyComment(models.Model):
    policy = models.ForeignKey('YouthPolicy', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"