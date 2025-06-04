from django.urls import path
from . import views

app_name = 'youth_policy'

urlpatterns = [
    path('policies/', views.basic_page, name='basic_page'),
]