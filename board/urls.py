from django.urls import path, re_path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/like_ajax/', views.post_like_ajax, name='post_like_ajax'),  # AJAX용 새 경로
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    # path('', views.index, name='index'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('notifications/read/<int:noti_id>/', views.notification_read, name='notifications_read'),
    path('notifications/all/', views.notification_list, name='notifications_all'),
    path('bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    re_path(r'^tag/(?P<slug>[\w\-가-힣]+)/$', views.tagged, name='tagged'),
    path('post/<int:pk>/report/', views.post_report, name='post_report'),
    path('post/<int:pk>/report/cancel/', views.report_cancel, name='report_cancel'),
    path('comment/<int:pk>/report/', views.comment_report, name='comment_report'),
]
