#
# @brief 시작 제어
#
# Created main.py on Tue Jun 07 2022
#
# @author kim jeonghoon <kyg1084@gmail.com>
#
# @copyright (c) 2022 DPJ
#

# pyinstaller --exclude-module _bootlacale --onefile main.py

import tkinter as tk
from tkinter import BOTH, PhotoImage, filedialog
import tkinter.ttk as ttk

import writeView
import registerView
# import koreanTokenizer as kt

from extract import extractExcel

# 776] WARNING: file already exists but should not: C:\Users\com\AppData\Local\Temp\_MEI327762\torch\_C.cp310-win_amd64.pyd

class MyApp():
    def switchFrame(self, classParam):
        if self.nowFrame:
            if self.nowFrame.outer:
                self.nowFrame.outer.destroy()
            self.nowFrame.destroy()
        self.nowFrame = classParam
        self.nowFrame.pack( fill=BOTH, expand=True )
    def currTransparent(self, v):
        window.attributes('-alpha', v)
    # def extractReview(self, url):
        # TODO : 리뷰글 크롤링 추가 ( review url )
        # test url   -    http://www.chungsosin.com/shop/shopdetail.html?branduid=2129822&xcode=001&mcode=001&scode=&type=X&sort=manual&cur_code=001&GfDT=a2l3UA%3D%3D
        # class = review_list_v2__message js-translate-review-message
        # kt.koreanTokenizer.morph("txt")
        
        # TODO : crawlUrl.json에 리뷰글 데이터 출력
        # TODO : 카테고리별로 문장 구분해서 sentence.json 업데이트

    def openFolder(self, window) -> None:
        dir_path = filedialog.askdirectory(parent=window,initialdir="/",title='Please select a directory')
        print("\ndir_path : ", dir_path)
        extractExcel().read(dir_path)
    def attachContext(self) -> None:
        extracts = extractExcel()
        print( "jsarray : {}".format( len(extracts.js_array) ) )
        print( "content : {}".format( len(extracts.TextList) ) )
        print( "content ==== \n{}\n============".format( extracts.TextList ) )
    # def crawlReview(self, window) -> None:
    #     popup = tk.Toplevel(window)
    #     popup.geometry("200x100")
    #     popup.title("url input")
    #     tk.Label(popup, text= "url", font=('Mistral 18 bold')).place(x=30, y=15)
    #     url = tk.StringVar(popup)
    #     url_entry = ttk.Entry(popup, textvariable=url).place(x=30, y=50)
    #     def callback1(event):
    #         # temp url
    #         url.set("http://www.chungsosin.com/shop/shopdetail.html?branduid=2129822&xcode=001&mcode=001&scode=&type=X&sort=manual&cur_code=001&GfDT=a2l3UA%3D%3D")
    #         classname = "review_list_v2__message js-translate-review-message" # "classname"
    #         print('url : {}'.format(url.get()))
    #         self.extractReview(url, classname)
    #     popup.bind('<Return>', callback1)

    def __init__(self, window):
        self.nowFrame = None
        window.title("문장 조합기")
        window.geometry('400x480')
        window.attributes('-topmost',True)

        # 투명조절
        scale = ttk.Scale(window, command=self.currTransparent, orient="horizontal", from_=0.3, to=1, value=1)
        scale.pack(side=tk.TOP, anchor=tk.NE)

        # MENU #
        allMenu = tk.Menu(window)
        menu = tk.Menu(allMenu, tearoff=0)
        menu.add_command(label='등록', command=lambda:self.switchFrame(registerView.InputApplication(window)))
        menu.add_command(label='조합', command=lambda:self.switchFrame(writeView.WriteApplication(window)))
        menu.add_command(label='리뷰글 엑셀', command=lambda:self.openFolder(window=window))
        # menu.add_command(label='리뷰글 URL', command=lambda:self.crawlReview(window=window))
        menu.add_command(label='리뷰글 원문', command=lambda:self.attachContext())
        self.switchFrame(registerView.InputApplication(window))
        allMenu.add_cascade(label='화면', menu=menu)
        onTop = tk.BooleanVar()
        onTop.set(True)
        def callback(*args):
            print(onTop.get())
            window.attributes('-topmost', onTop.get())
        onTop.trace("w", callback)
        menu2 = tk.Menu(allMenu, tearoff=0)
        menu2.add_checkbutton(label="onTop", variable=onTop)
        allMenu.add_cascade(label="설정", menu=menu2)
        window.config(menu=allMenu)
        window.mainloop()

if __name__ == "__main__": # 직접 실행된 모듈일 경우
    window = tk.Tk()
    photo = PhotoImage(file="./data/logo.png")
    window.iconphoto(False, photo)
    MyApp(window)