import os
import pandas as pd
from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy

class Command(BaseCommand):
    help = 'YouthPolicy와 Sigungu 간의 중간 테이블 데이터를 바탕화면에 엑셀로 저장합니다.'

    def handle(self, *args, **options):
        # 중간 테이블 모델 객체
        through_model = YouthPolicy.sigungu.through
        queryset = through_model.objects.all()

        if not queryset.exists():
            self.stdout.write(self.style.WARNING("중간 테이블에 데이터가 없습니다."))
            return

        # 필드명 추출
        field_names = [field.name for field in through_model._meta.fields]
        data = list(queryset.values(*field_names))
        df = pd.DataFrame(data)

        # 바탕화면 경로
        desktop_path = r'C:\Users\1-05\OneDrive\Desktop'
        file_path = os.path.join(desktop_path, "youthpolicy_sigungu_through.xlsx")

        # 저장
        df.to_excel(file_path, index=False)
        self.stdout.write(self.style.SUCCESS(f"중간 테이블 데이터가 바탕화면에 저장되었습니다: {file_path}"))
