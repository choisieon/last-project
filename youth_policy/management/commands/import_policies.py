from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy
import pandas as pd

class Command(BaseCommand):
    help = '엑셀 파일에서 청년정책 데이터를 불러옵니다.'

    def handle(self, *args, **kwargs):
        df = pd.read_excel(r'C:/Users/1-05/OneDrive/Desktop/청년정책_데이터.xlsx')  # 엑셀 파일명은 실제 경로로 수정

        # 기존 데이터 초기화 (선택 사항)
        YouthPolicy.objects.all().delete()

        # 행별로 객체 생성
        for _, row in df.iterrows():
            YouthPolicy.objects.create(
                name=row['정책명'],
                description=row['정책설명'],
                age_range=row['대상연령'],
                keyword=row.get('정책키워드', ''),
                region=row.get('시행지역', '')
            )

        self.stdout.write(self.style.SUCCESS("✅ 청년정책 데이터 저장 완료"))
