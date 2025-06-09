from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import YouthPolicy, PolicyComment, Region
from .utils import get_sido_code_list

# Create your views here.
def basic_page(request):
    policies = YouthPolicy.objects.all()
    return render(request, 'basic_page.html', {'policies': policies})

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

def region_view(request):
    selected_sido_code = request.GET.get('sido')
    selected_sigungu_code = request.GET.get('sigungu')

    sido_list = get_sido_code_list()

    sigungu_list = Region.objects.filter(code__startswith=selected_sido_code) if selected_sido_code else []
    filtered_policies = []

    if selected_sigungu_code:
        filtered_policies = YouthPolicy.objects.filter(region__regex=rf'(,|^){selected_sigungu_code}(,|$)')

    return render(request, '지역정책.html', {
        'sido_list': sido_list,
        'sigungu_list': sigungu_list,
        'policies': filtered_policies,
        'selected_sido_code': selected_sido_code,
        'selected_sigungu_code': selected_sigungu_code
    })
