from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentor_home, name='mentor_home'),
]