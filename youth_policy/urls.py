from django.urls import path
from . import views

app_name = 'youth_policy'

urlpatterns = [
    path('policy_list/', views.basic_page, name='basic_page'),
    path('<int:policy_id>/', views.policy_detail, name='policy_detail'),
    path('<int:policy_id>/comment/', views.add_policy_comment, name='add_policy_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_policy_comment, name='edit_policy_comment'),
    path('policy/<int:policy_id>/like/', views.toggle_policy_like, name='toggle_policy_like'),
    path('comment/<int:comment_id>/delete/', views.delete_policy_comment, name='delete_policy_comment'),

    path('calendar/', views.calendar_view, name='calendar_view'),
    path('active-policies/', views.active_policy_list, name='active_policy_list'),

]