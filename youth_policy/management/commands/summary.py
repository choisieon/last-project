from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy

def generate_summary(description):
    if not description:
        return ""
    description = description.replace('\n', ' ').strip()
    if len(description) <= 60:
        return description
    return description.split('○')[0].split('※')[0].split('.')[0][:60].strip() + "..."

class Command(BaseCommand):
    help = "정책 설명 필드를 기반으로 간단한 요약 설명을 생성합니다."

    def handle(self, *args, **kwargs):
        policies = YouthPolicy.objects.all()
        count = 0
        for policy in policies:
            old = policy.정책설명요약
            new = generate_summary(policy.정책설명)
            if new and old != new:
                policy.정책설명요약 = new
                policy.save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f"✅ {count}건의 정책 요약 설명이 생성/업데이트되었습니다."))
