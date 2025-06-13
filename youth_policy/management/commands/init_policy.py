import os
import pandas as pd
from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy

class Command(BaseCommand):
    help = '엑셀 파일을 읽어 청년정책 정보를 DB에 저장합니다.'

    def handle(self, *args, **kwargs):
        excel_path = r"C:\Users\1-05\OneDrive\Desktop\병합결과.xlsx"

        if not os.path.exists(excel_path):
            self.stderr.write(self.style.ERROR(f"❌ 파일이 존재하지 않습니다: {excel_path}"))
            return

        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ 엑셀 파일 읽기 오류: {e}"))
            return

        created_count = 0
        updated_count = 0

        for _, row in df.iterrows():
            obj, created = YouthPolicy.objects.update_or_create(
                정책명 = str(row.get('정책명', '')).strip(),
                defaults={
                    '정책설명': row.get('정책설명', ''),
                    '대상연령': row.get('대상연령', ''),
                    '정책키워드': row.get('정책키워드', ''),
                    '시행지역': row.get('시행지역', ''),
                    '신청기간': row.get('신청기간', ''),
                    '신청URL': row.get('신청URL', ''),
                    '추가신청자격조건내용': row.get('추가신청자격조건내용', ''),
                    '제출서류내용': row.get('제출서류내용', ''),
                    '참여제외대상': row.get('참여제외대상', ''),
                    '생애주기단계': row.get('생애주기단계', '')
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ 저장 완료: 추가 {created_count}개 / 업데이트 {updated_count}개"
        ))
