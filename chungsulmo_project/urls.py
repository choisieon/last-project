
"""
URL configuration for chungsulmo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('allauth.urls')),  # allauth 기본 경로
    path('', include('community.urls')),  # community 앱으로 연결,
    path('accounts/', include('accounts.urls')),
    path('board/', include('board.urls', namespace='board')),
    path('mentor/', include('mentor.urls')),  # 멘토멘티 연결 추가
    path('tinymce/', include('tinymce.urls')),
    path('yputh_policy/', include('youth_policy.urls', namespace='youth_policy')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

