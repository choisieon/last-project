# 경로: yourapp/management/commands/update_summary.py

from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy  # 앱 이름에 맞게 수정
from django.db.models import Q


class Command(BaseCommand):
    help = "'정책설명' 필드 내용을 요약하여 '정책설명요약' 필드에 저장합니다. 단, '정책설명요약'이 비어 있는 경우에만 수행됩니다."

    def handle(self, *args, **options):
        updated = 0

        policies = YouthPolicy.objects.filter(
            Q(정책설명__isnull=False) & ~Q(정책설명="") & (Q(정책설명요약__isnull=True) | Q(정책설명요약=""))
        )

        for policy in policies:
            description = policy.정책설명.strip().replace('\n', ' ')
            summary = description[:80] + "..." if len(description) > 80 else description
            policy.정책설명요약 = summary
            policy.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"✅ 총 {updated}개의 정책에 요약을 저장했습니다."))
