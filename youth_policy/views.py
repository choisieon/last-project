from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import YouthPolicy, PolicyComment, Region, Sigungu, Sido, PolicyViewLog
from django.core.paginator import Paginator
from django.db.models import Q
from collections import Counter

# Create your views here.
def basic_page(request):
    stage = request.GET.get('stage') # map.html에서 넘어오는 stage 파라미터
    selected_sido = request.GET.get('sido')
    selected_sigungu = request.GET.get('sigungu')
    selected_category = request.GET.get('category', 'all')
    

    policies = YouthPolicy.objects.all()

    if stage and stage != 'all':
        policies = policies.filter(생애주기단계__icontains=stage) # 'contains' 대신 'icontains'를 사용하면 대소문자 구분 없이 검색 가능

    sido_list = Sido.objects.all().order_by('code')
    
    sigungu_list = []
    if selected_sido:
        # 시도 코드로 시군구 필터링 (앞 2자리 매칭)
        sigungu_list = Sigungu.objects.filter(
            code__startswith=selected_sido
        ).order_by('code')
    
    
    if selected_sido:
        policies = policies.filter(sido_id=selected_sido)
    if selected_sigungu:
        policies = policies.filter(sigungu_id=selected_sigungu)
    if selected_category != 'all':
        # 예시: 대분류 또는 키워드 필터링 구현
        # '정책키워드' 필드에 '일자리', '교육' 등이 포함되어 있다고 가정
        if selected_category == 'job':
            policies = policies.filter(Q(정책키워드__icontains='일자리'))
        elif selected_category == 'education':
            policies = policies.filter(Q(정책키워드__icontains='교육'))
        elif selected_category == 'welfare':
            policies = policies.filter(Q(정책키워드__icontains='복지문화') | Q(정책키워드__icontains='참여권리'))
        elif selected_category == 'housing':
            policies = policies.filter(Q(정책키워드__icontains='주거'))

    if 'sido' in request.GET and not selected_sigungu:
        # 시도만 선택되고 시군구가 없으면, 해당 시도의 시군구 목록만 보여줌
        pass

    paginator = Paginator(policies, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'policies': page_obj,
        'page_obj': page_obj,
        'stage': stage, # 현재 선택된 생애 주기 정보도 템플릿으로 전달
        'sido_list': sido_list,
        'sigungu_list': sigungu_list,
        'selected_sido': selected_sido,
        'selected_sigungu': selected_sigungu,
        'selected_category': selected_category,  # 현재 선택된 카테고리 전달
        'top_viewed_policies': YouthPolicy.objects.order_by('-view_count')[:3],
        'paginator': paginator,  # paginator 객체 추가
        'is_paginated': True,  # 항상 페이지네이션 표시
    }
    
    return render(request, 'basic_page.html', context)

def youth_policy_detail(request, policy_id):
    policy = get_object_or_404(YouthPolicy, id=policy_id)
    return render(request, 'youth_policies.html', {'policy': policy})

def get_next_most_viewed(policy_id):
    logs = PolicyViewLog.objects.order_by('viewed_at')
    user_sequences = {}

    for log in logs:
        user_sequences.setdefault(log.user_id, []).append(log.policy_id)

    next_policies = []
    for sequence in user_sequences.values():
        if policy_id in sequence:
            idx = sequence.index(policy_id)
            if idx + 1 < len(sequence):
                next_policies.append(sequence[idx + 1])

    counter = Counter(next_policies)
    most_common_ids = [pk for pk, _ in counter.most_common(5)]
    return YouthPolicy.objects.filter(id__in=most_common_ids)

# youth_policy/views.py

@login_required
def add_policy_comment(request, policy_id):
    policy = get_object_or_404(YouthPolicy, id=policy_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        PolicyComment.objects.create(policy=policy, author=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# views.py > policy_detail
def policy_detail(request, policy_id):
    policy = get_object_or_404(YouthPolicy, id=policy_id)
    policy.view_count += 1
    policy.save(update_fields=['view_count'])

    comments = policy.comments.filter(parent__isnull=True)
    recommended_policies = get_next_most_viewed(policy_id)
    top_viewed_policies = YouthPolicy.objects.order_by('-view_count')[:3]

    return render(request, 'policy_detail.html', {
        'policy': policy,
        'comments': comments,
        'recommended_policies': recommended_policies,
        'top_viewed_policies': top_viewed_policies,
    })


# 댓글 삭제
@login_required
def delete_policy_comment(request, comment_id):
    comment = get_object_or_404(PolicyComment, id=comment_id, author=request.user)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


# 댓글 수정 (폼 + 처리)
@login_required
def edit_policy_comment(request, comment_id):
    comment = get_object_or_404(PolicyComment, id=comment_id, author=request.user)

    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'edit_comment.html', {'comment': comment})

def weekly_pick_view(request):
    categories = ['일자리', '교육', '주거', '복지문화', '참여권리']
    weekly_picks_by_category = {}

    for category in categories:
        weekly_picks_by_category[category] = YouthPolicy.objects.filter(
            is_weekly_pick=True,
            정책키워드__icontains=category
        ).order_by('-id')[:5]

    return render(request, 'weekly_pick.html', {
        'weekly_picks_by_category': weekly_picks_by_category
    })

def map_view(request):
    """
    RPG 지도 페이지를 렌더링합니다.
    """
    return render(request, 'policy_map.html')