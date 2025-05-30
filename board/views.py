from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'board/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 로그인한 사용자
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'board/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session_key = f'viewed_{post.pk}'

    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True
    # 조회수 증가 (작성자 본인은 제외)
    if request.user != post.author:
        post.views += 1
        post.save()
    
    # 댓글 작성 처리
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'board/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
    })

@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:  # 이미 좋아요를 눌렀다면 취소
        like.delete()
    
    return redirect('post_detail', pk=post.pk)