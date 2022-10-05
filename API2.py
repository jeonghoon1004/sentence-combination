from queue import Empty
from threading import Thread
from time import sleep

import logging
import argparse
import signal

from pathlib import Path
import sys
import json
import random
import os
import chromedriver_autoinstaller

from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver'
if os.path.exists(driver_path):
    print(f"chrome driver is installed: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver}")
    chromedriver_autoinstaller.install(True)

path_sentence = 'data/sentence.json'
path_temp = 'data/test_sentence.json'
path_temp_json = 'data/test_sentence_json.json'
path_writtend = 'data/writtend-'
url = "https://save-time.co.kr/product/%EC%97%AC%EB%A6%84%EB%A7%9E%EC%9D%B4-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%97%AC%ED%96%89%EA%B0%88%EB%95%8C-%EA%B2%9F%EC%95%84%EC%9B%83-%EB%A7%A4%ED%8A%B8/1823/category/73/display/1/#prdReview"
interval = 10

wrtFilterList = []

id = "네이버 페이 구매자"
pas = "pass"
star = 4
n = 1
input = "[배송]"
uuid = "default"
sentence = ""

if len(sys.argv) < 2:
    print("매개변수 부족")
    print("실행파일 n번 message id pas star(0~4) url")
    quit()

for v in range(1, len(sys.argv)):
        # print(sys.argv[v])
    if sys.argv[v] is None:
        print("매개변수 부족")
        print("실행파일 n번 message id pas star(0~4) url")
        quit()
    if v == 1:
        n = int(sys.argv[v])
    elif v == 2:
        input = sys.argv[v]
    elif v == 3:
        id = sys.argv[v]
    elif v == 4:
        pas = sys.argv[v]
    elif v == 5:
        star = int(sys.argv[v])
    elif v == 6:
        url = sys.argv[v]
    elif v == 7:
        uuid = sys.argv[v]
    else:
        print("too much")
        
# logging.basicConfig(level=logging.INFO, format='%(message_s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ReviewGen")

path_writtend = path_writtend + uuid + ".json"
file = Path(path_writtend)
file.touch(exist_ok=True)
file.write_text("[]", encoding="utf-8")
# if not file.exists():
    

def background_task(visible):
    print("|  back thread start!  |")
    error = []
    options = webdriver.ChromeOptions()
    # if visible == False:
    options.add_argument("--headless")
    # linux용
    options.add_argument('--no-sandbox')
    #options.add_argument('--single-process')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    # window용
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")

    # headless 숨기는 용도
    # options.add_argument("user-agent-Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6")

    # driver = webdriver.Chrome(driver_path, options=options)
    # driver.implicitly_wait(time_to_wait=interval)
    # print("driver start")
    for i in range(n):
        driver = webdriver.Chrome(driver_path, options=options)
        driver.implicitly_wait(time_to_wait=interval)
        print("driver start")
        buildSentence()
        text = sentence
        success_flag = False
        
        try:
            driver.get(url)
            print("|  url opened!  |")
            
            myElem = WebDriverWait(driver, interval).until(
                EC.presence_of_element_located((By.NAME, "review_widget3_0")))
            driver.switch_to.frame('review_widget3_0')  # iframe 이동

            # myElem = WebDriverWait(driver, interval).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "sf_review_save_btn")))
            element = WebDriverWait(driver, interval).until(EC.element_to_be_clickable((By.CLASS_NAME, "sf_review_save_btn")))
            # element.execute_script("arguments[0].click();", element)
            
            searchField = driver.find_element(
                By.CLASS_NAME, "sf_review_save_btn")
                # By.XPATH, "button[@class='sf_review_save_btn' @type='submit']")
            searchField.send_keys(Keys.ENTER)
            print("| review create start! |")
            driver._switch_to.default_content()
            myElem = WebDriverWait(driver, interval).until(
                EC.presence_of_all_elements_located((By.NAME, "review_widget11")))
            driver.switch_to.frame('review_widget11')
            # sleep(1)
            
            # div 하위 index click 전환 해야할수있음 - homenbox 이슈 이미 star로 전환 되어있음
            starField = driver.find_elements(
                By.CSS_SELECTOR, ".main_score .star_info > .not_star, .star")
            starField[star].click()

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
            
            print("| review information input |")
            
            btn_ok = driver.find_element(
                By.CSS_SELECTOR, ".sf_popup_bottom button[class='btn write']")
            
            btn_ok.send_keys(Keys.ENTER)
            sleep(0.8)
            print("| save btn(0.8) |")
            
            wrtFilterList.append(text)
            with open(path_writtend, "w", encoding="utf-8") as wt:
                wt.write(json.dumps(wrtFilterList))
            success_flag = True
            logger.info("url : {0}, status : {1}".format(url, success_flag))
        except TimeoutException as t:
            print("Loading took too much time!")
            # error.append(i)
            error.append("Loading took too much time!")
            error.append(t.args[0])
            logger.error("timout error {}".format(t))
            # driver.close()
            driver.quit()
            # messagebox.showinfo("리뷰 매크로", "Loading took too much time!")
        except Exception as e:
            # print("에러 내역 : {}".format(e))
            # error.append(i)
            print("에러")
            error.append(e.args[0])
            logger.error(e)
            # driver.close()
            driver.quit()
            # messagebox.showinfo("리뷰 매크로", "에러 내역 : {}".format(e))
        finally:
            print("status: {0},  {1} end".format(success_flag, i))
            logger.info("status: {0},  {1} end".format(success_flag, i))
            driver.quit()
    # messagebox.showinfo("리뷰 매크로", "{0}번 시행종료 \n error : {1}".format(n, error))
    # print("리뷰 등록", "{0}번 시행종료 \n error : {1}".format(n, error))
    print("리뷰 등록", " error : {} .".format(error) )
    
def buildSentence():
    form = input
    global sentence
    origin = sentence
    for key in OptionList:
        data = js_obj[key]
        t = "[{}]".format(key)
        if len(data) > 1:
            # random.choice
            tp = random.choice( data )
            
            # 직전값만 제거
            # if tp in origin:
            #     data.remove(tp)
            #     tp = random.choice( data )
            
            if tp in wrtFilterList:
                data.remove(tp)
            
            form = form.replace( t, tp )
        elif len(data) == 1:
            form = form.replace( t, data[0] )
    sentence = form
    
    # 필터 중복값이면 retry()
    requireLoop = False
    for w in wrtFilterList:
        if sentence in w:
            requireLoop = True
    if requireLoop:
        buildSentence()

# def stop(signum, frame):
#     # self.__stop = True
#     logger.info("Receive Signal {0}".format(signum))
#     logger.info("Stop Generate")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--log", help="log filename", default=None)
    # args = parser.parse_args()
    # log_file = args.log
    # if log_file:
    #     log_handler = logging.FileHandler(log_file)
    #     logger.addHandler(log_handler)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)
    file_handler = logging.FileHandler('API2.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # self.__stop = False

    # signal.signal(signal.SIGINT, stop)
    # signal.signal(signal.SIGTERM, stop)
    
    logger.info("Start Process Review Gen, PID {0}".format(os.getpid()))
    # while not self.__stop:
    
    # 쓰였던 글
    with open(path_writtend, "r", encoding="utf-8") as wrt:
        wrtFilterList = json.load(wrt)
    # data load
    with open(path_temp_json, "r", encoding="utf-8") as f:
        js_obj = json.load(f)
        OptionList = []
        for key in js_obj:
            OptionList.append(key)
    # data load
    
    # thread = Thread(target=background_task, daemon=True, name='category')
    # thread.start()
    
    background_task(visible=False)
