from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Post, Comment, Profile, Follow, PostImage
from .forms import PostForm, CommentForm
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt   # CSRF 검증 우회
from django.core.files.storage import default_storage   # 파일 저장을 위해 필요
from .models import Notification

# 게시글 목록 + 검색 + 정렬 + 페이지네이션
def post_list(request):
    sort = request.GET.get('sort', '')
    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')
    page = request.GET.get('page', 1)
    
    posts = Post.objects.all()
    
    # 카테고리 필터링
    if category:
        posts = posts.filter(category=category)
    
    # 검색 처리
    if keyword:
        posts = posts.filter(
            Q(title__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(author__username__icontains=keyword)
        )
    # 정렬 처리
    if sort == 'likes':
        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    elif sort == 'comments':
        posts = posts.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created_at')
    else:
        posts = posts.order_by('-created_at')

    # 페이지네이션 적용
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    
    return render(request, 'board/post_list.html', {
        'posts': page_obj,
        'sort': sort,
        'keyword': keyword,
        'category': category,  # 현재 카테고리 템플릿에 전달
    })

# 게시글 작성
@login_required
def post_new(request):
    category = request.GET.get('category') or request.POST.get('category')
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category  # 필요시
            post.save()
            # 여러 장 이미지 저장
            for f in request.FILES.getlist('images'):  # ✅ getlist('images')
                PostImage.objects.create(post=post, image=f)
            return redirect('board:post_list')
    else:
        form = PostForm(initial={'category': category})
    return render(request, 'board/post_new.html', {'form': form, 'category': category})

# 게시글 상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session_key = f'viewed_{post.pk}'
    # 조회수 증가 (작성자 본인 제외)
    if not request.session.get(session_key, False) and request.user != post.author:
        post.views += 1
        post.save()
        request.session[session_key] = True
    # 댓글 처리
    comments = post.comments.filter(parent__isnull=True)
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        parent_id = request.POST.get('parent_id')
        parent = Comment.objects.get(id=parent_id) if parent_id else None
        new_comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=comment_form.cleaned_data['content'],
            parent=parent
        )
        # 알림 생성 코드 추가
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                message=f"'{post.title}' 글에 새로운 댓글이 달렸습니다.",
                url=reverse('board:post_detail', args=[post.pk])
            )
        return redirect(f'{reverse("board:post_detail", kwargs={"pk": pk})}#comment-{new_comment.id}')
    # 팔로우 상태 확인 (로그인한 경우에만)
    is_following = False
    if request.user.is_authenticated:
        User = get_user_model()
        author = post.author
        is_following = author.followers.filter(pk=request.user.pk).exists()
    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'author': post.author,
        'is_following': is_following,
    })

# 좋아요 (페이지 리로드)
@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return redirect('board:post_detail', pk=pk)

# 좋아요 (AJAX)
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

# 게시글 수정
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('board:post_detail', pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_edit.html', {'form': form, 'post': post})

# 게시글 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('board:post_detail', pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('board:post_list')
    return render(request, 'board/post_confirm_delete.html', {'post': post})

# 댓글 수정
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return redirect('board:post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('board:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'board/comment_edit.html', {'form': form, 'comment': comment})

# 댓글 삭제
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
    return redirect('board:post_detail', pk=post_pk)

# 프로필 페이지
def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()
    followers = user_obj.follower_set.count()
    following = user_obj.following_set.count()
    return render(request, 'profile.html', {
        'profile_user': user_obj,
        'profile': profile,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    })

# 팔로우/언팔로우 토글
@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if request.user == target:
        return redirect('profile', username=target.username)
    
    # 팔로우 여부 확인 (related_name 주의!)
    is_following = Follow.objects.filter(
        follower=request.user, 
        following=target
    ).exists()
    
    if is_following:
        Follow.objects.filter(follower=request.user, following=target).delete()
    else:
        Follow.objects.create(follower=request.user, following=target)
    
    return redirect('profile', username=target.username)

def index(request):
    posts = Post.objects.order_by('-created_at')   # 최신순 정렬
    return render(request, 'board/index.html', {'posts': posts})

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # 파일 저장 (예: media/uploads/ 경로에 저장)
        file_name = default_storage.save(f'uploads/{file.name}', file)
        # 저장된 파일의 URL 생성 (예: /media/uploads/파일명.jpg)
        url = default_storage.url(file_name)
        return JsonResponse({'location': url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# def create_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             # 글 작성자에게 알림 생성 (자기 댓글은 제외)
#             if post.author != request.user:
#                 Notification.objects.create(
#                     user=post.author,
#                     message=f"'{post.title}' 글에 새로운 댓글이 달렸습니다.",
#                     url=reverse('board:post_detail', args=[post.id])
#                 )
#             return redirect('board:post_detail', post_id=post.id)

def notification_read(request, noti_id):
    noti = get_object_or_404(Notification, id=noti_id, user=request.user)
    noti.is_read = True
    noti.save()
    return redirect(noti.url)


@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'board/notification_list.html', {
        'notifications': notifications,
    })
