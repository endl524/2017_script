# -*- coding: utf-8 -*
from doTheWork import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import urllib.request

##global
conn = None
regKey = "0848050b31dd08165f0638be3fce6e5a"
server = "www.kobis.or.kr"

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
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)
        
def getXML(query, getType):
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    encText = urllib.parse.quote(query)
    if getType == 0 :
        url = userURIBuilder(server, getType, key=regKey, targetDt=encText)
    elif getType == 1:
        url = userURIBuilder(server, getType, key=regKey, movieNm=encText, itemPerPage='20')
    elif getType == 2:
        url = userURIBuilder(server, getType, key=regKey, movieCd=encText)
    response = urllib.request.urlopen(urllib.request.Request(url))
    if int(response.getcode()) == 200 :
        print("Data downloading complete!")
        response_body = response.read()
        if getType == 0 :
            return extractBoxOffice(response_body.decode('utf-8'))
        elif getType == 1:
            return extractMovieData(response_body.decode('utf-8'))
        elif getType == 2 :
            return extractDetailData(response_body.decode('utf-8'))
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None
#--------------------------------------------------------------
def extractBoxOffice(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    # Book 엘리먼트를 가져옵니다.
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
            #--정렬기준--
            audiCnt = item2.find("audiCnt") #당관
            salesAmt = item2.find("salesAmt") #당매
            audiAcc = item2.find("audiAcc") #누관
            salesAcc = item2.find("salesAcc") #누매
            BOList.append({"rank":rank.text, "movieNm":movieNm.text, "movieCd":movieCd.text, "openDt":openDt.text, "rankInten":int(rankInten.text), "audiCnt":int(audiCnt.text), "salesAmt":int(salesAmt.text), "audiAcc":int(audiAcc.text), "salesAcc":int(salesAcc.text)})
    return BOList

def extractMovieData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    # Book 엘리먼트를 가져옵니다.
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
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("movieInfo")  # return list type
    for item in itemElements:
        movieNm = item.find("movieNm")
        movieNmEn = item.find("movieNmEn")
        showTm = item.find("showTm")
        openDt = item.find("openDt")
        for item2 in tree.getiterator("nations"):
            for item3 in tree.getiterator("nation"):
                nationNm = item3.find("nationNm")
        for item2 in tree.getiterator("genres"):
            for item3 in tree.getiterator("genre"):
                genreNm = item3.find("genreNm")
        for item2 in tree.getiterator("directors"):
            for item3 in tree.getiterator("director"):
                peopleNm = item3.find("peopleNm")
        for item2 in tree.getiterator("audits"):
            for item3 in tree.getiterator("audit"):
                watchGradeNm = item3.find("watchGradeNm")
    return{"movieNm":movieNm.text,"movieNmEn":movieNmEn.text, "showTm":showTm.text, "openDt":openDt.text, "nationNm":nationNm.text, "genreNm":genreNm.text, "peopleNm":peopleNm.text, "watchGradeNm":watchGradeNm.text}
#--------------------------------------------------------------
def sendMain():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr = str(input ('sender email address :'))
    recipientAddr = str(input ('recipient email address :'))
    msgtext = str(input ('write message :'))
    passwd = str(input (' input your password of gmail account :'))
    msgtext = str(input ('Do you want to include book data (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로긴을 합니다. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400,' bad requst : please check the your url') # 잘 못된 요청라는 에러를 응답한다.
        
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
