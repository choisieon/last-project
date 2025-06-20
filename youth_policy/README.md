1. management와 command를 사용하는 이유
: Django 프로젝트 안에서 직접 데이터를 자동으로 불러오거나 처리할 수 있도록 하기 위한 구조

2. 클론한 후 필수 명령어
- pip install -r requirements.txt
- python manage.py makemigrations/migrate
- python manage.py init_policy
- python manage.py init_regions
- python manage.py init_sido

<!-- - python manage.py fill_sido_to_youthpolicy
- python manage.py fill_sigungu_to_youthpolicy -->
-> django.db에 있는 전체 파일로 대체

# init_policy.py/init_regions.py는 엑셀 파일 바탕화면에 저장한 후 실행
# 순서 반드시 지킬 것
# 경로명은 로컬에 맞게 수정