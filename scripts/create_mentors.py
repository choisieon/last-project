from mentor.models import UserProfile
from django.contrib.auth.models import User

def create_mentors():
    for i in range(1, 21):  # 멘토 20명 생성
        user = User.objects.create(username=f'mentor{i}', password='password123')
        UserProfile.objects.create(
            user=user,
            nickname=f'멘토{i}',
            bio=f'멘토{i}의 소개입니다.',
            is_mentor=True,
            role='mentor',
            keywords='경험, 조언, 도움'
        )
    print("멘토 생성 완료!")

create_mentors() 