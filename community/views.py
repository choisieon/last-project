from django.shortcuts import render
from mentor.models import MentorRequest, ChatRoom, Question
from accounts.models import UserProfile
from youth_policy.models import YouthPolicy
from board.models import Post
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone

def index(request):
    # 전체 게시글 최신순 정렬
    posts = Post.objects.order_by('-created_at')

    top_policies = YouthPolicy.objects.order_by('-view_count')[:3]

    # 지난 7일간 기준
    one_week_ago = timezone.now() - timedelta(days=7)

    # 지난 7일간 커뮤니티 인기글 (좋아요 많은 순)
    popular_community_posts = Post.objects.filter(
        created_at__gte=one_week_ago
    ).annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:5]

    # 지난 7일간 멘토멘티 인기 질문글 (좋아요 많은 순)
    popular_mentor_questions = (
        Question.objects.annotate(like_count=Count('likes'))
        .filter(like_count__gt=0)  # 좋아요 1개 이상인 질문만
        .order_by('-like_count')[:3]
    )

    return render(request, 'community/index.html', {
        'posts': posts,
        'popular_community_posts': popular_community_posts,
        'popular_mentor_questions': popular_mentor_questions,
        'top_policies': top_policies,
    })
