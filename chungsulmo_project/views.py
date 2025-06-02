# chungsulmo/views.py

from django.shortcuts import render
from django.db.models import Count
from board.models import Post

def index(request):
    popular_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')[:3]
    return render(request, 'community/index.html', {'popular_posts': popular_posts})