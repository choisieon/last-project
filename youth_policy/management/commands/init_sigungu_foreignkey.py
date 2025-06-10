from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy, Sigungu

class Command(BaseCommand):
    help = "YouthPolicy의 'region' 값을 기준으로 'sigungu' 외래키를 일괄 설정합니다. (여러 개일 경우 첫 번째 코드 사용)"

    def handle(self, *args, **kwargs):
        updated_count = 0
        failed_entries = []

        for policy in YouthPolicy.objects.all():
            if policy.region and not policy.sigungu:
                first_code = policy.region.split(',')[0].strip()
                try:
                    sigungu_obj = Sigungu.objects.get(code=first_code)
                    policy.sigungu = sigungu_obj
                    policy.save()
                    updated_count += 1
                except Sigungu.DoesNotExist:
                    failed_entries.append((policy.id, first_code))

        self.stdout.write(self.style.SUCCESS(f"성공적으로 {updated_count}개의 정책에 sigungu 외래키를 설정했습니다."))
        if failed_entries:
            self.stdout.write(self.style.WARNING(f"실패한 정책 ID / 코드 목록: {failed_entries}"))
