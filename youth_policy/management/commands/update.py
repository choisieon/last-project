import re
from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy

class Command(BaseCommand):
    help = '신청기간 필드에서 ~ 이전의 문자열을 제거합니다.'

    def handle(self, *args, **options):
        updated = 0

        policies = YouthPolicy.objects.all()
        for policy in policies:
            original = policy.신청기간
            if original and '~' in original:
                try:
                    updated_period = original.split('~', 1)[1].strip()
                    policy.신청기간 = updated_period
                    policy.save()
                    updated += 1
                except Exception as e:
                    self.stderr.write(f"❌ 오류 - ID {policy.id}: {e}")
        
        self.stdout.write(self.style.SUCCESS(f"✅ 총 {updated}개 항목이 업데이트되었습니다."))
