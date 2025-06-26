from django.shortcuts import render
from .models import Post
from mentor.models import MentorRequest, ChatRoom
from accounts.models import UserProfile

# Create your views here.

def index(request):
    posts = Post.objects.order_by('-created_at')  # 최신순 정렬

    return render(request, 'community/index.html', {'posts': posts,})