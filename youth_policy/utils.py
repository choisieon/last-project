# utils.py

SIDO_MAP = {
    '11': '서울특별시',
    '26': '부산광역시',
    '27': '대구광역시',
    '28': '인천광역시',
    '29': '광주광역시',
    '30': '대전광역시',
    '31': '울산광역시',
    '36': '세종특별자치시',
    '41': '경기도',
    '42': '강원특별자치도',
    '43': '충청북도',
    '44': '충청남도',
    '45': '전라북도',
    '46': '전라남도',
    '47': '경상북도',
    '48': '경상남도',
    '50': '제주특별자치도',
}

from .models import Region

def get_sido_code_list():
    region_codes = Region.objects.values_list('code', flat=True)
    sido_codes = sorted(set(code[:2] for code in region_codes))
    return [(code, SIDO_MAP.get(code, f"시도코드:{code}")) for code in sido_codes]
