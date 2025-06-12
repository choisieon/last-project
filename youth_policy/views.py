from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import YouthPolicy, PolicyComment, Region, Sigungu, Sido
from django.core.paginator import Paginator

# Create your views here.
def basic_page(request):
    selected_sido = request.GET.get('sido')
    selected_sigungu = request.GET.get('sigungu')
    
    sido_list = Sido.objects.all().order_by('code')
    
    sigungu_list = []
    if selected_sido:
        # 시도 코드로 시군구 필터링 (앞 2자리 매칭)
        sigungu_list = Sigungu.objects.filter(
            code__startswith=selected_sido
        ).order_by('code')
    
    # 정책 필터링도 마찬가지로 수정
    policies = YouthPolicy.objects.all()
    
    if selected_sido:
        policies = policies.filter(sido_id=selected_sido)
    if selected_sigungu:
        policies = policies.filter(sigungu_id=selected_sigungu)


    if 'sido' in request.GET and not selected_sigungu:
        # 시도만 선택되고 시군구가 없으면, 해당 시도의 시군구 목록만 보여줌
        pass

    paginator = Paginator(policies, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'policies': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'sido_list': sido_list,
        'sigungu_list': sigungu_list,
        'selected_sido': selected_sido,
        'selected_sigungu': selected_sigungu,
    }
    
    return render(request, 'basic_page.html', context)

def youth_policy_detail(request, policy_id):
    policy = get_object_or_404(YouthPolicy, id=policy_id)
    return render(request, 'youth_policies.html', {'policy': policy})

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
    return render(request, 'policy_detail.html', {
        'policy': policy,
        'comments': comments,
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