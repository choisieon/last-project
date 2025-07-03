from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import YouthPolicy, PolicyComment, Region, Sigungu, Sido
from .forms import CommentForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from collections import Counter
from datetime import date, datetime
from calendar import monthrange
import calendar
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
import json
from django.utils.dateformat import format as django_date_format
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def basic_page(request):
    stage = request.GET.get('stage')
    selected_sido = request.GET.get('sido')
    selected_sigungu = request.GET.get('sigungu')
    selected_category = request.GET.get('category', 'all')
    top_viewed_policies = YouthPolicy.objects.order_by('-view_count')[:10]

    policies = YouthPolicy.objects.all()

    if stage and stage != 'all':
        policies = policies.filter(생애주기단계__exact=stage)

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
        policies = policies.filter(sigungu__code=selected_sigungu)
    if selected_category != 'all':
        
        if selected_category == 'job':
            policies = policies.filter(Q(정책키워드__icontains='일자리'))
        elif selected_category == 'education':
            policies = policies.filter(Q(정책키워드__icontains='교육'))
        elif selected_category == 'welfare':
            policies = policies.filter(Q(정책키워드__icontains='금융복지') | Q(정책키워드__icontains='참여권리'))
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
        'stage': stage,
        'sido_list': sido_list,
        'sigungu_list': sigungu_list,
        'selected_sido': selected_sido,
        'selected_sigungu': selected_sigungu,
        'selected_category': selected_category, 
        'paginator': paginator, 
        'is_paginated': True,
        'top_viewed_policies': top_viewed_policies,
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
        parent_id = request.POST.get('parent_id')

        parent = PolicyComment.objects.filter(id=parent_id).first() if parent_id else None

        PolicyComment.objects.create(
            policy=policy,
            author=request.user,
            content=content,
            parent=parent
        )
    return redirect('youth_policy:policy_detail', policy_id=policy.id)

# 댓글 삭제
@login_required
def delete_policy_comment(request, comment_id):
    comment = get_object_or_404(PolicyComment, id=comment_id, author=request.user)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# 댓글 수정 (폼 + 처리)
@login_required
def edit_policy_comment(request, comment_id):
    comment = get_object_or_404(PolicyComment, id=comment_id)

    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()

        # 🔁 수정 완료 후 해당 정책 상세 페이지로 이동
        return redirect('youth_policy:policy_detail', policy_id=comment.policy.id)

    return render(request, 'edit_comment.html', {'comment': comment})

# views.py > policy_detail
def policy_detail(request, policy_id):
    form = CommentForm()
    policy = get_object_or_404(YouthPolicy, id=policy_id)
    policy.view_count += 1
    policy.save(update_fields=['view_count'])

    comments = PolicyComment.objects.filter(policy=policy, parent=None).order_by('-created_at')
    top_level_comments = PolicyComment.objects.filter(policy=policy, parent__isnull=True).select_related('author').prefetch_related('replies__author')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.policy = policy
            new_comment.user = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = PolicyComment.objects.get(id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()
            return redirect('post_detail', id=parent_id)

    return render(request, 'policy_detail.html', {
        'policy': policy,
        'comments': comments,
        'top_level_comments': top_level_comments,
        'form': form
    })

@login_required
def toggle_policy_like(request, policy_id):
    policy = get_object_or_404(YouthPolicy, id=policy_id)

    if request.user in policy.likes.all():
        policy.likes.remove(request.user)
    else:
        policy.likes.add(request.user)

    return redirect('youth_policy:policy_detail', policy_id=policy.id)

def get_calendar(year, month):
    cal = calendar.Calendar(firstweekday=6)
    return cal.monthdatescalendar(year, month)

from datetime import date
from collections import defaultdict
from django.utils.dateformat import format as django_date_format
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from .models import YouthPolicy
import calendar
import json

def calendar_view(request):
    today = date.today()

    # URL에서 year/month 파라미터 받아오기
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    start_of_month = date(year, month, 1)
    end_of_month = date(year, month, calendar.monthrange(year, month)[1])

    # 이번 달에 시작 또는 마감되는 정책
    policies = YouthPolicy.objects.filter(
        application_start__lte=end_of_month,
        application_end__gte=start_of_month
    )

    # 현재 진행 중인 정책: today가 신청 기간 사이에 포함되는 경우
    active_policies = YouthPolicy.objects.filter(
        application_start__lte=today,
        application_end__gte=today
    ).order_by('application_end')

    start_dict = {}
    end_dict = {}

    for policy in policies:
        if policy.application_start and start_of_month <= policy.application_start <= end_of_month:
            key = policy.application_start
            start_dict.setdefault(key, []).append(policy)

        if policy.application_end and start_of_month <= policy.application_end <= end_of_month:
            key = policy.application_end
            end_dict.setdefault(key, []).append(policy)

    calendar_data = get_calendar(year, month)

    calendar_json_dict = defaultdict(list)
    for date_obj, policies_list in start_dict.items():
        date_str = django_date_format(date_obj, 'Y-m-d')
        for p in policies_list:
            calendar_json_dict[date_str].append({
                'id': p.id,
                '정책명': p.정책명
            })

    for date_obj, policies_list in end_dict.items():
        date_str = django_date_format(date_obj, 'Y-m-d')
        for p in policies_list:
            calendar_json_dict[date_str].append({
                '정책명': p.정책명
            })

    context = {
        'year': year,
        'month': month,
        'today': today,
        'calendar': calendar_data,
        'policies': policies,
        'start_dict': start_dict,
        'end_dict': end_dict,
        'calendar_data_json': json.dumps(calendar_json_dict, cls=DjangoJSONEncoder),
        'active_policies': active_policies,  # ← 추가
    }

    return render(request, 'calendar.html', context)

def active_policy_list(request):
    today = timezone.localdate()
    policies = YouthPolicy.objects.filter(
        application_start__lte=today,
        application_end__gte=today
    ).order_by('application_end')

    return render(request, 'active_policy_list.html', {
        'policies': policies,
        'today': today
    })
