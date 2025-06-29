from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # 회원가입 / 로그인 / 로그아웃
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # 프로필 관련
    path('profile/', views.my_page, name='my_page'),  # 메인 마이페이지
    path('profile/view/<int:user_id>/', views.view_profile, name='view_profile'),  # 다른 사람 프로필 보기
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # 수정
    path('profile/upload-avatar/', views.upload_avatar, name='upload_avatar'),  # ✅ 아바타 업로드 (URL 오류 방지)
    path('practice/', views.practice_page, name='practice'),  # ✅ 연습용 URL 추가
    path('add-life-event/', views.add_life_event, name='add_life_event'),  # ✅ 추가
    path('life_event/delete/<int:event_id>/', views.delete_life_event, name='delete_life_event'),  # ✅ 삭제
    path('social/', include('allauth.urls')),  # ✅ 요거 추가해야 {% provider_login_url %}이 동작함
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('toggle-popularity/<int:user_id>/', views.toggle_popularity, name='toggle_popularity'),

    # 필요 시 추후 소셜 로그인 연결도 여기에 추가
    # path('social/kakao/login/', views.social_login, name='social_login'),
    # path('social/kakao/logout/', views.social_logout, name='social_logout'),
]
