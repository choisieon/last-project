from django.core.management.base import BaseCommand
from youth_policy.models import Region, YouthPolicy

class Command(BaseCommand):
    help = "YouthPolicy.region 문자열에 포함된 코드들을 Region 테이블로 이관"

    def handle(self, *args, **kwargs):
        all_codes = set()

        for policy in YouthPolicy.objects.all():
            if policy.region:
                codes = [code.strip() for code in policy.region.split(',') if code.strip()]
                all_codes.update(codes)

        created = 0
        for code in sorted(all_codes):
            region, created_flag = Region.objects.get_or_create(code=code)
            if created_flag:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created}개의 Region 레코드가 생성되었습니다."))
