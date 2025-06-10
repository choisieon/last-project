from django.db import models
from django.conf import settings


class Sigungu(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    sido_name = models.CharField(max_length=20)  # 예: '경기도'

    def __str__(self):
        return self.name
    
    
class YouthPolicy(models.Model):
    name = models.CharField("정책명", max_length=255)
    description = models.TextField("정책설명")
    age_range = models.CharField("대상연령", max_length=50)
    keyword = models.CharField("정책키워드", max_length=100, blank=True)
    region = models.CharField("시행지역", max_length=200, blank=True)
    period = models.CharField("신청기간", max_length=200, blank=True)
    URL_ADD = models.URLField("신청URL", max_length=200, blank=True)
    major = models.CharField("대분류명", max_length=100, blank=True)  
    medium = models.CharField("중분류명", max_length=100, blank=True) 
    minage = models.IntegerField("최소연령", null=True, blank=True)  
    maxage = models.IntegerField("최대연령", null=True, blank=True) 
    addaply = models.TextField("추가신청자격조건내용", blank=True)
    document = models.TextField("제출서류내용", blank=True)
    etc = models.TextField("기타사항내용", blank=True)

    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_policies', blank=True)

    sigungu = models.ForeignKey(Sigungu, on_delete=models.CASCADE, related_name='policies', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def comment_count(self):
        return self.comments.count()
    

class Region(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class Sido(models.Model):
    code = models.CharField(max_length=2, primary_key=True)  # 예: '11'
    name = models.CharField(max_length=50)  # 예: '서울특별시'

    def __str__(self):
        return self.name
    
    
class PolicyComment(models.Model):
    policy = models.ForeignKey('YouthPolicy', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
