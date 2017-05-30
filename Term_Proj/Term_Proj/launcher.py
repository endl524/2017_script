# -*- coding: cp949 -*-
loopFlag = 1
from getFromInternet import *
import datetime

#### Menu  implementation
def printMenu():
    print("\nWellcome to BOX OFFICE!!")
    print("=========Menu==========")
    print("최신 박스오피스 순위: box")
    print("일별 박스오피스 정렬(YYYYMMDD): date")
    print("영화 정보 검색: search")
    print("영화 코드를 입력하여 상세정보 검색: detail")
    print("종료: exit")
    print("=========Menu==========")
    
def launcherFunction(menu):
    if menu == 'box' :

        s = datetime.date.today() - datetime.timedelta(1)
        yesterday = s.strftime("%Y%m%d")
        list_yesBoxOffice = getXML(yesterday, 0)
        #print(list_yesBoxOffice)
        print("")
        for i in list_yesBoxOffice:
            print("-{0}위-".format(i['rank']))
            print("영화 제목 : {0}".format(i['movieNm']))
            print("영화 코드 : {0}".format(i['movieCd']))
            print("개봉일 : {0}".format(i['openDt']))
            # --
            print("당일 관객 수 : {0} 명".format(format(int(i['audiCnt']),',')))
            print("당일 매출액 : {0} 원".format(format(int(i['salesAmt']),',')))
            print("누적 관객 수 : {0} 명".format(format(int(i['audiAcc']),',')))
            print("누적 매출액 : {0} 원".format(format(int(i['salesAcc']),',')))
            print("")
    elif menu == 'date':
        tgdt = input ("날짜를 입력하세요 : ")
        list_boxOffice = getXML(tgdt, 0)             # ret = list
        #print(list_boxOffice)
        print("")
        print("정렬 기준을 선택 해주세요")
        print("당일 관객수 - 1 / 당일 매출액 - 2 / 누적 관객수 - 3 / 누적 매출액 - 4")
        howSort = input("How? >> ")
        print("")
        if howSort == '1':
            list_boxOffice
            #sorted(list_boxOffice, key=lambda x, y: x[y['audiCnt']])
        elif howSort == '2':
            sorted(list_boxOffice, key=lambda x: x['salesAmt'])
        elif howSort == '3':
            sorted(list_boxOffice, key=lambda x: x['audiAcc'])
        elif howSort == '4':
            sorted(list_boxOffice, key=lambda x: x['salesAcc'])
        else:
            return 0
        rank = 0;
        for i in list_boxOffice:
            rank += 1
            print("-{0}위-".format(rank))
            print("영화 제목 : {0}".format(i['movieNm']))
            print("영화 코드 : {0}".format(i['movieCd']))
            print("개봉일 : {0}".format(i['openDt']))
            #--
            print("당일 관객 수 : {0} 명".format(format(int(i['audiCnt']), ',')))
            print("당일 매출액 : {0} 원".format(format(int(i['salesAmt']), ',')))
            print("누적 관객 수 : {0} 명".format(format(int(i['audiAcc']), ',')))
            print("누적 매출액 : {0} 원".format(format(int(i['salesAcc']), ',')))
            print("")
    elif menu == 'search':
        mvdt = input ("영화제목을 입력하세요 : ")
        list_movieData = getXML(mvdt, 1)
        #print(list_movieData)
        print("")
        print("'{0}' 검색 결과 입니다.".format(mvdt))
        print("")
        count = 0
        for i in list_movieData:
            count += 1
            print("-{0}-".format(count))
            print("영화 제목 : {0}".format(i['movieNm']))
            print("영문명 : {0}".format(i['movieNmEn']))
            print("개봉일 : {0}".format(i['openDt']))
            print("장르 : {0}".format(i['genreAlt']))
            print("상세검색용 코드 : {0}".format(i['movieCd']))
            print("")
        print("** 정확한 검색을 원하시면 제목을 정확히 입력해 주세요. **")
    elif menu == 'detail':
        mvcd = input ("영화코드를 입력하세요 : ")
        dic_movieDetail = getXML(mvcd, 2)
        #print(dic_movieDetail)
        print("")
        print("코드 '{0}' 검색 결과 입니다.".format(mvcd))
        print("")
        print("영화 제목 : {0}".format(dic_movieDetail['movieNm']))
        print("영문명 : {0}".format(dic_movieDetail['movieNmEn']))
        print("상영 시간 : {0} 분".format(dic_movieDetail['showTm']))
        print("개봉일 : {0}".format(dic_movieDetail['openDt']))
        print("제작국가 : {0}".format(dic_movieDetail['nationNm']))
        print("장르 : {0}".format(dic_movieDetail['genreNm']))
        print("감독명 : {0}".format(dic_movieDetail['peopleNm']))
        print("관람등급 : {0}".format(dic_movieDetail['watchGradeNm']))
        print("")
    elif menu == 'exit':
        global loopFlag
        loopFlag = 0
    # -----------------------------------------------------

    else:
        print ("error : unknow menu key")


##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu : '))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")
