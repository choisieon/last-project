from .models import Sigungu

def get_sido_code_list():
    sido_qs = Sigungu.objects.values('sido_name').distinct()
    sido_list = []
    for sido in sido_qs:
        # code는 시도명을 기준으로 앞 2자리 코드로 정의 (ex: '11' = 서울특별시)
        first_match = Sigungu.objects.filter(sido_name=sido['sido_name']).first()
        if first_match:
            sido_list.append((first_match.code[:2], sido['sido_name']))
    return sido_list
