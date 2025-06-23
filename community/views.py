from django.shortcuts import render
from .models import Post
from youth_policy.models import YouthPolicy
from mentor.models import MentorRequest, ChatRoom
from accounts.models import UserProfile

# Create your views here.

# def index(request):
#     posts = Post.objects.order_by('-created_at')  # 최신순 정렬
#     top_viewed_policies = YouthPolicy.objects.order_by('-view_count')[:3]
#     return render(request, 'community/index.html', {'posts': posts})


def index(request):
    posts = Post.objects.order_by('-created_at')  # 최신순 정렬
    top_viewed_policies = YouthPolicy.objects.order_by('-view_count')[:3] # 인기 청년정책(조회수)

    return render(request, 'community/index.html', {
        'posts': posts,
        'top_viewed_policies': top_viewed_policies,
    })