from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from board.models import Post
from mentor.models import Question
from youth_policy.models import YouthPolicy

def popular_posts(request):
    """모든 템플릿에서 사용할 인기글 데이터를 제공하는 context processor"""
    
    # 지난 7일간 기준
    one_week_ago = timezone.now() - timedelta(days=7)
    
    # 지난 7일간 커뮤니티 인기글 (조회수 높은 순)
    popular_community_posts = Post.objects.filter(
        created_at__gte=one_week_ago
    ).order_by('-views')[:4]
    
    # 지난 7일간 멘토멘티 인기 질문글 (조회수 높은 순)
    popular_mentor_questions = Question.objects.filter(
        created_at__gte=one_week_ago
    ).order_by('-views')[:4]
    
    # 인기 청년정책 (조회수 높은 순)
    popular_youth_policies = YouthPolicy.objects.order_by('-view_count')[:5]
    
    return {
        'popular_community_posts': popular_community_posts,
        'popular_mentor_questions': popular_mentor_questions,
        'popular_youth_policies': popular_youth_policies,
    }