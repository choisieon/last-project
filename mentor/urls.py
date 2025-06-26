from django.urls import path
from . import views

app_name = 'mentor'

urlpatterns = [
    path('', views.index, name='index'),
    path('mentor_home/', views.mentor_home, name='mentor_home'),

    # 문답
    path('questions/', views.question_list, name='question_list'),
    path('question/new/', views.question_create, name='question_create'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/answer/', views.answer_create, name='answer_create'),

    # 멘토링 신청
    path('request/', views.mentor_request, name='mentor_request_blank'),  # 폼만 보이는 기본
    path('request/question/<int:question_id>/', views.mentor_request, name='mentor_request_with_question'),
    path('request/direct/<int:mentor_id>/', views.mentor_request_direct, name='mentor_request_direct'),
    

    # 기타
    path('onboarding/', views.onboarding, name='onboarding'),
    path('list/', views.mentor_list, name='mentor_list'),
    path('profile/<int:userprofile_id>/', views.mentor_profile, name='mentor_profile'),

    path('requests/received/', views.mentor_requests_received, name='mentor_requests_received'),
    path('request/accept/<int:request_id>/', views.accept_mentor_request, name='accept_mentor_request'),
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('chat/my_rooms/', views.my_chat_rooms, name='my_chat_rooms'),
    path('question/<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('answer/<int:pk>/delete/', views.answer_delete, name='answer_delete'),
    path('chat/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('chat/delete/<int:chatroom_id>/', views.delete_chatroom, name='delete_chatroom'),
        path('question/<int:pk>/like/', views.question_like, name='question_like'),
    path('answer/<int:answer_id>/comment/', views.comment_create, name='comment_create'),
    path('question/<int:pk>/like/', views.question_like, name='question_like'),
    path('question/<int:pk>/curious/', views.question_curious, name='question_curious'),
      path('request/delete/<int:request_id>/', views.delete_mentor_request, name='delete_mentor_request'),
      path('chatroom/delete_selected/', views.delete_selected_chatrooms, name='delete_chatrooms'),
     path('chatrooms/delete/', views.delete_chatrooms, name='delete_chatrooms'),
    path('answer/<int:answer_id>/adopt/', views.answer_adopt, name='answer_adopt'),
    path('answer/<int:answer_id>/evaluate/', views.answer_evaluate, name='answer_evaluate'),

    ]
