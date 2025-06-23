from django.urls import path
from . import views

app_name = 'advice'

urlpatterns = [
    path('', views.advice_center, name='center'),
    path('advice/', views.advice_center, name='advice_center'),
    
]