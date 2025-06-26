import os
import pandas as pd
from django.core.management.base import BaseCommand
from youth_policy.models import Region

class Command(BaseCommand):
    help = '바탕화면의 엑셀 파일을 읽어 데이터베이스에 저장합니다.'

    def handle(self, *args, **options):
        excel_file = r'C:/Users/1-05/OneDrive/Desktop/시군구 코드_전국.xlsx'

        try:
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                Region.objects.update_or_create(
                    name=row['시군구 명'],
                    code=row['시군구 코드']
                )
            self.stdout.write(self.style.SUCCESS("데이터 저장 완료"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("엑셀 파일을 찾을 수 없습니다."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"에러 발생: {e}"))
