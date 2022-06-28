#
# @brief 조합, 클립보드 attach
#
# Created writeView.py on Tue Jun 07 2022
#
# @author kim jeonghoon <kyg1084@gmail.com>
#
# @copyright (c) 2022 DPJ
#

from threading import Thread
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from turtle import width
from pynput.keyboard import Listener, Key, KeyCode
import json
import clipboard
import random
import os
import chromedriver_autoinstaller

# import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
# from webdriver_auto_update import check_driver


def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        make_draggable(self)
class DnDFrame(DragDropMixin, tk.Frame):
    pass

# tk.Frame
class WriteApplication(tk.Frame):
    HOT_KEYS = {
        # refresh setence and ready to clipboard
        'self.buildSentence': set([ Key.ctrl_l, Key.space]),
        'self.btnRunClick': set([ Key.ctrl_l, Key.enter])
    }
    path_sentence = 'data/sentence.json'
    path_temp = 'data/test_sentence.json'
    path_temp_json = 'data/test_sentence_json.json'
    url = "https://save-time.co.kr/product/%EC%97%AC%EB%A6%84%EB%A7%9E%EC%9D%B4-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%97%AC%ED%96%89%EA%B0%88%EB%95%8C-%EA%B2%9F%EC%95%84%EC%9B%83-%EB%A7%A4%ED%8A%B8/1823/category/73/display/1/#prdReview";
    def __init__(self, parent):
        # super().__init__(parent
        self.outer = None
        tk.Frame.__init__(self, parent)
        
        self.loadJson()
        
        self.variable = tk.StringVar(self)
        self.variable.set(self.OptionList[0])
            
        lbl = ttk.Label(self, text="문장 조합")
        lbl.pack()
        describtion = ttk.Label(self, text="ctrl + space - 클립보드에 탑재 *ctrl+v로 붙여넣기(매크로 권장)\nex)[카테고리명] blah [카테고리명]...")
        describtion.pack()
        
        # box = ttk.Combobox(self, values=self.OptionList)
        # box.pack()
        # box.set(self.OptionList[0])
        
        lbl = tk.Label(self)
        lbl.pack(side=tk.LEFT)
        
        listbox = tk.Listbox(lbl, width=10)
        listbox.insert(tk.END, *self.OptionList)
        listbox.pack()
        
        self.chkvariable = tk.BooleanVar(self)
        chkbox = tk.Checkbutton(lbl, text="브라우저", variable=self.chkvariable)
        chkbox.pack()
        
        # self.textEntry = tk.StringVar()
        # txt = ttk.Entry(self, textvariable=self.textEntry, width=52)
        # txt.pack()
        
        self.input = tk.Text(self, height=5, width=52)
        self.input.pack()
        
        sep2 = tk.Label(self, text="∥ 출력")
        sep2.pack()
        
        self.result = tk.Text(self, height=5, width=52)
        self.result.pack()
        
        self.store = set()
        listener =  Listener(on_press=self.handlePress, on_release=self.handleRelease)
        listener.start()
        
        # url
        lbUrl = ttk.Label(self, text="url : 현재 해당 url 외에 추가시 협의 필요")
        lbUrl.pack()
        self.textUrlEntry = tk.StringVar(self)
        textUrl = ttk.Entry(self, textvariable = self.textUrlEntry)
        textUrl.pack()
        self.textUrlEntry.set(self.url)
        
        # 아이디
        lbId = ttk.Label(self, text="아이디")
        lbId.pack()
        self.textIdEntry = tk.StringVar(self)
        textId = ttk.Entry(self, textvariable = self.textIdEntry)
        textId.pack()
        self.textIdEntry.set("네이버 페이 구매자")
        
        # 비밀번호
        lbPass = ttk.Label(self, text="비밀번호")
        lbPass.pack()
        self.textPassEntry = tk.StringVar(self)
        textPass = ttk.Entry(self, textvariable = self.textPassEntry)
        textPass.pack()
        self.textPassEntry.set("pass")
        # 별점
        lbStar = ttk.Label(self, text="별점")
        lbStar.pack()
        self.textStarEntry = tk.StringVar(self)
        textStar = ttk.Entry(self, textvariable = self.textStarEntry)
        textStar.pack()
        self.textStarEntry.set("5")
        # 반복시행
        lbCount = ttk.Label(self, text="반복시행")
        lbCount.pack()
        self.textRepeatEntry = tk.StringVar(self)
        self.textRepeatEntry.set(1)
        textRepeat = ttk.Entry(self, textvariable = self.textRepeatEntry)
        textRepeat.pack()
        self.textRepeatEntry.set("1")
        
        
        btn = ttk.Button(self, text="시행", command=self.btnRunClick)
        btn.pack()
        
        
        # div class sf_review_save > btn class sf_review_save_btn  | submit
        # 별점체크 (확인 필요)
        # div class score_info > input name score[]
        # div class score_info > div star_info
        # 로그인
        # div class login_info > div user_name > input name login[name]
        # div class login_info > div user_pass > input name login[password]
        # 텍스트
        # div class sf_write > textArea name review_text
        # 동의 체크
        # div class sf_agree_privacy_head > input class sf_check_agree_privacy
        # 확인 버튼
        # div class sf_popup_bottom > btn class btn write
    def btnRunClick(self):
        self.thread = Thread(target=self.background_task, daemon=True, name='category')
        self.thread.start()
        pass
    def background_task(self):
        # url = "https://save-time.co.kr/product/%EC%97%AC%EB%A6%84%EB%A7%9E%EC%9D%B4-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%97%AC%ED%96%89%EA%B0%88%EB%95%8C-%EA%B2%9F%EC%95%84%EC%9B%83-%EB%A7%A4%ED%8A%B8/1823/category/73/display/1/#prdReview";
        url = self.textUrlEntry.get()
        interval = 7 # sec
        id = self.textIdEntry.get()
        pas = self.textPassEntry.get()
        star = int(self.textStarEntry.get()) - 1
        n = int(self.textRepeatEntry.get())
        
        # n = 2
        # id = "네이버 페이 구매자"
        # star = 4
        error = []
        
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        driver_path = f'./{chrome_ver}/chromedriver.exe'
        if os.path.exists(driver_path):
            print(f"chrom driver is installed: {driver_path}")
        else:
            print(f"install the chrome driver(ver: {chrome_ver}")
            chromedriver_autoinstaller.install(True)
        if self.chkvariable.get():
            # driver = webdriver.Chrome("data/chromedriver102.exe")
            driver = webdriver.Chrome(driver_path)
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument('window-size=1920x1080')
            # driver = webdriver.Chrome("data/chromedriver102.exe", options=options)
            driver = webdriver.Chrome(driver_path, options=options)
        
        driver.implicitly_wait(time_to_wait=interval)
        
        for i in range(n):
            self.buildSentence()
            text = self.result.get("1.0", tk.END)
            driver.get(url)
            try:
                myElem = WebDriverWait(driver, interval).until(
                    EC.presence_of_element_located((By.NAME, "review_widget3_0")))
                driver.switch_to.frame('review_widget3_0')  # iframe 이동

                # myElem = WebDriverWait(driver, interval).until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "sf_review_save_btn")))
                element = WebDriverWait(driver, interval).until(EC.element_to_be_clickable((By.CLASS_NAME, "sf_review_save_btn")))
                # element.execute_script("arguments[0].click();", element)

                searchField = driver.find_element(
                    By.CLASS_NAME, "sf_review_save_btn")
                # searchField.click()
                searchField.send_keys(Keys.ENTER)
                
                driver._switch_to.default_content()
                myElem = WebDriverWait(driver, interval).until(
                    EC.presence_of_all_elements_located((By.NAME, "review_widget11")))
                driver.switch_to.frame('review_widget11')
                # sleep(1)
                
                # div 하위 index click 전환 해야할수있음 - homenbox 이슈 이미 star로 전환 되어있음
                # starField = driver.find_elements(By.CSS_SELECTOR, ".main_score .star_info > .not_star")
                starField = driver.find_elements(
                    By.CSS_SELECTOR, ".main_score .star_info > .not_star, .star")
                starField[star].click()

                # $(scoreInfo).find('.star_info .star, .star_info .not_star').on('click', function (e) {
                # var score = $(this).index() + 1;
                # var scoreWrap = $(this).parents('.score_info');

                nameField = driver.find_element(
                    By.CSS_SELECTOR, "input[name='login[name]']")
                nameField.send_keys(id)
                passField = driver.find_element(
                    By.CSS_SELECTOR, "input[name='login[password]']")
                passField.send_keys(pas)

                textField = driver.find_element(
                    By.CSS_SELECTOR, "textArea[name='review_text']")
                textField.send_keys(text)

                privacyCheck = driver.find_element(
                    By.CLASS_NAME, "sf_check_agree_privacy")
                privacyCheck.click()

                btn_ok = driver.find_element(
                    By.CSS_SELECTOR, ".sf_popup_bottom button[class='btn write']")
                btn_ok.send_keys(Keys.ENTER)
                myElem = WebDriverWait(driver, interval).until(
                    EC.presence_of_all_elements_located((By.NAME, "review_widget3_0")))
                # sleep(2)
            except TimeoutException:
                print("Loading took too much time!")
                error.append(i)
                # messagebox.showinfo("리뷰 매크로", "Loading took too much time!")
            except Exception as e:
                print("에러 내역 : {}".format(e))
                error.append(i)
                # messagebox.showinfo("리뷰 매크로", "에러 내역 : {}".format(e))
            finally:
                print("{} end".format(i))
        driver.quit()
        messagebox.showinfo("리뷰 매크로", "{0}번 시행종료 \n error : {1}".format(n, error))
    def loadJson(self):
        # data load
        with open(self.path_temp_json, "r", encoding="utf-8") as f:
            self.js_obj = json.load(f)
            self.OptionList = []
            for key in self.js_obj:
                self.OptionList.append(key)
                
        # data load
    def buildSentence( self ):
        # TODO : 금지어 추가 (타품목 언급 관련)
        
        # form = self.textEntry.get()
        form = self.input.get("1.0", tk.END)
        # for form.split("{{*}}")[i].replace("{{categoryname}}", randomchoice(category) )
        origin = self.result.get("1.0", tk.END)
        
        for key in self.OptionList:
            data = self.js_obj[key]
            t = "[{}]".format(key)
            if len(data) > 1:
                # random.choice
                tp = random.choice( data )
                if tp in origin:
                    data.remove(tp)
                    tp = random.choice( data )
                form = form.replace( t, tp )
            elif len(data) == 1:
                form = form.replace( t, data[0] )
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, form)
        # clipboard
        clipboard.copy(form)
    # keyEvent
    def handlePress( self, key ):
        self.store.add( key )
    def handleRelease( self, key ):
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

# run this file class
if __name__ == "__main__":
    root = tk.Tk()
    root.title("문장 조합기")
    root.geometry('300x450')
    root.attributes('-topmost',True)
    # make_draggable(tk.Frame(root))
    WriteApplication(root).pack()
    root.mainloop()