from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o%&=o*y*ew1%h$$$1a)9)gcv-y@c0htrpie(x$e1undd+z2%)('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    '*',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'community',
    'accounts',
    'board.apps.BoardConfig',   # 사용자 프로필/팔로우
    'tinymce',
    'taggit.apps.TaggitAppConfig',
    'taggit_templatetags2',
    'taggit_autosuggest',
    'youth_policy',

    'django.contrib.sites',  # 필수
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',  # 카카오 로그인
    'allauth.socialaccount.providers.naver',  # 네이버 로그인
    'allauth.socialaccount.providers.google', # 구글 로그인
    'mentor.apps.MentorConfig',
    'advice',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'chungsulmo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'board.context_processors.notification_counts',
                'chungsulmo_project.context_processors.popular_posts',
            ],
        },
    },
]

WSGI_APPLICATION = 'chungsulmo_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # collectstatic 명령으로 모일 경로

# 개발 시 static 파일 경로
STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static'),
]

AUTH_USER_MODEL = 'accounts.User'



SITE_ID = 2

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'   # 로그인 성공 시 이동 경로
LOGOUT_REDIRECT_URL = '/'  # 로그아웃 시 이동 경로

# TinyMCE self-hosted 설정
TINYMCE_JS_URL = '/static/tinymce/js/tinymce/tinymce.min.js'
TINYMCE_COMPRESSOR = False


# TINYMCE_DEFAULT_CONFIG = {
#     'height': 400,
#     'plugins': 'image,link,code',
#     'toolbar': 'undo redo | image link | code',
#     'images_upload_url': '/upload-image/',  # 이미지 업로드 URL
# }  


# TINYMCE_DEFAULT_CONFIG = {
#     'height': 600,
#     'plugins': '''
#         advlist autolink lists link image charmap preview anchor
#         pagebreak searchreplace wordcount visualblocks visualchars code
#         fullscreen insertdatetime media nonbreaking save table
#         directionality emoticons codesample
#     ''',
#     'toolbar1': '''
#         fullscreen preview bold italic underline | fontselect fontsizeselect | 
#         forecolor backcolor | alignleft alignright aligncenter alignjustify | 
#         indent outdent | bullist numlist table | link image media | codesample
#     ''',
#     'toolbar2': '''
#         visualblocks visualchars | charmap emoticons | insertdatetime
#         | hr nonbreaking | pagebreak restoredraft | code
#     ''',
#     'contextmenu': 'formats | link image',
#     'menubar': True,
#     'statusbar': True,
#     'theme_advanced_resizing': True,
#     'images_upload_url': '/board/upload-image/',
#     'width': '100%',
#     'language': 'ko_KR',
#     'language_url': '/static/tinymce/js/tinymce/langs/ko_KR.js',
# }


SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

LOGIN_URL = '/accounts/login/'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account'
        }
    },
    'kakao': {
        'SCOPE': ['profile_nickname'],
        'AUTH_PARAMS': {
            "response_type": "code",
            'prompt': 'login'
        },
    },
    'naver': {
        'SCOPE': ['name', 'email'],
        'AUTH_PARAMS': {
            "response_type": "code",
            'auth_type': 'reauthenticate'
        },
    }
}

