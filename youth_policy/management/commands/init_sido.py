# youth_policy/management/commands/init_sido.py

from django.core.management.base import BaseCommand
from youth_policy.models import Sido

class Command(BaseCommand):
    help = '시도 데이터를 초기화합니다.'

    def handle(self, *args, **options):
        sido_data = [
            ("11", "서울특별시"),
            ("26", "부산광역시"),
            ("27", "대구광역시"),
            ("28", "인천광역시"),
            ("29", "광주광역시"),
            ("30", "대전광역시"),
            ("31", "울산광역시"),
            ("36", "세종특별자치시"),
            ("41", "경기도"),
            ("43", "충청북도"),
            ("44", "충청남도"),
            ("46", "전라남도"),
            ("47", "경상북도"),
            ("48", "경상남도"),
            ("50", "제주특별자치도"),
            ("51", "강원특별자치도"),
            ("52", "전북특별자치도")
        ]

        for code, name in sido_data:
            Sido.objects.update_or_create(code=code, defaults={'name': name})

        self.stdout.write(self.style.SUCCESS('시도 데이터가 성공적으로 초기화되었습니다.'))
