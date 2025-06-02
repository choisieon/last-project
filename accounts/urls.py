from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # path('social/kakao/login', views.sociallogin, name='sociallogin'),
    # path('social/kakao/login', views.sociallogout, name='sociallogout')
]