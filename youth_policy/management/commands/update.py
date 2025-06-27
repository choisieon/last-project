import pandas as pd
from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy, Sigungu

class Command(BaseCommand):
    help = '엑셀 파일로부터 정책별 시군구 다대다 연결 수행'

    def add_arguments(self, parser):
        parser.add_argument('policy_excel_path', type=str, help=r'C:/Users/1-05/OneDrive/Desktop/Final_Merge')
        parser.add_argument('sigungu_code_excel_path', type=str, help=r'C:/Users/1-05/OneDrive/Desktop/시군구 코드_전국')

    def handle(self, *args, **options):
        policy_excel = options['policy_excel_path']
        sigungu_excel = options['sigungu_code_excel_path']

        # 1. 시군구 코드 매핑 딕셔너리 생성
        sigungu_df = pd.read_excel(sigungu_excel)
        sigungu_map = {
            str(row['시군구 명']).strip(): str(int(row['시군구 코드']))
            for _, row in sigungu_df.iterrows()
        }

        # 2. 정책 엑셀 읽기
        df = pd.read_excel(policy_excel)

        if '정책명' not in df.columns or '시군구명' not in df.columns:
            self.stderr.write("엑셀에 '정책명' 또는 '시군구명' 열이 없습니다.")
            return

        updated = 0
        skipped = 0

        for _, row in df.iterrows():
            policy_name = row['정책명']
            sigungu_string = str(row['시군구명'])

            try:
                policy = YouthPolicy.objects.get(정책명=policy_name)
            except YouthPolicy.DoesNotExist:
                self.stderr.write(f"[스킵] DB에 정책 없음: {policy_name}")
                skipped += 1
                continue

            if pd.isna(sigungu_string) or sigungu_string.strip() == '':
                self.stderr.write(f"[스킵] 시군구명 없음: {policy_name}")
                continue

            sigungu_names = [name.strip() for name in sigungu_string.split(',')]
            sigungu_objects = []

            for name in sigungu_names:
                code = sigungu_map.get(name)
                if not code:
                    self.stderr.write(f"[경고] 시군구 매핑 실패: '{name}' (정책: {policy_name})")
                    continue
                try:
                    sigungu = Sigungu.objects.get(code=code)
                    sigungu_objects.append(sigungu)
                except Sigungu.DoesNotExist:
                    self.stderr.write(f"[에러] Sigungu(code={code}) 존재하지 않음 - {name}")
                    continue

            if sigungu_objects:
                policy.sigungu.add(*sigungu_objects)
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"시군구 매핑 완료: {updated}건"))
        self.stdout.write(self.style.WARNING(f"정책명 불일치 스킵: {skipped}건"))
