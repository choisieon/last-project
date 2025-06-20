
# 소셜 로그인 사용 위한 단계별 설정

## 카카오톡
1. 프로젝트 clone 및 마이그레이션

2. requirements 파일 다운로드(+ pip install pillow)

3. admin 계정 생성
   - SITES에 'loacalhost:8000' 추가
   - SOCIAL APPLICATION에 들어가서 'ADD SOCIAL APPLICATION' 클릭
       - Provider -> Kakao
       - Name -> 아무거나 ex)소셜 로그인 기능 구현(카카오)
       - Client id -> 각 플랫폼별 개발자 사이트에서 발급받은 키 입력 ex) 카카오 디벨로퍼스, 네이버 개발자 센터
       - Secret key -> 카카오는 필수 아님. 구글과 네이버는 반드시 입력
       - SITES -> 앞서 입력한 site 선택
       - SAVE 버튼 클릭
    
4. 카카오, 네이버, 구글에 대해 3번 과정 반복

