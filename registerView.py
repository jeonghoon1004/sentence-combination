#
# @brief 문장 입력 화면
#
# Created registerView.py on Thu Jun 02 2022
#
# @author kim jeonghoon <kyg1084@gmail.com>
#
# @copyright (c) 2022 DPJ
#

from threading import Thread
import tkinter as tk
from tkinter import messagebox
from tkinter import BOTH, FALSE, LEFT, N, NW, RIGHT, TRUE, VERTICAL, Y, Scrollbar, filedialog
import tkinter.ttk as ttk
from pynput.keyboard import Listener, Key, KeyCode
import json
import clipboard
import re

from extract import extractExcel
from koreanTokenizer import kmran, pprint

class InputApplication(ttk.Frame):
    # 단축키
    HOT_KEYS = {
        'self.autoCopy': set([ Key.ctrl_l, KeyCode(char= chr(ord("C")-64))]),
        'self.btnInputClick': set([ Key.ctrl_l, Key.space])
    }
    path_sentence = 'data/sentence.json'
    path_temp = 'data/test_sentence.json'
    path_temp_json = 'data/test_sentence_json.json'
    def resizeCanvas(self, event):
        width = event.width - 4
        self.canvas.itemconfig("self.contentWindow", width=width)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    def __init__(self, parent):
        
        self.outer = tk.Frame(parent, width=0, height=0)
        self.canvas = tk.Canvas(self.outer, width=280)
        self.scroll = tk.Scrollbar(self.outer, command=self.canvas.yview, width=20)

        # super().__init__(self.canvas)
        ttk.Frame.__init__(self, self.canvas, width=0, height=0)
        self.contentWindow = self.canvas.create_window((0,0), window=self, anchor=NW, width=300)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y", expand=True)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.bind("<Configure>", self.resizeCanvas)
        
        self.pack = self.outer.pack
        self.place = self.outer.place
        self.grid = self.outer.grid
        
        self.loadJson()
        
        # Gui paint
        lbl = ttk.Label(self, text="문장 등록")
        lbl.pack()
        describtion = ttk.Label(self, text="ctrl + c - 복사한 텍스트 -> 입력창 \nctrl + space - 현재 카테고리에 등록")
        describtion.pack()
        
        # input
        self.variable = tk.StringVar(self)
        self.textEntry = tk.StringVar()
        txt = ttk.Entry(self, textvariable = self.textEntry)
        txt.pack()
        # category select
        opt = ttk.OptionMenu(self, self.variable, self.OptionList[0], *self.OptionList)
        opt.pack()
        btn = ttk.Button(self, text="등록", command=self.btnInputClick)
        btn.pack()
        # lbl1 = ttk.Label(self, text=self.js_obj, wraplength=200)
        # lbl1.pack()
        # ~Gui paint
        
        # select box eventListener
        def callback(*args):
            # print("selected {}".format(self.variable.get()))
            # print("and index {}".format(self.OptionList.index(self.variable.get())))
            # lbl1.configure(text="{}".format( self.js_obj[self.variable.get()] ))
            pass
        # ~select box eventListener
        self.variable.trace("w", callback)
        self.variable.set(self.OptionList[0])
        
        btnFolder = ttk.Button(self, text="리뷰 엑셀 폴더", command=self.openFolder)
        btnFolder.pack()
        btnListup = ttk.Button(self, text="리뷰글 목록", command=self.attachContext)
        btnListup.pack()
        self.textList = tk.StringVar(self)
        lblList = ttk.Label(self, textvariable=self.textList, wraplength=200)
        lblList.pack()
        
        
        # hotkey listener
        self.store = set()
        listener =  Listener(on_press=self.handlePress, on_release=self.handleRelease)
        listener.start()
    def loadJson(self):
        # data load
        # array <=> object convert   obj.keys() = self.OptionList
        with open(self.path_temp_json, "r", encoding="utf-8") as f:
            self.js_obj = json.load(f)
            self.OptionList = []
            for key in self.js_obj:
                self.OptionList.append(key)
        # data load
    # btn eventListener    
    def background_task(msg_queue):
        path_temp_json = 'data/test_sentence_json.json'
        extracts = extractExcel()
        extracts.getText()
        # extracts.getText(idx=tuple(range(10)))
        # print( "jsarray : {}".format( len(extracts.js_array) ) )
        # print( "content : {}".format( len(extracts.TextList) ) )
        # print( "content ==== \n{}\n============".format( extracts.TextList ) )
        
        # self.textList.set( extracts.TextList )
        
        # TODO : 추출된 리뷰 텍스트를 분류 @see koreanTokenizer
        # 전처리
        stopword = ['후드', '림프', '마사지'] #금지어
        # ctag = ['배송','만족','품질','감사'] #예상 태그
        with open(path_temp_json, "r", encoding="utf-8") as f:
            sData = json.load(f)
        for key in sData:
            sData[key].clear()
        # sData = {
        #     "배송":[],
        #     "만족":[],
        #     "주문":[],
        #     "품질":[],
        #     "감사":[],
        #     "가격":[],
        #     "편리":[],
        #     "사용":[],
        #     "부모":[],
        #     "효과":[],
        #     "굿":[],
        #     "아이디어":[],
        #     "평생":[],
        #     "대박":[],
        #     "모호함":[] # 기타항목 - 추후 업데이트 및 기타용도
        # }
        ctag = sData.keys()
        
        # TODO : 문장 split ?
        # TODO : 구매자 평점 상위
        only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                "]+", flags=re.UNICODE)
        for text in extracts.TextList:
            # koreanTokenizer().morph(text=text)
            # koreanTokenizer().getTags(text=text)
            # pprint( kmran().pos(text=text) )
            
            text = only_BMP_pattern.sub(r'', text)
            nouns = kmran().nouns(text=text)
            if any( item in nouns for item in stopword ):
                # 금지어 포함
                pass
            else:
                # LOG
                # str = "%s <=> %s\n" % ( nouns, text )
                # print ( str )
                # with open(self.path_temp, "a+", encoding="utf-16") as f:
                #     f.write(str)
                
                if any( item in nouns for item in ctag):
                    # 걸린 item name
                    for item in ctag:
                        if item in nouns:
                            sData[item].append(text)
                            print("[ %s ] : %s" % (item, text))
                    # with open(path_temp_json, "w", encoding="utf-8") as f:
                    #     json.dump( sData , f, ensure_ascii=False, indent=4)
                else: 
                    # print("not checked")
                    sData["모호함"].append(text)
            pass
        # 결과 주입
        with open(path_temp_json, "w", encoding="utf-8") as f:
            json.dump( sData , f, ensure_ascii=False, indent=4)
        print("END")
        messagebox.showinfo("json 등록", "종료")
        pass
    def openFolder(self, window) -> None:
        dir_path = filedialog.askdirectory(parent=window,initialdir="/",title='최상위 폴더 선택')
        print("\ndir_path : ", dir_path)
        extractExcel().read(dir_path)
    def attachContext(self) -> None:
        self.thread = Thread(target=self.background_task, daemon=True, name='category')
        self.thread.start()
        
    def btnInputClick(self):  # ctrl + space
        print(self.js_obj[self.variable.get()])
        self.js_obj[self.variable.get()].append(self.textEntry.get())
        print(self.js_obj[self.variable.get()])
        with open(self.path_temp_json, "w", encoding="utf-8") as f:
            json.dump(self.js_obj, f, ensure_ascii=False, indent=4)
        # refresh
        self.loadJson()
        self.variable.set(self.variable.get())
    def autoCopy(self):  # ctrl + c
        print( 'auto copy () - {}'.format(clipboard.paste()))
        self.setTextInput(clipboard.paste())
    def setTextInput(self, text):
        self.textEntry.set(text)
        # self.btnInputClick() # 자동 등록
        pass
    # ~btn eventListener
    def handlePress( self, key ):
        self.store.add( key )
        # print( 'Press: {}'.format( self.store ))
    def handleRelease( self, key ):
        # print( 'Released: {}'.format( key ))
        # INPUT HOT KEY FUNCTION
        for action, trigger in self.HOT_KEYS.items():
            CHECK = all([ True if triggerKey in self.store else False for triggerKey in trigger ])
            if CHECK:
                try:
                    func = eval( action )
                    if callable( func ):
                        func()
                except NameError as err:
                    print( err )
        if key in self.store:
            self.store.remove( key )
        # if key == Key.esc:
        #     root.destroy()
        #     quit(0)

if __name__ == "__main__": # 직접 실행된 모듈일 경우
    root = tk.Tk()
    root.title("문장 조합기")
    root.geometry('300x300')
    root.attributes('-topmost',True)
    
    # scrollbar = Scrollbar(root)
    # scrollbar.pack( side = RIGHT, fill=Y)
    
    frame = InputApplication(root)
    frame.pack( fill=BOTH, expand=True )
    # frame.pack(fill="both", expand=True)
    # frame.pack( side = LEFT, fill=BOTH)
    
    # scrollbar.config( command = frame.canvas.yview )
    
    root.mainloop()