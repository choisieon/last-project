import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Prefetch
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Post, Comment, Profile, Follow, PostImage, Report, CommentReport, PostFile
from .forms import PostForm, CommentForm
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt   # CSRF 검증 우회
from django.core.files.storage import default_storage   # 파일 저장을 위해 필요
from .models import Notification, Bookmark
from taggit.models import Tag
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

# 게시글 목록 + 검색 + 정렬 + 페이지네이션
def post_list(request):
    sort = request.GET.get('sort', '')
    keyword = request.GET.get('keyword', '')
    search_type = request.GET.get('search_type', '')  # 검색 유형 추가
    category = request.GET.get('category', '')
    page = request.GET.get('page', 1)
    tag_filter = request.GET.getlist('tag', [])
    posts = Post.objects.all()
    
    # 카테고리 필터링
    if category:
        posts = posts.filter(category=category)
    
    # 검색 처리 (유형별)
    if keyword:
        if search_type == 'author':
            posts = posts.filter(author__username__icontains=keyword)
        elif search_type == 'tag':
            posts = posts.filter(tags__name__icontains=keyword)
        elif search_type == 'content':
            posts = posts.filter(content__icontains=keyword)
        else:  # 전체 검색
            posts = posts.filter(
                Q(title__icontains=keyword) |
                Q(content__icontains=keyword) |
                Q(author__username__icontains=keyword)
            )
    
    # 태그 필터링
    if tag_filter:
        posts = posts.filter(tags__name__in=tag_filter).distinct()
    
    # 정렬 처리
    if sort == 'likes':
        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    elif sort == 'comments':
        posts = posts.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created_at')
    elif sort == 'views':  # 조회수순 추가
        posts = posts.order_by('-views', '-created_at')
    else:
        posts = posts.order_by('-created_at')

    # 페이지네이션
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    # 주간 인기글: 지난 7일 동안의 글 중 좋아요 순으로 상위 10개
    one_week_ago = timezone.now() - timedelta(days=7)
    weekly_top_posts = Post.objects.filter(
        created_at__gte=one_week_ago
    ).annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:10]

    # 인기 태그
    popular_mentor_tags = Tag.objects.filter(name__in=['대학', '연애', '운동', '인생', '자취', '지갑', '취업', '정책'])

    fixed_posts = Post.objects.filter(is_notice=True).order_by('-created_at')[:5]
    
    return render(request, 'board/post_list.html', {
        'page_obj': page_obj,
        'sort': sort,
        'keyword': keyword,
        'search_type': search_type,  # 검색 유형 추가
        'category': category,
        'popular_mentor_tags': popular_mentor_tags,
        'tag_filter': tag_filter,
        'weekly_top_posts': weekly_top_posts,
        'fixed_posts': fixed_posts,
    })


# 게시글 작성
@login_required
def post_new(request):
    # 1. 카테고리 파라미터 추출 (GET/POST 요청 모두 처리)
    category = request.GET.get('category') or request.POST.get('category')
    
    # 2. 인기 태그 조회 (기존 기능 유지)
    popular_tags = Tag.objects.annotate(num_posts=models.Count('taggit_taggeditem_items')).order_by('-num_posts')[:10]

    # 3. POST 요청 처리 (글 생성 로직)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # files = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category  # 카테고리 설정
            post.save()
            form.save_m2m()
            
            # 4. 태그 처리
            tags_str = request.POST.get('tags', '')
            if tags_str:
                tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                post.tags.set(tag_list)
                
            # 5. 이미지 저장
            for f in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=f)

            # 파일 저장 (여기 추가!)
            for f in request.FILES.getlist('files'):
                PostFile.objects.create(post=post, file=f)
                
            # 6. 핵심 변경: 생성 후 해당 카테고리로 리다이렉트
            return redirect(f"{reverse('board:post_list')}?category={category}")
    
    # 7. GET 요청 처리 (기존 로직 유지)
    else:
        form = PostForm(initial={'category': category})
        form.instance = None
    
    # 8. 렌더링 (기존 로직 유지)
    return render(request, 'board/post_new.html', {
        'form': form, 
        'category': category, 
        'popular_tags': popular_tags,
    })


# 게시글 상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session_key = f'viewed_{post.pk}'
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = post.bookmark_set.filter(user=request.user).exists()
    
    # 조회수 증가 (작성자 본인 제외)
    if not request.session.get(session_key, False) and request.user != post.author:
        post.views += 1
        post.save()
        request.session[session_key] = True
    
    # 재귀 Prefetch 함수 정의 (최대 5단계 깊이)
    def recursive_prefetch(queryset, depth=0, max_depth=5):
        if depth >= max_depth:
            return queryset.annotate(report_count=Count('commentreport'))
        return queryset.annotate(report_count=Count('commentreport')).prefetch_related(
            Prefetch('replies', queryset=recursive_prefetch(Comment.objects.all(), depth+1, max_depth))
        )
    
    # 최상위 댓글 쿼리 (재귀 Prefetch 적용)
    comments = post.comments.filter(parent__isnull=True).annotate(
        report_count=Count('commentreport')
    ).prefetch_related(
        Prefetch('replies', queryset=recursive_prefetch(Comment.objects.all()))
    )
    
    # 댓글 폼 처리
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
        # 알림 생성 (작성자와 다른 경우)
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                message=f"'{post.title}' 글에 새로운 댓글이 달렸습니다.",
                url=reverse('board:post_detail', args=[post.pk])
            )
        return redirect(f'{reverse("board:post_detail", kwargs={"pk": pk})}#comment-{new_comment.id}')
    
    # 팔로우 상태 확인
    is_following = False
    if request.user.is_authenticated:
        User = get_user_model()
        author = post.author
        is_following = author.followers.filter(pk=request.user.pk).exists()
    
    # 게시글 신고 횟수
    report_count = Report.objects.filter(post=post).count()

    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'author': post.author,
        'is_following': is_following,
        'is_bookmarked': is_bookmarked,
        'report_count': report_count,
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
    # 1. 카테고리 파라미터 추출 (GET 요청에서)
    category = request.GET.get('category', '')
    
    # 2. 게시글 객체 가져오기
    post = get_object_or_404(Post, pk=pk)
    
    # 3. 작성자 검증
    if request.user != post.author:
        return redirect('board:post_detail', pk=pk)
    
    # 4. 인기 태그 조회 (기존 기능 유지)
    popular_tags = Tag.objects.annotate(num_posts=Count('taggit_taggeditem_items')).order_by('-num_posts')[:10]

    # 5. POST 요청 처리 (수정 로직)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            for f in request.FILES.getlist('files'):
                PostFile.objects.create(post=post, file=f)
            # 6. 핵심 변경: 수정 후 해당 카테고리로 리다이렉트
            return redirect(f"{reverse('board:post_detail', kwargs={'pk': pk})}?category={category}")
    
    # 7. GET 요청 처리 (기존 로직 유지)
    else:
        form = PostForm(instance=post)
    
    # 8. 렌더링 (기존 로직 유지)
    return render(request, 'board/post_edit.html', {
        'form': form,
        'post': post,
        'popular_tags': popular_tags
    })


# 게시글 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category = request.GET.get('category', '')  # 1. URL에서 카테고리 추출
    
    if request.user != post.author:  # 2. 작성자 검증
        return redirect('board:post_detail', pk=pk)
    
    if request.method == "POST":  # 3. 삭제 요청 처리
        post.delete()
        # 4. 카테고리 정보 포함한 리다이렉트 (핵심 변경점)
        if category:
            return redirect(f"{reverse('board:post_list')}?category={category}")
        return redirect('board:post_list')  # 카테고리 없을 시 기본
    
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


@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
        return JsonResponse({'bookmarked': bookmarked})
    return HttpResponseBadRequest()

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    return render(request,'board/tagged.html', {
        'tag': tag,
        'posts': posts,
    })

@login_required
def post_report(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # 1. 요청 본문 디코딩 및 JSON 파싱
            body_str = request.body.decode('utf-8')
            data = json.loads(body_str)
            reason = data.get('reason', '').strip()
            
            # 2. 신고 사유 유효성 검사
            if not reason:
                return JsonResponse({'success': False, 'message': '신고 사유를 입력해야 합니다.'})
                
            # 3. 게시글 조회
            post = get_object_or_404(Post, pk=pk)
            
            # 4. 자신의 글 신고 방지
            if post.author == request.user:
                return JsonResponse({'success': False, 'message': '자신의 글은 신고할 수 없습니다.'})
                
            # 5. 중복 신고 방지
            if Report.objects.filter(post=post, user=request.user).exists():
                return JsonResponse({'success': False, 'message': '이미 신고한 게시글입니다.'})
                
            # 6. 신고 내역 저장
            Report.objects.create(post=post, user=request.user, reason=reason)
            
            # 7. 신고 횟수 계산 및 블라인드 처리
            report_count = Report.objects.filter(post=post).count()
            blinded = report_count >= 5
            if blinded:
                post.is_blinded = True
                post.save()
                
            # 8. 성공 응답
            return JsonResponse({
                'success': True,
                'report_count': report_count,
                'blinded': blinded
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 JSON 형식입니다.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'서버 오류: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})

@login_required
def report_cancel(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Report.objects.filter(post=post, user=request.user).delete()
    messages.success(request, "신고가 취소되었습니다.")
    return redirect('board:post_detail', pk=pk)

@login_required
def comment_report(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # JSON 파싱
            data = json.loads(request.body.decode('utf-8'))
            reason = data.get('reason', '').strip()
            
            # 유효성 검사
            if not reason:
                return JsonResponse({'success': False, 'message': '신고 사유를 입력해야 합니다.'}, status=400)
                
            comment = get_object_or_404(Comment, pk=pk)
            
            # 조건 검사
            if comment.author == request.user:
                return JsonResponse({'success': False, 'message': '자신의 댓글은 신고할 수 없습니다.'}, status=400)
                
            if CommentReport.objects.filter(comment=comment, user=request.user).exists():
                return JsonResponse({'success': False, 'message': '이미 신고한 댓글입니다.'}, status=400)
            
            # 신고 처리
            CommentReport.objects.create(comment=comment, user=request.user, reason=reason)
            report_count = CommentReport.objects.filter(comment=comment).count()
            
            # 자동 블라인드 처리
            blinded = report_count >= 5
            if blinded and not comment.is_blinded:  # 최적화: 이미 블라인드된 댓글은 재처리 방지
                comment.is_blinded = True
                comment.save()
                
            return JsonResponse({
                'success': True,
                'report_count': report_count,
                'blinded': blinded
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 JSON 형식입니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'서버 오류: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'}, status=400)

