# -*- coding: utf-8 -*
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import urllib.request

##global
conn = None
regKey = "0848050b31dd08165f0638be3fce6e5a"
server = "www.kobis.or.kr"

daumKey =  "8d62f1664ef7401400175ae83fd286c3"
daumServer = "apis.daum.net"


# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def userURIBuilder(server,case,**user):
    #str = "http://" + server + "/search" + "?"
    if case == 0:
        str = "https://" + server + "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?"
    elif case == 1:
        str = "https://" + server + "/kobisopenapi/webservice/rest/movie/searchMovieList.xml?"
    elif case == 2:
        str = "https://" + server + "/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml?"
    elif case == 3:
        str = "https://" + server + "/contents/movie?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer(getType):
    global conn, server
    if getType == 3:
        conn = HTTPConnection(daumServer)
    else:
        conn = HTTPConnection(server)
        
def getXML(query, getType, date):
    global server, regKey, conn, daumServer, daumKey
    if conn == None :
        connectOpenAPIServer(getType)
    encText = urllib.parse.quote(query)
    if getType == 0 :
        url = userURIBuilder(server, getType, key=regKey, targetDt=encText)
    elif getType == 1:
        url = userURIBuilder(server, getType, key=regKey, movieNm=encText, itemPerPage='20')
    elif getType == 2:
        url = userURIBuilder(server, getType, key=regKey, movieCd=encText)
    elif getType == 3:
        url = userURIBuilder(daumServer, getType, apikey=daumKey, q=encText, output="xml")
    response = urllib.request.urlopen(urllib.request.Request(url))
    if int(response.getcode()) == 200 :
        print("Data downloading complete!")
        response_body = response.read()
        if getType == 0 :
            return extractBoxOffice(response_body.decode('utf-8'))
        elif getType == 1:
            return extractMovieData(response_body.decode('utf-8'))
        elif getType == 2:
            return extractDetailData(response_body.decode('utf-8'))
        elif getType == 3:
            return extractThumbnail(response_body.decode('utf-8'), date)
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None
#--------------------------------------------------------------
def extractBoxOffice(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("dailyBoxOfficeList")  # return list type
    itemElements2 = tree.getiterator("dailyBoxOffice")
    BOList = []
    for item in itemElements:
        for item2 in itemElements2:
            rank = item2.find("rank") #순위
            rankInten = item2.find("rankInten") #순위 변동
            movieNm = item2.find("movieNm") #영화 제목
            movieCd = item2.find("movieCd") #영화 코드
            openDt = item2.find("openDt") #개봉일
            str = openDt.text
            #--정렬기준--
            audiCnt = item2.find("audiCnt") #당관
            salesAmt = item2.find("salesAmt") #당매
            audiAcc = item2.find("audiAcc") #누관
            salesAcc = item2.find("salesAcc") #누매
            BOList.append({"rank":rank.text, "movieNm":movieNm.text, "movieCd":movieCd.text, "openDt":str.replace("-", ''), "rankInten":int(rankInten.text), "audiCnt":int(audiCnt.text), "salesAmt":int(salesAmt.text), "audiAcc":int(audiAcc.text), "salesAcc":int(salesAcc.text)})
    return BOList

def extractMovieData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("movieList")  # return list type
    itemElements2 = tree.getiterator("movie")
    MVList = []
    for item in itemElements:
        for item2 in itemElements2:
            movieNm = item2.find("movieNm")
            movieNmEn = item2.find("movieNmEn")
            openDt = item2.find("openDt")
            movieCd = item2.find("movieCd")
            genreAlt = item2.find("genreAlt")
            MVList.append({"movieNm":movieNm.text,"movieNmEn":movieNmEn.text, "openDt":openDt.text, "movieCd": movieCd.text, "genreAlt":genreAlt.text})
    return MVList

def extractDetailData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("movieInfo")  # return list type
    #actorList = []
    for item in itemElements:
        movieNm = item.find("movieNm")
        movieNmEn = item.find("movieNmEn")
        showTm = item.find("showTm")
        openDt = item.find("openDt")
        str = openDt.text
        nationNm = item.find("nations").find("nation").find("nationNm")
        genreNm = item.find("genres").find("genre").find("genreNm")
        dirNm = item.find("directors").find("director").find("peopleNm")
        watchGradeNm = item.find("audits").find("audit").find("watchGradeNm")
        #for item2 in tree.getiterator("actor"):
        #    actorNm = item2.find("peopleNm")
        #    charNm = item2.find("cast")
        #    actorList.append({"actorNm":actorNm.text, "charNm":charNm.text})
        if str != None:
            return {"movieNm":movieNm.text,"movieNmEn":movieNmEn.text, "showTm":showTm.text, "openDt":str.replace("-", ''),
            "nationNm":nationNm.text, "genreNm":genreNm.text, "dirNm":dirNm.text, "watchGradeNm":watchGradeNm.text}#, "actorList":actorList}

def extractThumbnail(strXml, date):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    for item in tree.getiterator("item"):
        thumbnail = item.find("thumbnail").find("content")
        movieNm = item.find("title").find("content")
        openDt = item.find("open_info").find("content")
        str = openDt.text
        l = str.split('.')
        str2 = l[0]+l[1]+l[2]
        if str2 == date:
            return {"movieNm": movieNm.text, "openDt": str2, "thumbnail": thumbnail.text}

#--------------------------------------------------------------

def sendMain():
    global host, port
    html = ""
    title = str(input('Title :'))
    senderAddr = str(input('sender email address :'))
    recipientAddr = str(input('recipient email address :'))
    msgtext = str(input('write message :'))
    passwd = str(input(' input your password of gmail account :'))
    msgtext = str(input('Do you want to include book data (y/n):'))
    if msgtext == 'y':
        keyword = str(input('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))

    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset='UTF-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)

    print("connect smtp server ... ")
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)  # 로긴을 합니다.
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()


def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server 종료합니다.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
