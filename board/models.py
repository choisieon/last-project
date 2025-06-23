from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager
from tinymce.models import HTMLField # ✅ TinyMCE용 필드 import


# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
    ('review', '후기'),
    ('share', '자료공유'),
    ('free', '잡담'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='free')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    tags = TaggableManager(blank=True)
    thumbnail = models.ImageField(upload_to='reviews/', null=True, blank=True)  # 후기 전용 썸네일(선택)
    is_blinded = models.BooleanField(default=False)  # 블라인드 여부

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_blinded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boardprofile')
    nickname = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followings', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('follower', 'following')

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications') # 알림 받을 사용자
    message = models.CharField(max_length=255)
    url = models.URLField(blank=True) # 알림 클릭 시 이동할 주소
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('user', 'post') # 같은 글 중복 저장 방지

class Report(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)  # 신고 사유 (선택)

    class Meta:
        unique_together = ('post', 'user')  # 중복 신고 방지

class CommentReport(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('comment', 'user')  # 중복 신고 방지

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/')  # 일반 파일 저장 경로
    image = models.ImageField(
        upload_to='images/',  # 이미지 전용 저장 경로
        null=True,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


