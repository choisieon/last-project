# 소셜 로그인 사용 위한 단계별 설정

## 카카오톡
1. 프로젝트 clone 및 마이그레이션

2. requirements 파일 다운로드

3. admin 계정 생성
   - SITES에 'loacalhost:8000' 추가
   - SOCIAL APPLICATION에 들어가서 'ADD SOCIAL APPLICATION' 클릭
       - Provider -> Kakao
       - Name -> 아무거나 ex)소셜 로그인 기능 구현(카카오)
       - Client id -> 카카오 디벨로퍼스에서 발급받은 Rest_API 키 입력
       - Secret key -> 카카오는 생략 가능
       - SITES -> 앞서 입력한 site 선택
       - SAVE 버튼 클릭

## 네이버
1. 프로젝트 clone 및 마이그레이션

2. requirements 파일 다운로드

3. admin 계정 생성
   - SITES에 'loacalhost:8000' 추가

--------------------------------------------------------------------------- 앞과 동일
   - SOCIAL APPLICATION에 들어가서 'ADD SOCIAL APPLICATION' 클릭
       - Provider -> Naver
       - Name -> 아무거나 ex)소셜 로그인 기능 구현(네이버))
       - Client id -> 네이버 개발자 센터에서 발급받은 Client ID 입력
       - Secret key -> 네이버 개발자 센터에서 발급받은 Client Secret 입력
       - SITES -> 앞서 입력한 site 선택
       - SAVE 버튼 클릭
