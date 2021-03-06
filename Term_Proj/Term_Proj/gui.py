# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
from tkinter import ttk
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from getFromInternet import *
import datetime



host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

# Tk Setting Start.
root = Tk()
root.configure(background='black')
root.geometry("1000x830+200+100")
root.title("박스오피스 & 영화검색")
# Tk Setting End.

# Image Load Start.
logoPath = "logo1.jpg"
logoImage = ImageTk.PhotoImage(Image.open(logoPath))
starPath = "star.png"
starImage = ImageTk.PhotoImage(Image.open(starPath))
mailPath = "email.png"
mailImage = ImageTk.PhotoImage(Image.open(mailPath))
thumb_url = ""
dic_thumbnail = {}
img = 0
photo_url = ""
dic_photo = {}
pht = 0
# Image Load End.

# Frame Setting Start
n=ttk.Notebook(root)
bo_Frame = ttk.Frame(n)
sc_Frame = ttk.Frame(n)
sm_Frame = ttk.Frame(n)
n.add(bo_Frame, text='BoxOffice')
n.add(sc_Frame, text='Search')
n.add(sm_Frame, text='SendMail')
n.place(x=20, y=105, width=960, height = 700)
#Frame Setting End.

s = datetime.date.today() - datetime.timedelta(1)
yesterday = s.strftime("%Y%m%d")



def Title():
    # Title Setting Start.
    logoBack = Label(root, bg = "white")
    logoBack.place(width = 1000, height = 85)

    logoLine1 = Label(root, bg="black")
    logoLine1.place(x=180, y=20, width=170, height=10)
    logoLine2 = Label(root, bg="black")
    logoLine2.place(x=180, y=40, width=170, height=10)
    logoLine3 = Label(root, bg="black")
    logoLine3.place(x=180, y=60, width=170, height=10)
    logoLine4 = Label(root, bg="black")
    logoLine4.place(x=700, y=20, width=170, height=10)
    logoLine5 = Label(root, bg="black")
    logoLine5.place(x=700, y=40, width=170, height=10)
    logoLine6 = Label(root, bg="black")
    logoLine6.place(x=700, y=60, width=170, height=10)

    logo = Label(root, image = logoImage, bg = 'white')
    logo.place(x=0, y=0)

    star = Label(root, image = starImage, bg = 'white')
    star.place(x=890, y=0)
    fontemp = font.Font(root, size = 40, weight = 'bold', slant = 'italic')
    title = Label(root, font = fontemp, text="BOX OFFICE", bg = "white")
    title.place(x=360, y=10)
    # Title Setting End.

# BoxOffice==================================
def BoxOfficeMenu():
    global list_boxOffice, m1_ListBox, m2_ListBox, m3_ListBox, m4_ListBox, m5_ListBox
    global dic_thumbnail, image
    bgLabel = Label(bo_Frame, width=600, height=600, bg='white')
    bgLabel.place(x=0, y=0)
    list_boxOffice = getXML(yesterday, 0, 0)

    init_dateInputLabel()
    init_dateSearchButton()
    init_SortingButton()

    fontemp = font.Font(bo_Frame, size=12, weight='bold')

    # BoxOffice Tab Setting Start.

    m1_ListBox = Listbox(bo_Frame, font=fontemp, width=37, height=11, borderwidth=2, relief='ridge')
    m1_ListBox.place(x=80, y=75)

    m2_ListBox = Listbox(bo_Frame, font=fontemp, width=11, height=11, borderwidth=2, relief='ridge')
    m2_ListBox.place(x=0, y=400)

    m3_ListBox = Listbox(bo_Frame, font=fontemp, width=14, height=11, borderwidth=2, relief='ridge')
    m3_ListBox.place(x=105, y=400)

    m4_ListBox = Listbox(bo_Frame, font=fontemp, width=12, height=11, borderwidth=2, relief='ridge')
    m4_ListBox.place(x=238, y=400)

    m5_ListBox = Listbox(bo_Frame, font=fontemp, width=16, height=11, borderwidth=2, relief='ridge')
    m5_ListBox.place(x=353, y=400)

    dateText = Label(bo_Frame, font=fontemp, bg="grey", fg="black", text="BOX OFFICE 순위")
    dateText.place(x=180, y=15)

    m1_ListBox.bind('<<ListboxSelect>>', listBox_Event)

    # BoxOffice Tab Setting End.


def init_SortingButton():
    fontemp = font.Font(bo_Frame, size=12, weight='bold')

    m1_button = Button(bo_Frame, font=fontemp, bg="grey", fg="black",
                       text="최신 BOX OFFICE 순위 출력\n({0} 기준)".format(yesterday), command=lambda: searchButtonAction(1))
    m1_button.place(x=730, y=5)
    m2_button = Button(bo_Frame, font=fontemp, bg="grey", fg="black", text="당일 관객 수",
                       command=lambda: sortingButtonAction(1))
    m2_button.place(x=5, y=350)
    m3_button = Button(bo_Frame, font=fontemp, bg="grey", fg="black", text="당일 매출액",
                       command=lambda: sortingButtonAction(2))
    m3_button.place(x=127, y=350)
    m4_button = Button(bo_Frame, font=fontemp, bg="grey", fg="black", text="누적 관객 수",
                       command=lambda: sortingButtonAction(3))
    m4_button.place(x=250, y=350)
    m5_button = Button(bo_Frame, font=fontemp, bg="grey", fg="black", text="누적 매출액",
                       command=lambda: sortingButtonAction(4))
    m5_button.place(x=382, y=350)
def sortingButtonAction(b):
    global list_boxOffice
    if b == 1:
        list_boxOffice = sorted(list_boxOffice, key=lambda x: x['audiCnt'], reverse=True)

    elif b == 2:
        list_boxOffice = sorted(list_boxOffice, key=lambda x: x['salesAmt'], reverse=True)

    elif b == 3:
        list_boxOffice = sorted(list_boxOffice, key=lambda x: x['audiAcc'], reverse=True)

    elif b == 4:
        list_boxOffice = sorted(list_boxOffice, key=lambda x: x['salesAcc'], reverse=True)

    m1_ListBox.delete(0, END)
    m2_ListBox.delete(0, END)
    m3_ListBox.delete(0, END)
    m4_ListBox.delete(0, END)
    m5_ListBox.delete(0, END)

    rank = 0;
    for i in list_boxOffice:
        rank += 1
        m1_ListBox.insert(rank - 1, "-{0}위-  {1}\n".format(rank, i['movieNm']))
        m2_ListBox.insert(rank - 1, "{0} 명\n".format(format(int(i['audiCnt']), ',')))
        m3_ListBox.insert(rank - 1, "{0} 원\n".format(format(int(i['salesAmt']), ',')))
        m4_ListBox.insert(rank - 1, "{0} 명\n".format(format(int(i['audiAcc']), ',')))
        m5_ListBox.insert(rank - 1, "{0} 원\n".format(format(int(i['salesAcc']), ',')))


def init_dateInputLabel():
    global InputLabel
    fontemp = font.Font(bo_Frame, size=12, weight='bold')
    dateLabel = Label(bo_Frame, font=fontemp, text="날짜 입력\n(YYYYMMDD)", bg='grey')
    dateLabel.place(x=405, y = 13)
    InputLabel = Entry(bo_Frame, font=fontemp, width=14, borderwidth=3, relief='ridge')
    InputLabel.place(x=520, y=20)
def init_dateSearchButton():
    fontemp = font.Font(bo_Frame, size=12, weight='bold')
    sButton = Button(bo_Frame, font=fontemp, text = "검색", command=lambda: searchButtonAction(0))
    sButton.place(x=670, y=17)
def searchButtonAction(is_yester):
    global list_boxOffice

    fontemp = font.Font(bo_Frame, size=12, weight='bold')

    if is_yester==1:
        date = yesterday
    else:
        date = InputLabel.get()

    list_boxOffice = getXML(date, 0, 0)

    dateText = Label(bo_Frame, font=fontemp, bg="grey", fg="black", text="BOX OFFICE 순위\n({0} 기준)".format(date))
    dateText.place(x=180, y=15)

    m1_ListBox.delete(0, END)
    m2_ListBox.delete(0, END)
    m3_ListBox.delete(0, END)
    m4_ListBox.delete(0, END)
    m5_ListBox.delete(0, END)

    rank = 0;
    for i in list_boxOffice:
        rank += 1
        m1_ListBox.insert(rank - 1, "-{0}위-  {1}\n".format(rank, i['movieNm']))
        m2_ListBox.insert(rank - 1, "{0} 명\n".format(format(int(i['audiCnt']), ',')))
        m3_ListBox.insert(rank - 1, "{0} 원\n".format(format(int(i['salesAmt']), ',')))
        m4_ListBox.insert(rank - 1, "{0} 명\n".format(format(int(i['audiAcc']), ',')))
        m5_ListBox.insert(rank - 1, "{0} 원\n".format(format(int(i['salesAcc']), ',')))


def listBox_Event(evt):
    index = m1_ListBox.curselection()[0]
    get_thumbnail(list_boxOffice[index]['movieNm'], index)
def get_thumbnail(q,index):
    global dic_thumbnail, list_boxOffice, thumb_url
    open1 = list_boxOffice[index]['openDt']
    print(open1)
    dic_thumbnail = getXML(q, 3, open1)
    thumb_url = dic_thumbnail['thumbnail']
    print(thumb_url)
    draw_thumbnail(thumb_url)
def draw_thumbnail(url):
    global img
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    img = ImageTk.PhotoImage(im)
    label = Label(bo_Frame, image=img, width=430, height=625, bg='black')
    label.place(x=520, y=70)
#============================================


# Search=====================================
def SearchMenu():
    global list_movieData, dic_detailData, s1_ListBox, s2_ListBox
    global dic_photo, photo
    list_movieData = []
    dic_detailData = {}
    bgLabel = Label(sc_Frame, width=600, height=600, bg='white')
    bgLabel.place(x=0, y=0)
    init_searchInputLabel()

    fontemp = font.Font(sc_Frame, size=12, weight='bold')
    s1_ListBox = Listbox(sc_Frame, font=fontemp, width=37, height=18, borderwidth=2, relief='ridge')
    s1_ListBox.place(x=5, y=75)
    s2_ListBox = Listbox(sc_Frame, font=fontemp, width=37, height=10, borderwidth=2, relief='ridge')
    s2_ListBox.place(x=5, y=450)


    s1_ListBox.bind('<<ListboxSelect>>', info_event)


def init_searchInputLabel():
    global Input_search
    fontemp = font.Font(sc_Frame, size=12, weight='bold')
    searchLabel = Label(sc_Frame, font=fontemp, text="영화 제목 입력", bg = 'grey')
    searchLabel.place(x=65, y=10)
    Input_search = Entry(sc_Frame, font=fontemp, width=20, borderwidth=3, relief='ridge')
    Input_search.place(x=20, y=40)
    fontemp = font.Font(sc_Frame, size=12, weight='bold')
    sButton = Button(sc_Frame, font=fontemp, text="검색", command=lambda : get_search())
    sButton.place(x=220, y=37)
def get_search():
    global list_movieData, s1_ListBox
    q = Input_search.get()
    fontemp = font.Font(sc_Frame, size=12, weight='bold')
    list_movieData = getXML(q, 1, 0)
    s1_ListBox.delete(0,END)
    rank = 0;
    for i in list_movieData:
        rank += 1
        s1_ListBox.insert(rank - 1, "- {0}\n".format(i['movieNm']))


def info_event(evt):
    global s1_ListBox, list_movieData
    index = s1_ListBox.curselection()[0]
    get_movieinfo(list_movieData[index]['movieCd'])
    get_moviePhoto(list_movieData[index]['movieNm'], index)
def get_movieinfo(q):
    global list_movieData, dic_detailData, s2_ListBox
    fontemp = font.Font(sc_Frame, size=12, weight='bold')
    dic_detailData = getXML(q, 2, 0)
    s2_ListBox.delete(0, END)
    s2_ListBox.insert(END, "제목: {0}\n".format(dic_detailData['movieNm']))
    s2_ListBox.insert(END, "영문 제목: {0}\n".format(dic_detailData['movieNmEn']))
    s2_ListBox.insert(END, "상영시간: {0}분\n".format(dic_detailData['showTm']))
    s2_ListBox.insert(END, "개봉일: {0}\n".format(dic_detailData['openDt']))
    s2_ListBox.insert(END, "제작국가: {0}\n".format(dic_detailData['nationNm']))
    s2_ListBox.insert(END, "장르: {0}\n".format(dic_detailData['genreNm']))
    s2_ListBox.insert(END, "감독명: {0}\n".format(dic_detailData['dirNm']))
    s2_ListBox.insert(END, "관람등급: {0}\n".format(dic_detailData['watchGradeNm']))
def get_moviePhoto(q,index):
    global dic_photo, list_movieData, photo_url
    open1 = list_movieData[index]['openDt']
    dic_photo = getXML(q, 3, open1)
    photo_url = dic_photo['thumbnail']
    if photo_url != NONE:
        movie_Photo(photo_url)
def movie_Photo(url):
    global pht
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    pht = ImageTk.PhotoImage(im)
    label = Label(sc_Frame, image=pht, width=430, height=625, bg='black')
    label.place(x=450, y=10)
#============================================



# Email======================================
def EmailMenu():
    bgLabel = Label(sm_Frame, width=600, height=600, bg='white')
    bgLabel.place(x=0,y=0)
    mailIcon = Label(sm_Frame, image=mailImage, bg='white')
    mailIcon.place(x=30, y=220)
    init_loginLabel()

def init_loginLabel():
    global IDInputLabel, PWInputLabel
    fontemp = font.Font(sm_Frame, size=40, weight='bold')
    fontemp2 = font.Font(sm_Frame, size=30, weight='bold')
    fontemp3 = font.Font(sm_Frame, size=20, weight='bold')

    titleLabel = Label(sm_Frame, font=fontemp, text="SEND E-MAIL", bg='white')
    titleLabel.place(x=470, y=150)

    IDLabel = Label(sm_Frame, font=fontemp2, text="ID", bg='white')
    IDLabel.place(x=350, y=250)
    IDInputLabel = Entry(sm_Frame, font=fontemp2, width=18, borderwidth=3, relief='ridge', fg='blue')
    IDInputLabel.place(x=450, y=250)

    PWLabel = Label(sm_Frame, font=fontemp2, text="PW", bg='white')
    PWLabel.place(x=335, y=350)
    PWInputLabel = Entry(sm_Frame, font=fontemp2, width=18, borderwidth=3, relief='ridge', fg='blue', show='*')
    PWInputLabel.place(x=450, y=350)

    sendButton = Button(sm_Frame, font=fontemp3, text="Send", command=lambda: sendMail())
    sendButton.place(x=600, y=550)
#============================================
def sendMail():
    global host, port, id, pw
    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    id = IDInputLabel.get()
    pw = PWInputLabel.get()

    msgtext = str('y')
    if msgtext == 'y':
        html = makeText()

    title = dic_detailData['movieNm']

    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = id
    msg['To'] = id
    infoPart = MIMEText(html, 'html', _charset = 'utf-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(infoPart)


    print ("connect smtp server ... ")
    smt = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    smt.ehlo()
    smt.starttls()
    smt.ehlo()
    smt.login(id, pw)    # 로긴을 합니다.
    smt.sendmail(id , [id], msg.as_string())
    smt.close()

    print ("Mail sending complete!!!")

def makeText():
    from xml.dom.minidom import getDOMImplementation
    # get Dom Implementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')
    b= newdoc.createElement('b')
    text1 = newdoc.createTextNode("영화 제목 : {0}".format(dic_detailData['movieNm']))
    b.appendChild(text1)
    body.appendChild(b)

    br = newdoc.createElement('br')
    body.appendChild(br)

    c = newdoc.createElement('c')
    text2 = newdoc.createTextNode("영문명 : {0}".format(dic_detailData['movieNmEn']))
    c.appendChild(text2)
    body.appendChild(c)

    br = newdoc.createElement('br')
    body.appendChild(br)

    d = newdoc.createElement('d')
    text3 = newdoc.createTextNode("상영 시간 : {0}".format(dic_detailData['showTm']))
    d.appendChild(text3)
    body.appendChild(d)

    br = newdoc.createElement('br')
    body.appendChild(br)

    e = newdoc.createElement('e')
    text4 = newdoc.createTextNode("개봉일 : {0}".format(dic_detailData['openDt']))
    e.appendChild(text4)
    body.appendChild(e)

    br = newdoc.createElement('br')
    body.appendChild(br)

    f = newdoc.createElement('f')
    text5 = newdoc.createTextNode("제작국가 : {0}".format(dic_detailData['nationNm']))
    f.appendChild(text5)
    body.appendChild(f)

    br = newdoc.createElement('br')
    body.appendChild(br)

    g = newdoc.createElement('g')
    text6 = newdoc.createTextNode("장르 : {0}".format(dic_detailData['genreNm']))
    g.appendChild(text6)
    body.appendChild(g)

    br = newdoc.createElement('br')
    body.appendChild(br)

    h = newdoc.createElement('h')
    text7 = newdoc.createTextNode("감독명 : {0}".format(dic_detailData['dirNm']))
    h.appendChild(text7)
    body.appendChild(h)

    br = newdoc.createElement('br')
    body.appendChild(br)

    i = newdoc.createElement('i')
    text8 = newdoc.createTextNode("관람등급 : {0}".format(dic_detailData['watchGradeNm']))
    i.appendChild(text8)
    body.appendChild(i)

    br = newdoc.createElement('br')
    body.appendChild(br)

    j = newdoc.createElement('j')
    text9 = newdoc.createTextNode("포스터 URL : {0}".format(dic_photo['thumbnail']))
    j.appendChild(text9)
    body.appendChild(j)

    br = newdoc.createElement('br')
    body.appendChild(br)

    top_element.appendChild(body)

    return newdoc.toxml()
#========================================================================

#  main loop
Title()
BoxOfficeMenu()
SearchMenu()
EmailMenu()
root.mainloop()