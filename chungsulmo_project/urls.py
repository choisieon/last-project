from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # 앱별 URL 등록
    path('', include('community.urls')),
    path('accounts/', include('accounts.urls')),  # ✅ accounts 내부에서 allauth 포함됨
    path('board/', include('board.urls')),
    path('mentor/', include('mentor.urls')),
    path('policy/', include('youth_policy.urls')),
    path('advice/', include('advice.urls')),
    path('accounts/', include('allauth.urls')),
]

# 미디어 파일 경로 처리
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
