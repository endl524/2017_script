# -*- coding: cp949 -*-
loopFlag = 1
from getFromInternet import *
import datetime

#### Menu  implementation
def printMenu():
    print("\nWelcome! Book Manager Program (xml version)")
    print("========Menu==========")
    print("Yesterday's BoxOffice: y")
    print("Get dailyBoxOffice: box")
    print("Get MovieData: data")
    print("Get DetailData: detail")
    print("========Menu==========")
    
def launcherFunction(menu):
    if menu == 'y' :
        s = datetime.date.today() - datetime.timedelta(1)
        yesterday = s.strftime("%Y%m%d")
        list_yesBoxOffice = getXML(yesterday, 0)
        #print(list_yesBoxOffice)
        print("")
        rank = 0;
        for i in list_yesBoxOffice:
            rank += 1
            print("-{0}위-".format(rank))
            print("영화 제목 : {0}".format(i['movieNm']))
            print("어제 관객 수 : {0} 명".format(i['audiCnt']))
            print("")
    elif menu == 'box':
        tgdt = str(input ("날짜를 입력하세요 : "))
        list_boxOffice = getXML(tgdt, 0)             # ret = list
        #print(list_boxOffice)
        print("")
        rank = 0;
        for i in list_boxOffice:
            rank += 1
            print("-{0}위-".format(rank))
            print("영화 제목 : {0}".format(i['movieNm']))
            print("당일 관객 수 : {0} 명".format(i['audiCnt']))
            print("")
    elif menu == 'data':
        mvdt = str(input ("영화제목을 입력하세요 : "))
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
            print("상세검색용 코드 : {0}".format(i['movieCd']))
            print("")
        print("** 정확한 검색을 원하시면 제목을 정확히 입력해 주세요. **")
    elif menu == 'detail':
        mvcd = str(input ("영화코드를 입력하세요 : "))
        dic_movieDetail = getXML(mvcd, 2)
        #print(dic_movieDetail)
        print("")
        print("코드 '{0}' 검색 결과 입니다.".format(mvcd))
        print("")
        print("영화 제목 : {0}".format(dic_movieDetail['movieNm']))
        print("영문명 : {0}".format(dic_movieDetail['movieNmEn']))
        print("상영 시간 : {0} 분".format(dic_movieDetail['showTm']))
        print("개봉일 : {0}".format(dic_movieDetail['openDt']))
        print("")
    # -----------------------------------------------------
    elif menu == 'm':
        keyword = str(input ('input keyword code to the html  :'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
        print("-----------------------")
        print(html)
        print("-----------------------")
    elif menu == 'i':
        sendMain()
    elif menu == "t":
        startWebService()
    else:
        print ("error : unknow menu key")

def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()
    
##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu : '))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")
