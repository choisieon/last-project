from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import YouthPolicy, PolicyComment, Region, Sigungu, Sido

# Create your views here.
def basic_page(request):
    selected_sido = request.GET.get('sido')
    selected_sigungu = request.GET.get('sigungu')

    sido_list = Sido.objects.all().order_by('code')
    sigungu_list = Sigungu.objects.filter(code__startswith=selected_sido) if selected_sido else []

    policies = YouthPolicy.objects.all()
    if selected_sigungu:
        policies = policies.filter(sigungu__code=selected_sigungu)
    elif selected_sido:
        policies = policies.filter(sigungu__code__startswith=selected_sido)

    return render(request, 'basic_page.html', {
        'sido_list': sido_list,
        'sigungu_list': sigungu_list,
        'selected_sido': selected_sido,
        'selected_sigungu': selected_sigungu,
        'policies': policies,
    })

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


