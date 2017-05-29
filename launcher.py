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
            print("-{0}��-".format(rank))
            print("��ȭ ���� : {0}".format(i['movieNm']))
            print("���� ���� �� : {0} ��".format(i['audiCnt']))
            print("")
    elif menu == 'box':
        tgdt = str(input ("��¥�� �Է��ϼ��� : "))
        list_boxOffice = getXML(tgdt, 0)             # ret = list
        #print(list_boxOffice)
        print("")
        rank = 0;
        for i in list_boxOffice:
            rank += 1
            print("-{0}��-".format(rank))
            print("��ȭ ���� : {0}".format(i['movieNm']))
            print("���� ���� �� : {0} ��".format(i['audiCnt']))
            print("")
    elif menu == 'data':
        mvdt = str(input ("��ȭ������ �Է��ϼ��� : "))
        list_movieData = getXML(mvdt, 1)
        #print(list_movieData)
        print("")
        print("'{0}' �˻� ��� �Դϴ�.".format(mvdt))
        print("")
        count = 0
        for i in list_movieData:
            count += 1
            print("-{0}-".format(count))
            print("��ȭ ���� : {0}".format(i['movieNm']))
            print("������ : {0}".format(i['movieNmEn']))
            print("������ : {0}".format(i['openDt']))
            print("�󼼰˻��� �ڵ� : {0}".format(i['movieCd']))
            print("")
        print("** ��Ȯ�� �˻��� ���Ͻø� ������ ��Ȯ�� �Է��� �ּ���. **")
    elif menu == 'detail':
        mvcd = str(input ("��ȭ�ڵ带 �Է��ϼ��� : "))
        dic_movieDetail = getXML(mvcd, 2)
        #print(dic_movieDetail)
        print("")
        print("�ڵ� '{0}' �˻� ��� �Դϴ�.".format(mvcd))
        print("")
        print("��ȭ ���� : {0}".format(dic_movieDetail['movieNm']))
        print("������ : {0}".format(dic_movieDetail['movieNmEn']))
        print("�� �ð� : {0} ��".format(dic_movieDetail['showTm']))
        print("������ : {0}".format(dic_movieDetail['openDt']))
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
