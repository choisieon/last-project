from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    sort = request.GET.get('sort', '')
    if sort == 'likes':
        posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    elif sort == 'comments':
        posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts, 'sort': sort})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'board/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session_key = f'viewed_{post.pk}'

    # 조회수 증가 (작성자 본인 제외)
    if not request.session.get(session_key, False) and request.user != post.author:
        post.views += 1
        post.save()
        request.session[session_key] = True

    comments = post.comments.filter(parent__isnull=True)
    comment_form = CommentForm(request.POST or None)
    
    if request.method == 'POST' and comment_form.is_valid():
        parent_id = comment_form.cleaned_data.get('parent_id')
        parent = None
        
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id, post=post)
            except Comment.DoesNotExist:
                parent = None

        new_comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=comment_form.cleaned_data['content'],
            parent=parent
        )
        # 댓글 작성 후 해당 위치로 이동
        url = reverse('post_detail', kwargs={'pk': pk})
        return redirect(f'{url}#comment-{new_comment.id}')

    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return redirect('post_detail', pk=pk)

@login_required
@require_POST
def post_like_ajax(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    liked = False
    
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'count': post.likes.count(),
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)
    
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'board/post_confirm_delete.html', {'post': post})
