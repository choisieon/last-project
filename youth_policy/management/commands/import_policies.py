from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy
import pandas as pd

class Command(BaseCommand):
    help = '엑셀 파일에서 청년정책 데이터를 불러옵니다.'

    def handle(self, *args, **kwargs):
        # 엑셀 파일 경로
        df = pd.read_excel(r'C:/Users/1-05/OneDrive/Desktop/청년정책_데이터.xlsx')

        # 기존 데이터 삭제 (선택사항)
        YouthPolicy.objects.all().delete()

        # 각 행을 순회하면서 데이터베이스에 저장
        for _, row in df.iterrows():
            YouthPolicy.objects.create(
                name=row['정책명'],
                description=row['정책설명'],
                age_range=row['대상연령'],
                keyword=row.get('정책키워드', ''),
                region=row.get('시행지역', ''),
                period=row.get('신청기간', ''),
                URL_ADD=row.get('신청URL', ''),
                major=row.get('대분류명', ''),
                medium=row.get('중분류명', ''),
                minage=row.get('최소연령', None),
                maxage=row.get('최대연령', None),
                addaply=row.get('추가신청자격조건내용', ''),
                document=row.get('제출서류내용', ''),
                etc=row.get('기타사항내용', '')
            )

        self.stdout.write(self.style.SUCCESS("✅ 청년정책 데이터 저장 완료"))