from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User, UserProfile
import requests
from django.core.files.base import ContentFile
# from .utils import generate_avatar  # 임시 주석 처리 
import base64
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import os
import io
from .models import LifeEvent

from django.contrib.auth import authenticate, login as auth_login

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 인증을 통해 backend 정보 포함된 user 객체 획득
            user = authenticate(request, username=username, password=raw_password)

            if user is not None:
                # UserProfile 생성
                UserProfile.objects.get_or_create(user=user)
                # 회원가입 완료 후 로그인 페이지로 리다이렉트
                return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # 안전하게 프로필 가져오거나 생성
            profile, created = UserProfile.objects.get_or_create(user=user)

            # 닉네임이 비어있으면 프로필 수정 페이지로
            if not profile.nickname or profile.nickname.strip() == "":
                return redirect('accounts:profile_edit')

            # 로그인 성공 후 이동할 경로
            next_url = request.GET.get('next')
            return redirect(next_url or 'community:index')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('community:index')


# ✅ accounts/views.py 안 profile_edit 뷰 수정
@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'generate_avatar':
            # 아바타 생성 처리
            avatar_prompt = request.POST.get('avatar_prompt', '').strip()
            if avatar_prompt:
                full_prompt = "pixel art style, full body, one person standing, Korean appearance, decent-looking, white background, facing slightly to the right, eyes looking toward front-right direction, proportions similar to MapleStory character"
                full_prompt += f", {avatar_prompt}"

                try:
                    response = openai.images.generate(
                        model="dall-e-3",
                        prompt=full_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1
                    )
                    image_url = response.data[0].url
                    image_response = requests.get(image_url)

                    if image_response.status_code == 200:
                        file_name = f"{request.user.username}_avatar.png"
                        profile.avatar_image.save(file_name, ContentFile(image_response.content), save=True)
                        profile.avatar_edit_count += 1
                        profile.save()
                except Exception as e:
                    print(f"[아바타 생성 오류] {str(e)}")
        
        elif action == 'save_profile':
            # 프로필 저장 처리
            profile.nickname = request.POST.get('nickname', '')
            profile.age = request.POST.get('age', '') or None
            profile.job = request.POST.get('job', '')
            profile.interests = request.POST.get('interests', '')
            profile.tagline = request.POST.get('tagline', '')
            profile.save()
            return redirect('accounts:my_page')
        
        elif action == 'edit_avatar':
            # 아바타 수정 처리
            avatar_prompt = request.POST.get('avatar_prompt', '').strip()
            if avatar_prompt:
                full_prompt = "pixel art style, full body, one person standing, Korean appearance, decent-looking, white background, facing slightly to the right, eyes looking toward front-right direction, proportions similar to MapleStory character"
                full_prompt += f", {avatar_prompt}"

                try:
                    response = openai.images.generate(
                        model="dall-e-3",
                        prompt=full_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1
                    )
                    image_url = response.data[0].url
                    image_response = requests.get(image_url)

                    if image_response.status_code == 200:
                        file_name = f"{request.user.username}_avatar.png"
                        profile.avatar_image.save(file_name, ContentFile(image_response.content), save=True)
                        profile.avatar_edit_count += 1
                        profile.save()
                except Exception as e:
                    print(f"[아바타 수정 오류] {str(e)}")
        
        elif action == 'delete_avatar':
            # 아바타 삭제 처리
            if profile.avatar_image:
                profile.avatar_image.delete()
                profile.save()

    return render(request, 'profile_edit.html', {'form': form})



from django.contrib.auth import get_user_model

@login_required
def view_profile(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return redirect('accounts:my_page')  # 존재하지 않으면 마이페이지로

    life_events = LifeEvent.objects.filter(user=user).order_by('date')
    
    others = [
        {"name": "은지(26)", "activity": "비영리 단체 활동 시작"},
        {"name": "민수(29)", "activity": "창업교육 수료 + 카페 창업 준비"},
        {"name": "유나(25)", "activity": "지방 공무원 시험 도전"}
    ]
    paths = []

    return render(request, 'profile.html', {
        'profile': profile,
        'life_events': life_events,
        'paths': paths,
        'others': others,
        'user': user,
    })

@login_required
def my_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    life_events = LifeEvent.objects.filter(user=request.user).order_by('date')

    others = [
        {"name": "은지(26)", "activity": "비영리 단체 활동 시작"},
        {"name": "민수(29)", "activity": "창업교육 수료 + 카페 창업 준비"},
        {"name": "유나(25)", "activity": "지방 공무원 시험 도전"}
    ]
    paths = []  # 구불구불 선 나중에

    return render(request, 'profile.html', {
        'profile': profile,
        'life_events': life_events,
        'paths': paths,
        'others': others,
        'user': request.user,
    })

@login_required
def update_profile(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)

            # ✅ 아바타 생성은 오직 최초 1회만! 이후에는 무시
            if profile.avatar_edit_count == 0:
                custom_detail = request.POST.get('avatar_prompt', '').strip()
                if custom_detail:
                    base_prompt = "pixel art character, full body, white background, moderately attractive Korean appearance, looking toward the front-right diagonal, one person only, maple story character proportions"
                    prompt = f"{base_prompt}, {custom_detail}"

                    try:
                        response = openai.images.generate(
                            model="dall-e-3",
                            prompt=prompt,
                            size="1024x1024",
                            quality="standard",
                            n=1
                        )
                        image_url = response.data[0].url
                        image_response = requests.get(image_url)

                        if image_response.status_code == 200:
                            file_name = f"{request.user.username}_avatar.png"
                            profile.avatar_image.save(file_name, ContentFile(image_response.content), save=True)
                            profile.avatar_edit_count = 1

                    except Exception as e:
                        print("아바타 생성 실패:", e)
                else:
                    print("프롬프트 없음 → 아바타 생성 안 함")
            else:
                # ✅ 입력이 있더라도 완전 무시함
                print("아바타 이미 생성됨 → 추가 생성을 막음")

            profile.save()
            return redirect('accounts:my_page')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

from django.conf import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

import io
from io import BytesIO
from django.core.files.base import ContentFile

@login_required
@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        profile = request.user.profile

        # 아바타 수정 횟수 제한 제거

        # ✅ 기본 프롬프트
        base_prompt = (
    "pixel art style, full body, one character, Korean appearance, "
    "white background, decent-looking, turned slightly to the right, "
    "eyes looking toward front-right direction, proportions similar to MapleStory character"
)

        # ✅ 사용자 세부사항만 입력받기
        custom_detail = request.POST.get('custom_detail', '').strip()
        prompt = base_prompt
        if custom_detail:
            prompt += f", {custom_detail}"

        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            image_response = requests.get(image_url)

            if image_response.status_code != 200:
                return HttpResponseBadRequest("Failed to fetch generated image.")

            file_name = f"{request.user.username}_avatar.png"
            profile.avatar_image.save(file_name, ContentFile(image_response.content), save=True)

            profile.avatar_edit_count += 1
            profile.save()

            return JsonResponse({
                "avatar_url": profile.avatar_image.url
            })

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid method")

@login_required
def toggle_popularity(request, user_id):
    if request.method == 'POST':
        try:
            target_user = User.objects.get(id=user_id)
            profile = target_user.userprofile
            
            # 현재 사용자가 이미 추천했는지 확인
            session_key = f'recommended_{user_id}'
            
            if request.session.get(session_key, False):
                # 이미 추천한 경우 - 추천 취소
                profile.popularity = max(0, profile.popularity - 1)
                request.session[session_key] = False
                action = 'removed'
            else:
                # 추천하지 않은 경우 - 추천 추가
                profile.popularity += 1
                request.session[session_key] = True
                action = 'added'
            
            profile.save()
            
            return JsonResponse({
                'success': True,
                'popularity': profile.popularity,
                'action': action
            })
            
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def practice_page(request):
    return render(request, 'practice.html')

def add_life_event(request):
    if request.method == 'POST':
        LifeEvent.objects.create(
            user=request.user,
            date=request.POST['date'],
            title=request.POST['title'],
            note=request.POST['note'],
            feeling=request.POST['feeling'],
            score=request.POST['score'],
            detail=request.POST['detail'],
        )
    return redirect('accounts:my_page')

@login_required
def delete_life_event(request, event_id):
    if request.method == 'POST':
        event = LifeEvent.objects.get(id=event_id, user=request.user)
        event.delete()
    return redirect('accounts:my_page')

from youth_policy.models import YouthPolicy
import random

def get_random_policies(request):
    try:
        all_policies = list(YouthPolicy.objects.all())
        if len(all_policies) >= 3:
            random_policies = random.sample(all_policies, 3)
        else:
            random_policies = all_policies
        
        policies_data = []
        for policy in random_policies:
            policies_data.append({
                'id': policy.id,
                'name': policy.정책명,
                'description': policy.정책설명요약 or policy.정책설명[:100] if policy.정책설명 else '설명 없음'
            })
        
        return JsonResponse({'policies': policies_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_policies_by_lifecycle(request):
    lifecycle = request.GET.get('lifecycle')
    if not lifecycle:
        return JsonResponse({'policies': []})
    
    try:
        policies = YouthPolicy.objects.filter(생애주기단계=lifecycle)[:5]
        policies_data = []
        for policy in policies:
            policies_data.append({
                'id': policy.id,
                'name': policy.정책명,
                'description': policy.정책설명요약 or policy.정책설명[:100] if policy.정책설명 else '설명 없음'
            })
        
        return JsonResponse({'policies': policies_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)