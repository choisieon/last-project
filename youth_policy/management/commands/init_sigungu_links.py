from django.core.management.base import BaseCommand
import pandas as pd
import os

from youth_policy.models import YouthPolicy, Sigungu

class Command(BaseCommand):
    help = '엑셀 파일에서 정책-시군구 관계(ManyToMany)를 중간 테이블에 저장합니다.'

    def handle(self, *args, **options):
        # 바탕화면 경로에 있는 엑셀 파일 불러오기
        desktop_path = r'C:\Users\1-05\OneDrive\Desktop'
        file_path = r"C:\Users\1-05\OneDrive\Desktop\시군구 중간 테이블.xlsx"

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"파일을 찾을 수 없습니다: {file_path}"))
            return

        df = pd.read_excel(file_path)

        inserted = 0
        for _, row in df.iterrows():
            try:
                policy = YouthPolicy.objects.get(id=row['youthpolicy'])
                sigungu = Sigungu.objects.get(id=row['sigungu'])
                policy.sigungu.add(sigungu)
                inserted += 1
            except YouthPolicy.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"정책 ID {row['youthpolicy']} 없음"))
            except Sigungu.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"시군구 ID {row['sigungu']} 없음"))

        self.stdout.write(self.style.SUCCESS(f"총 {inserted}건의 정책-시군구 연결이 추가되었습니다."))
