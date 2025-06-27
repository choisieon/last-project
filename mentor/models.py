from django.db import models
from django.conf import settings
from accounts.models import UserProfile  # ✅ UserProfile 통합본 사용

CATEGORY_CHOICES = [
    ('life', '인생선배'),
    ('college', '대학선배'),
    ('love', '연애선배'),
    ('house', '자취선배'),
    ('job', '취업선배'),
    ('money', '지갑선배'),
    ('fitness', '운동선배'),
    ('etc', '기타'),
]

category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='life')


class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    is_promoted_to_mentoring = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_questions', blank=True)
    curious = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='curious_questions', blank=True)



    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    is_adopted = models.BooleanField(default=False)
    good_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='good_answers', blank=True)
    soso_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='soso_answers', blank=True)
    bad_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bad_answers', blank=True)



    def __str__(self):
        return f"{self.author.nickname} → {self.question.title}"
    
    def good_count(self):
        return self.good_users.count()

    def soso_count(self):
        return self.soso_users.count()

    def bad_count(self):
        return self.bad_users.count()

class MentorRequest(models.Model):
    mentee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='requests_made')
    mentor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='requests_received')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    message = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mentee.nickname} → {self.mentor.nickname}"

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.nickname} → {self.receiver.nickname}"

class ChatRoom(models.Model):
    mentor_request = models.OneToOneField(MentorRequest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.nickname} – {self.content[:20]}"

class QuestionView(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} → {self.question} ({self.viewed_at})'

from django.db import models

class Concern(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name