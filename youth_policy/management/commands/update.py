import requests
import time
import pandas as pd

# 공공데이터포털 API 키
SERVICE_KEY = "여기에_발급받은_API_키_입력"

# 시도 목록 요청 URL
SIDO_URL = f"https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList?serviceKey={SERVICE_KEY}&type=json&locatadd_nm="

# 시군구 목록 요청 URL (시도코드 기준)
SIGUNGU_URL = f"https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList?serviceKey={SERVICE_KEY}&type=json&locatadd_nm={{}}"

def fetch_sido_list():
    print("[시도 목록 수집 시작]")
    response = requests.get(SIDO_URL)
    data = response.json()
    sido_list = []

    for item in data['StanReginCd'][1]['row']:
        if item['up_locat_code'] == '0':  # 상위 코드가 0이면 시도
            sido_list.append({
                'sido_name': item['locatadd_nm'],
                'sido_code': item['locat_code']
            })

    print(f"[완료] 시도 수: {len(sido_list)}")
    return sido_list

def fetch_sigungu_list(sido):
    print(f"[시군구 수집: {sido['sido_name']}]")
    url = SIGUNGU_URL.format(sido['sido_name'])
    response = requests.get(url)
    data = response.json()
    sigungu_list = []

    for item in data['StanReginCd'][1]['row']:
        if item['up_locat_code'] == sido['sido_code']:
            sigungu_list.append({
                'sigungu_name': item['locatadd_nm'],
                'sigungu_code': item['locat_code'],
                'sido_name': sido['sido_name'],
                'sido_code': sido['sido_code']
            })

    print(f" → 수집된 시군구 수: {len(sigungu_list)}")
    return sigungu_list

def main():
    sido_list = fetch_sido_list()
    total_sigungu = []

    for sido in sido_list:
        sigungu_list = fetch_sigungu_list(sido)
        total_sigungu.extend(sigungu_list)
        time.sleep(0.5)  # 요청 간격 제한

    df = pd.DataFrame(total_sigungu)
    df.to_excel("시군구_코드_목록.xlsx", index=False)
    print("\n[완료] 시군구 목록 엑셀로 저장 완료")

if __name__ == "__main__":
    main()
