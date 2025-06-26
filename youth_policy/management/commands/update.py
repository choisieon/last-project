import pandas as pd
from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy

class Command(BaseCommand):
    help = '엑셀에서 신청기간 데이터를 읽어 application_period에 채워 넣습니다 (기존 값이 없는 경우만)'

    def handle(self, *args, **kwargs):
        excel_path = r"C:\Users\1-05\OneDrive\Desktop\병합결과_최종.xlsx"

        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'엑셀 파일을 불러오는 데 실패했습니다: {e}'))
            return

        update_count = 0
        for _, row in df.iterrows():
            try:
                policy = YouthPolicy.objects.get(id=row['id'])
                if not policy.application_period and pd.notna(row['신청기간']):
                    policy.application_period = str(row['신청기간'])
                    policy.save()
                    update_count += 1
            except YouthPolicy.DoesNotExist:
                continue  # 해당 ID가 없는 경우 무시

        self.stdout.write(self.style.SUCCESS(f'{update_count}개의 정책이 업데이트되었습니다.'))
