from django.shortcuts import render
from .models import Post

# Create your views here.


def index(request):
    posts = Post.objects.order_by('-created_at')  # 최신순 정렬
    return render(request, 'community/index.html', {'posts': posts})
