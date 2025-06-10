from django.core.management.base import BaseCommand
from youth_policy.models import Region, Sigungu

class Command(BaseCommand):
    help = "Region 테이블의 데이터를 Sigungu로 이관합니다."

    def handle(self, *args, **kwargs):
        count = 0
        for region in Region.objects.all():
            Sigungu.objects.get_or_create(code=region.code, name=region.name)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'{count}개의 시군구 데이터를 이관 완료했습니다.'))