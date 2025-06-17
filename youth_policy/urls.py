from django.urls import path
from . import views

app_name = 'youth_policy'

urlpatterns = [
    path('policy_list/', views.basic_page, name='basic_page'),
    path('<int:policy_id>/comment/', views.add_policy_comment, name='add_policy_comment'),
    path('<int:policy_id>/', views.policy_detail, name='policy_detail'),
    path('comment/<int:comment_id>/edit/', views.edit_policy_comment, name='edit_policy_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_policy_comment, name='delete_policy_comment'),
    path('weekly-pick/', views.weekly_pick_view, name='weekly_pick'),
    path('map/', views.map_view, name='policy_map'), # 새로 추가된 부분
]