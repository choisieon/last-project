import os
import pandas as pd
from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy, Sido
class Command(BaseCommand):
    help = '엑셀 파일을 읽어 청년정책 정보를 DB에 저장합니다.'
    def handle(self, *args, **kwargs):
        excel_path = r"/Users/choesieon/Desktop/병합결과_최종.xlsx"
        if not os.path.exists(excel_path):
            self.stderr.write(self.style.ERROR(f":x: 파일이 존재하지 않습니다: {excel_path}"))
            return
        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f":x: 엑셀 파일 읽기 오류: {e}"))
            return
        created_count = 0
        updated_count = 0
        for _, row in df.iterrows():
            policy_name = str(row.get('정책명', '')).strip()
            if not policy_name:
                continue
            try:
                view_count = int(row.get('view_count', 0))
            except:
                view_count = 0
            try:
                sido_id = int(row.get('sido')) if not pd.isna(row.get('sido')) else None
            except:
                sido_id = None
            application_start = row.get('application_start') if not pd.isna(row.get('application_start')) else None
            application_end = row.get('application_end') if not pd.isna(row.get('application_end')) else None
            obj, created = YouthPolicy.objects.update_or_create(
                정책명=policy_name,
                defaults={
                    '정책설명': row.get('정책설명', '') or '',
                    '대상연령': row.get('대상연령', '') or '',
                    '정책키워드': row.get('정책키워드', '') or '',
                    'application_period': row.get('application_period', '') or '',
                    '신청URL': row.get('신청URL', '') or '',
                    '추가신청자격조건내용': row.get('추가신청자격조건내용', '') or '',
                    '제출서류내용': row.get('제출서류내용', '') or '',
                    '참여제외대상': row.get('참여제외대상', '') or '',
                    '생애주기단계': row.get('생애주기단계', '') or '',
                    '정책설명요약': row.get('정책설명요약', '') or '',
                    'view_count': view_count,
                    'application_start': application_start,
                    'application_end': application_end,
                    'sido_id': sido_id
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        self.stdout.write(self.style.SUCCESS(
            f":흰색_확인_표시: 저장 완료: 추가 {created_count}개 / 업데이트 {updated_count}개"
        ))