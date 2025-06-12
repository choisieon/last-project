from django.core.management.base import BaseCommand
from youth_policy.models import YouthPolicy, Sido


class Command(BaseCommand):
    help = '시행지역에서 시도명을 추출해 sido_id 필드를 채움'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='실제 저장하지 않고 결과만 미리보기',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        # Sido 데이터 조회
        sido_list = Sido.objects.all()
        if not sido_list.exists():
            self.stdout.write(self.style.ERROR('❌ Sido 테이블에 데이터가 없습니다.'))
            return
        
        result_log = []
        success_count = 0
        fail_count = 0
        
        # 시행지역이 있는 정책만 조회
        policies = YouthPolicy.objects.exclude(시행지역__isnull=True).exclude(시행지역='')
        
        self.stdout.write(f'📊 처리할 정책 수: {policies.count()}개')
        self.stdout.write(f'📊 사용 가능한 시도 수: {sido_list.count()}개')
        
        # 시도 정보 출력 (디버깅용)
        self.stdout.write('\n🔍 사용 가능한 시도 목록:')
        for sido in sido_list:
            code_info = getattr(sido, 'code', '코드없음')
            name_info = getattr(sido, 'name', '이름없음')
            self.stdout.write(f'  - {name_info} (코드: {code_info})')

        for policy in policies:
            if not policy.시행지역:
                continue

            matched_sido = None
            # 시도명으로 매칭 (긴 이름부터 확인하도록 정렬)
            sorted_sido_list = sorted(sido_list, key=lambda x: len(x.name or ''), reverse=True)
            
            for sido in sorted_sido_list:
                if sido.name and sido.name in policy.시행지역:
                    matched_sido = sido
                    break

            if matched_sido:
                if not dry_run:
                    # sido_id 필드에 code 값을 저장
                    if hasattr(matched_sido, 'code'):
                        policy.sido_id = matched_sido.code
                    else:
                        # code 필드가 없다면 sido 객체의 pk 사용
                        policy.sido_id = matched_sido.pk
                    
                    policy.save()
                
                success_count += 1
                code_value = getattr(matched_sido, 'code', matched_sido.pk)
                result_log.append([
                    policy.정책명[:30] + '...' if len(policy.정책명) > 30 else policy.정책명,
                    policy.시행지역[:20] + '...' if len(policy.시행지역) > 20 else policy.시행지역,
                    matched_sido.name,
                    str(code_value),
                    "✅ 성공"
                ])
            else:
                fail_count += 1
                result_log.append([
                    policy.정책명[:30] + '...' if len(policy.정책명) > 30 else policy.정책명,
                    policy.시행지역[:20] + '...' if len(policy.시행지역) > 20 else policy.시행지역,
                    "",
                    "",
                    "❌ 실패"
                ])

        # 결과 출력
        self.stdout.write('\n' + '='*100)
        self.stdout.write(f'{"정책명":<32} {"시행지역":<22} {"매칭된 시도":<12} {"저장된 코드":<12} {"결과":<8}')
        self.stdout.write('='*100)
        
        for log in result_log:
            self.stdout.write(f'{log[0]:<32} {log[1]:<22} {log[2]:<12} {log[3]:<12} {log[4]:<8}')
        
        # 통계 출력
        self.stdout.write('\n' + '='*100)
        self.stdout.write(self.style.SUCCESS(f'✅ 성공: {success_count}건'))
        self.stdout.write(self.style.ERROR(f'❌ 실패: {fail_count}건'))
        self.stdout.write(f'📊 총 처리: {success_count + fail_count}건')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  DRY RUN 모드 - 실제로 저장되지 않았습니다.'))
        
        # 실패한 시행지역 분석
        if fail_count > 0:
            self.stdout.write('\n🔍 매칭 실패한 시행지역 (상위 10개):')
            failed_regions = [log[1] for log in result_log if log[4] == "❌ 실패"]
            unique_failed = list(set(failed_regions))
            
            for region in unique_failed[:10]:
                count = failed_regions.count(region)
                self.stdout.write(f'  - "{region}" ({count}건)')