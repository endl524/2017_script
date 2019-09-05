# 한국산업기술대학교 게임공학부
#### 2017년도 스크립트 언어 과목 - 텀프로젝트      


# 영화 정보 검색 프로그램
* **사용 언어** - 파이썬 3  


# 주요 기능
* **tkinter GUI**를 사용하여 GUI 구현 (텍스트, 이미지, 버튼 배치 등..)
* **KOFIC**(영화관 입장권 통합 전산망) **open API**를 활용하여 일자 별 **박스 오피스 순위** 및 **영화 정보 검색** 기능 구현    
-> 입력한 **일자(Date)에 따른 순위 검색** 기능  
-> **최신 순위 검색** 기능  
-> 검색한 순위를 **다양한 값으로 정렬**하는 기능 (당일 관객수, 당일 매출수, 누적 관객수, 누적 매출수)  
-> 영화 **제목으로 정보 검색** 기능 (**유사한 제목까지 포함**하여 검색 가능)  
-> 영화 **상세 정보 출력** 기능  
-> email로 검색한 **정보를 전송**하는 기능  
* **Pillow** 라이브러리와 ~**DAUM open API**의 검색 기능을 활용~하여 ~**영화 포스터(썸네일)**을 가져와 표시해주는 기능 구현~  
-> (**DAUM open API**는 **2019.01.01 부로 이용이 불가**하여 영화 포스터(썸네일) 표시 **기능이 제한** 됨.)