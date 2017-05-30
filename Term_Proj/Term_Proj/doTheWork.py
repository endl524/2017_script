# -*- coding: cp949 -*-
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

##### global
xmlFD = -1
BooksDoc = None

def AddBook(bookdata):
     global BooksDoc
     if not checkDocument() :
        return None
     
     # book 엘리먼트 생성
     newBook = BooksDoc.createElement('BoxOffice')
     newBook.setAttribute('audiCnt',bookdata['audiCnt'])
     # Title 엘리먼트 생성
     titleEle = BooksDoc.createElement('movieNm')
     # 텍스트 노드 생성
     titleNode = BooksDoc.createTextNode(bookdata['movieNm'])
     # 텍스트 노드를 Title 엘리먼트와 연결
     try:
         titleEle.appendChild(titleNode)
     except Exception:
         print ("append child fail- please,check the parent element & node!!!")
         return None
     else:
         titleEle.appendChild(titleNode)

     # Title 엘리먼트를 Book 엘리먼트와 연결.
     try:
         newBook.appendChild(titleEle)
         booklist = BooksDoc.firstChild
     except Exception:
         print ("append child fail- please,check the parent element & node!!!")
         return None
     else:
         if booklist != None:
             booklist.appendChild(newBook)

def SearchBookTitle(keyword):
    global BooksDoc
    retlist = []
    if not checkDocument():
        return None
        
    try:
        tree = ElementTree.fromstring(str(BooksDoc.toxml()))
    except Exception:
        print ("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None
    
    #get Book Element
    bookElements = tree.getiterator("book")  # return list type
    for item in bookElements:
        strTitle = item.find("title")
        if (strTitle.text.find(keyword) >=0 ):
            retlist.append((item.attrib["ISBN"], strTitle.text))
    
    return retlist

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for bookitem in BookList:
        #create bold element
        b = newdoc.createElement('b')
        #create text node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)
    
        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

        #create title Element
        p = newdoc.createElement('p')
        #create text node
        titleText= newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  #line end
         
    #append Body
    top_element.appendChild(body)
    
    return newdoc.toxml()
