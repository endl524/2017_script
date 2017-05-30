# -*- coding: cp949 -*-
loopFlag = 1
from getFromInternet import *
import datetime

#### Menu  implementation
def printMenu():
    print("\nWellcome to BOX OFFICE!!")
    print("=========Menu==========")
    print("�ֽ� �ڽ����ǽ� ����: box")
    print("�Ϻ� �ڽ����ǽ� ����(YYYYMMDD): date")
    print("��ȭ ���� �˻�: search")
    print("��ȭ �ڵ带 �Է��Ͽ� ������ �˻�: detail")
    print("����: exit")
    print("=========Menu==========")
    
def launcherFunction(menu):
    if menu == 'box' :

        s = datetime.date.today() - datetime.timedelta(1)
        yesterday = s.strftime("%Y%m%d")
        list_yesBoxOffice = getXML(yesterday, 0)
        #print(list_yesBoxOffice)
        print("")
        for i in list_yesBoxOffice:
            print("-{0}��-".format(i['rank']))
            print("��ȭ ���� : {0}".format(i['movieNm']))
            print("��ȭ �ڵ� : {0}".format(i['movieCd']))
            print("������ : {0}".format(i['openDt']))
            # --
            print("���� ���� �� : {0} ��".format(format(int(i['audiCnt']),',')))
            print("���� ����� : {0} ��".format(format(int(i['salesAmt']),',')))
            print("���� ���� �� : {0} ��".format(format(int(i['audiAcc']),',')))
            print("���� ����� : {0} ��".format(format(int(i['salesAcc']),',')))
            print("")
    elif menu == 'date':
        tgdt = input ("��¥�� �Է��ϼ��� : ")
        list_boxOffice = getXML(tgdt, 0)             # ret = list
        #print(list_boxOffice)
        print("")
        print("���� ������ ���� ���ּ���")
        print("���� ������ - 1 / ���� ����� - 2 / ���� ������ - 3 / ���� ����� - 4")
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
            print("-{0}��-".format(rank))
            print("��ȭ ���� : {0}".format(i['movieNm']))
            print("��ȭ �ڵ� : {0}".format(i['movieCd']))
            print("������ : {0}".format(i['openDt']))
            #--
            print("���� ���� �� : {0} ��".format(format(int(i['audiCnt']), ',')))
            print("���� ����� : {0} ��".format(format(int(i['salesAmt']), ',')))
            print("���� ���� �� : {0} ��".format(format(int(i['audiAcc']), ',')))
            print("���� ����� : {0} ��".format(format(int(i['salesAcc']), ',')))
            print("")
    elif menu == 'search':
        mvdt = input ("��ȭ������ �Է��ϼ��� : ")
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
            print("�帣 : {0}".format(i['genreAlt']))
            print("�󼼰˻��� �ڵ� : {0}".format(i['movieCd']))
            print("")
        print("** ��Ȯ�� �˻��� ���Ͻø� ������ ��Ȯ�� �Է��� �ּ���. **")
    elif menu == 'detail':
        mvcd = input ("��ȭ�ڵ带 �Է��ϼ��� : ")
        dic_movieDetail = getXML(mvcd, 2)
        #print(dic_movieDetail)
        print("")
        print("�ڵ� '{0}' �˻� ��� �Դϴ�.".format(mvcd))
        print("")
        print("��ȭ ���� : {0}".format(dic_movieDetail['movieNm']))
        print("������ : {0}".format(dic_movieDetail['movieNmEn']))
        print("�� �ð� : {0} ��".format(dic_movieDetail['showTm']))
        print("������ : {0}".format(dic_movieDetail['openDt']))
        print("���۱��� : {0}".format(dic_movieDetail['nationNm']))
        print("�帣 : {0}".format(dic_movieDetail['genreNm']))
        print("������ : {0}".format(dic_movieDetail['peopleNm']))
        print("������� : {0}".format(dic_movieDetail['watchGradeNm']))
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
