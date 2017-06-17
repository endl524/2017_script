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


# Tk Setting Start.
root = Tk()
root.configure(background='black')
root.geometry("1000x830+200+100")
# Tk Setting End.

# Image Load Start.
logoPath = "logo1.jpg"
logoImage = ImageTk.PhotoImage(Image.open(logoPath))
starPath = "star.png"
starImage = ImageTk.PhotoImage(Image.open(starPath))
thumb_url = ""
dic_thumbnail = {}
img = 0
# Image Load End.

# Frame Setting Start
n=ttk.Notebook(root)
bo_Frame = ttk.Frame(n)
sc_Frame = ttk.Frame(n)
n.add(bo_Frame, text='BoxOffice')
n.add(sc_Frame, text='Search')
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

def BoxOfficeMenu():
    global list_boxOffice, m1_ListBox, m2_ListBox, m3_ListBox, m4_ListBox, m5_ListBox
    global dic_thumbnail, image
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

    m1_ListBox.delete(0, 9)
    m2_ListBox.delete(0, 9)
    m3_ListBox.delete(0, 9)
    m4_ListBox.delete(0, 9)
    m5_ListBox.delete(0, 9)
    rank = 0;
    for i in list_boxOffice:
        rank += 1
        m1_ListBox.insert(rank - 1, "-{0}위-  {1}\n".format(rank, i['movieNm']))
        m2_ListBox.insert(rank - 1, "{0} 명\n".format(format(int(i['audiCnt']), ',')))
        m3_ListBox.insert(rank - 1, "{0} 원\n".format(format(int(i['salesAmt']), ',')))
        m4_ListBox.insert(rank - 1, "{0} 명\n".format(format(int(i['audiAcc']), ',')))
        m5_ListBox.insert(rank - 1, "{0} 원\n".format(format(int(i['salesAcc']), ',')))

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

    m1_ListBox.delete(0, 9)
    m2_ListBox.delete(0, 9)
    m3_ListBox.delete(0, 9)
    m4_ListBox.delete(0, 9)
    m5_ListBox.delete(0, 9)

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
    dateLabel = Label(bo_Frame, font=fontemp, text="날짜 입력")
    dateLabel.place(x=440, y = 20)
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

    m1_ListBox.delete(0, 9)
    m2_ListBox.delete(0, 9)
    m3_ListBox.delete(0, 9)
    m4_ListBox.delete(0, 9)
    m5_ListBox.delete(0, 9)

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
    dic_thumbnail = getXML(q, 3, open1)
    open2 = dic_thumbnail['openDt']
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


# main loop
Title()
BoxOfficeMenu()

root.mainloop()