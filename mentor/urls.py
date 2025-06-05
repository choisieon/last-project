from django.urls import path
from . import views

app_name = 'mentor'

urlpatterns = [
    path('', views.index, name='index'),  # 기본 홈
    path('mentor_home/', views.mentor_home, name='mentor_home'),  # 멘토홈
    path('question/new/', views.question_create, name='question_create'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/answer/', views.answer_create, name='answer_create'),
    path('request/', views.mentor_request, name='mentor_request'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('questions/', views.question_list, name='question_list'),
    path('list/', views.mentor_list, name='mentor_list'),
    path('request/<int:question_id>/', views.mentor_request, name='mentor_request'),
    path('profile/<int:userprofile_id>/', views.mentor_profile, name='mentor_profile'),
    path('request/direct/<int:mentor_id>/', views.mentor_request, name='mentor_request_direct'),
]


