from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='mentor_profile')
    nickname = models.CharField(max_length=20)
    age_range = models.CharField(max_length=20, choices=[
        ('10s', '10대'), ('20s', '20대'), ('30s', '30대 이상')
    ])
    bio = models.TextField(blank=True)
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=True)

    # ✅ 온보딩용 필드 추가
    onboarding_complete = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=[('mentor', '멘토'), ('mentee', '멘티'), ('both', '둘다')], null=True, blank=True)
    concerns = models.ManyToManyField('Concern', blank=True)
    keywords = models.CharField(max_length=255, blank=True)  # 쉼표로 구분된 키워드 저장

    def __str__(self):
        return self.nickname

class Concern(models.Model):
    name = models.CharField(max_length=50)  # ex) 대학생활, 스펙, 인생, 연애

    def __str__(self):
        return self.name


# 멘토멘티 카테고리 선택
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

# 질문 모델
class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    is_promoted_to_mentoring = models.BooleanField(default=False)  # 멘토멘티 연결 여부

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# 답변 모델
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.author.nickname} → {self.question.title}"


# 멘토링 신청 모델
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


# 쪽지 모델
class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.nickname} → {self.receiver.nickname}"

