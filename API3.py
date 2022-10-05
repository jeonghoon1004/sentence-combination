# from concurrent.futures import ThreadPoolExecutor
# from multiprocessing import Pool
import threading
from time import sleep

import logging
from logging.handlers import TimedRotatingFileHandler

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
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, NoSuchFrameException

import numpy as np

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver'
if not os.path.exists(driver_path):
    print(f"install the chrome driver(ver: {chrome_ver}")
    chromedriver_autoinstaller.install(True)
else:
    print(f"chrome driver ver : {driver_path}")

# 단일 프로세싱일때..
# try:
#     for line in os.popen("ps ax | grep chrome | grep -v grep"):
#         fields = line.split()
#         pid = fields[0]
#         # kill terminal level SIGKILL no such
#         # terminate
#         os.kill(int(pid), signal.SIGTERM)
# except OSError:
#     print("Error : still running recent process - contact server engineer")

path_sentence = 'data/sentence.json'
path_temp = 'data/test_sentence.json'
path_temp_json = 'data/test_sentence_json.json'
path_writtend = 'data/writtend-'
path_recent = 'data/recent-dataset.json'
url = "https://save-time.co.kr/product/%EC%97%AC%EB%A6%84%EB%A7%9E%EC%9D%B4-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%97%AC%ED%96%89%EA%B0%88%EB%95%8C-%EA%B2%9F%EC%95%84%EC%9B%83-%EB%A7%A4%ED%8A%B8/1823/category/73/display/1/#prdReview"
interval = 30

wrtFilterList = []

id = "네이버 페이 구매자"
pas = "pass"
star = 4
n = 1
input = "[배송]"
uuid = "default"
sentence = ""

# 설정에 이전 동일 키 있는지 체크
def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False
    return True

# 실행시 필요 매개변수들 체크
if len(sys.argv) < 2:
    print("매개변수 부족")
    print("실행파일 n번 message id pas star(0~4) url")
    quit()

for v in range(1, len(sys.argv)):
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
        
# 로깅설정
# logging.basicConfig(level=logging.INFO, format='%(message_s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ReviewGen")

# 웹크롤링으로 리뷰 작성 동작 O(n)
def background_task(visible):
    print("|  back thread start!  |")
    error = []
    successCnt = 0
    failureCnt = 0
    options = webdriver.ChromeOptions()
    # if visible == False:
    options.add_argument("--headless")
    # options.headless = True
    # linux용
    options.add_argument('--no-sandbox')
    # options.add_argument('--single-process')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    # options.add_argument('--remote-debugging-port=9230')
    
    # window용
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")

    # headless 숨기는 용도
    # options.add_argument("user-agent-Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6")
    # driver = webdriver.Chrome(driver_path, options=options)
    # driver.implicitly_wait(time_to_wait=interval)
    # WebElement element = (new WebDriverWait(driver, 10)).until(ExpectedConditions.presenceOfElementLocated(By.id("element")));
    print("웹크롤링 시작")
    # for i in tqdm(range(n)):
    for i in range(n):
        logger.info("progress start pid : {0}".format(os.getpid()) )
        print("| 웹페이지 로딩 : 시작 |")
        # try:
        driver = webdriver.Chrome(driver_path, options=options)
        driver.implicitly_wait(time_to_wait=interval)
        print("| 웹페이지 로딩 : 세션 시작 |")
        # print(sys.argv)
        buildSentence2()
        logger.info("progress text gen")
        print("| 웹페이지 로딩 : 문장생성 |")
        text = sentence
        success_flag = False
        try:
            wait = WebDriverWait(driver, interval)
            driver.get(url)
            print("| 웹페이지 로딩 : 완료 |")
            # frame_widget3_0 = WebDriverWait(driver, interval).until(
            driver.switch_to.default_content()
            # wait.until(
            #     EC.frame_to_be_available_and_switch_to_it((By.NAME, 'review_widget3_0')))
            wait.until(
                EC.visibility_of_element_located((By.NAME, 'review_widget3_0')))
            
            driver.switch_to.frame('review_widget3_0')  # iframe 이동
            # driver.switch_to.frame(frame_widget3_0)

            # myFrame = WebDriverWait(driver, interval).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "sf_review_save_btn")))
            # btnSaveReview = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sf_review_save_btn")))
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sf_review_save_btn")))
            # btnSaveReview.send_keys(Keys.ENTER)
            searchField = driver.find_element(By.CLASS_NAME, "sf_review_save_btn")
            searchField.send_keys(Keys.ENTER)
            print("| 리뷰 입력 : 시작 |")
            driver.switch_to.default_content()
            # frame_widget11 = WebDriverWait(driver, interval).until(
            # wait.until(
            #     EC.frame_to_be_available_and_switch_to_it((By.NAME, 'review_widget11')))
            wait.until(
                EC.visibility_of_element_located((By.NAME, 'review_widget11')))
            driver.switch_to.frame('review_widget11')
            # driver.switch_to.frame(frame_widget11)
            # sleep(1)
            
            # div 하위 index click 전환 해야할수있음 - homenbox 이슈 이미 star로 전환 되어있음
            # starField = WebDriverWait(driver, interval).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".main_score .star_info > .not_star, .star")))
            starField = driver.find_elements(
                By.CSS_SELECTOR, ".main_score .star_info > .not_star, .star")
            starField[star].click()
            # logger.info(" star ")
            nameField = driver.find_element(
                By.CSS_SELECTOR, "input[name='login[name]']")
            nameField.send_keys(id)
            # logger.info(" name ")
            passField = driver.find_element(
                By.CSS_SELECTOR, "input[name='login[password]']")
            passField.send_keys(pas)
            # logger.info(" pass ")
            textField = driver.find_element(
                By.CSS_SELECTOR, "textArea[name='review_text']")
            textField.send_keys(text)
            # logger.info(" text ")

            privacyCheck = driver.find_element(
                By.CLASS_NAME, "sf_check_agree_privacy")
            privacyCheck.click()
            # logger.info(" privacy ")
            
            print("| 리뷰 입력 : 완료 |")
            logger.info("progress input [data] pid : {0}".format(os.getpid()))
            
            btn_ok = driver.find_element(
                By.CSS_SELECTOR, ".sf_popup_bottom button[class='btn write']")
            btn_ok.send_keys(Keys.ENTER)
            wait.until( EC.invisibility_of_element_located(btn_ok))
            # sleep(0.8)
            print("| 리뷰 등록(0.8) : 완료 |")
            logger.info("progress input complete pid : {0}".format(os.getpid()))
            success_flag = True
        except TimeoutException as t:
            print("| 등록 에러 : 타임아웃 에러 |")
            error.append("Loading took too much time!")
            error.append(t.args[0])
            logger.error("timout error {}".format(t))
            failureCnt+=1
            # driver.quit()
        except NoSuchWindowException:
            print("| 등록 에러 : NoSuchWindow 에러 |")
            error.append("webdriver can't find window!")
            error.append(t.args[0])
            logger.error("웹 로딩 error {}".format(t))
            failureCnt+=1
            # driver.quit()
        except NoSuchFrameException:
            print("| 등록 에러 : NoSuchFrame 에러 |")
            error.append("webdriver can't find frame!")
            error.append(t.args[0])
            logger.error("웹 로딩 error {}".format(t))
            failureCnt+=1
            # driver.quit()
        except Exception as e:
            print("| 에러 : 에러발생 |")
            error.append(e.args[0])
            logger.error(e)
            failureCnt+=1
            # driver.quit()
        finally:
            print("status: {0}, {1}, {2} end".format(success_flag, i, os.getpid()))
            logger.info("url: {0} status: {1}, n: {2} pid: {3} end".format(url, success_flag, i, os.getpid()))
            if success_flag:
                wrtFilterList.append(text)
                success_flag+=1
                # with open(path_writtend, "w", encoding="utf-8") as wt:
                #     wt.write(json.dumps(wrtFilterList))
                with open(path_writtend, "w", encoding="utf-8") as out_file:
                    json.dump(wrtFilterList, out_file, ensure_ascii=False, indent=6)
                    out_file.close()
            driver.switch_to.default_content()
            driver.close()
            if driver:
                driver.quit()
    # driver.switch_to.default_content()
    if driver:
        driver.quit()
    print("리뷰 등록", " error : {} .".format(error) )
    logger.info("END Process Review Gen, PID {0} succss: {1} failure: {2}".format(os.getpid(), successCnt, failureCnt))

# 핸들러 테스트
# threading 전역 인프리터 록에 의해 하나의 쓰레드만
# I/O 병목작업시 유효
# 멀티 코어 활용시 multiprocessing, concurrent.futures, ProcessPoolExecutor
# threadLocal = threading.local()
# def get_driver():
#     driver = getattr(threadLocal, 'driver', None)
#     if driver is None:
#         options = webdriver.ChromeOptions()
#         # if visible == False:
#         options.add_argument("--headless")
#         # options.headless = True
#         # linux용
#         options.add_argument('--no-sandbox')
#         # options.add_argument('--single-process')
#         options.add_argument('--disable-setuid-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--remote-debugging-port=9222')
#         # options.add_argument('--remote-debugging-port=9230')
#         driver = webdriver.Chrome(chrome_options=options)
#         setattr(threadLocal, 'driver', driver)
#     return driver
# def get_title(url): # ex)
#     driver = get_driver()
#     driver.get(url)
# def found_window(name):
#     def predicate(driver):
#         try: driver.switch_to.window(name)
#         except NoSuchWindowException:
#             return False
#         except NoSuchFrameException:
#             return False
#         else:
#             return True # found window
#     return predicate

# TODO : 크롬 드라이버를 병렬처리로 가능하게 테스트
# 병렬처리 프로세스 테스트
# def work_func(x):
#     print("value %s is in PID : %s" % (x, os.getpid()))
#     sleep(1)
#     return x**5
# def test_parallel():
#     start = int(time())
#     num_cores = 4
#     pool = Pool(num_cores)
#     print( pool.map(work_func, range(1,13)) )
#     print("***run time(sec) :", int(time()) - start)
# # 데이터 프레임 병렬 처리
# def work_func(data):
#     print('PID :', os.getpid())
#     data['length_str'] = data['Name'].apply(lambda x : len(x))
#     return data
# def parallel_dataframe(df, func, num_cores):
#     # 데이터를 코어수만큼 나누어 병렬처리
#     df_split = np.array_split(df, num_cores)
#     pool = Pool(num_cores)
#     df = pd.concat(pool.map(func, df_split))
#     # 메모리 정리
#     pool.close()
#     pool.join()
#     return df
# def test():
#     start = int(time())
#     my_dir = r"D:\Python\kaggle\titanic\\"
#     df = pd.read_csv(my_dir + "train.csv", dtype=str)
#     num_cores = 4
#     df = parallel_dataframe(df,work_func, num_cores)
#     print("***run time(sec) :", int(time()) - start)
    
    
#     drivers = [driver_setup() for _ in range(4)]
#     chunks = np.array_split(np.arange(1,126), 4)
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         bucket = executor.map(crawler, chunks, drivers)
#         results = [item for block in bucket for item in block]
#     [driver.quit() for driver in drivers]

# 문장 로드
# @Deprecated
# def buildSentence():
#     form = input
#     global sentence
#     origin = sentence
#     for key in OptionList:
#         data = js_obj[key]
#         t = "[{}]".format(key)
#         if len(data) > 1:
#             # random.choice
#             tp = random.choice( data )
            
#             if tp in wrtFilterList:
#                 data.remove(tp)
            
#             form = form.replace( t, tp )
#         elif len(data) == 1:
#             form = form.replace( t, data[0] )
#     sentence = form
    
#     # 필터 중복값이면 retry()
#     requireLoop = False
#     for w in wrtFilterList:
#         if sentence in w:
#             requireLoop = True
#     if requireLoop:
#         buildSentence()

# 문장로드 2
def buildSentence2():
    form = input
    global sentence
    for key in OptionList:
        data = js_obj[key]
        t = "[{}]".format(key)
        if len(data) > 1:
            if len(wrtFilterList) >= 1:
                sentencelist = np.setdiff1d(np.array(data), np.array(wrtFilterList))
            else:
                sentencelist = data
            # random.choice
            if len(sentencelist) < 1:
                print("status: {0}, {1} end : 태그 내 텍스트 부족!!!".format(False, os.getpid()))
                logger.info("url: {0} status: {1}, pid: {2} end : tag text needed!!".format(url, False, os.getpid()))
                return
            tp = random.choice(sentencelist)
            form = form.replace( t, tp )
        elif len(data) == 1:
            form = form.replace( t, data[0] )
            sentence = form
            return
    sentence = form

if __name__ == "__main__":
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler = logging.FileHandler('API3.log')
    # test handler when filesize is over : change file
    # file_handler = RotatingFileHandler('./API3.log', mode='a', maxBytes=5*1024*1024, backupCount=1, encoding='utf-8', delay=False)
    file_handler = TimedRotatingFileHandler('./API3TODAY.log', when="d", interval=1, backupCount=3, encoding="utf-8", delay=False, atTime=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.info("Start Process Review Gen, PID {0}".format(os.getpid()))
    
    # 과거 동일 상품리뷰 데이터셋 없을 경우 생성
    file_recent = Path(path_recent)
    if not file_recent.exists():
        file_recent.write_text("{}", encoding="utf-8")

    with open(file_recent, "r", encoding="utf-8") as rcnt:
        recentList = json.load(rcnt)
        if not is_json_key_present(recentList, url):
            # url 정보 없으면 uuid로 생성
            recentList[url] = uuid
            # recent 데이터셋에 기록
            with open(file_recent, "w", encoding="utf-8") as rcntw:
                json.dump(recentList, rcntw)
            rcntw.close()

            path_writtend = path_writtend + uuid + ".json"
            file = Path(path_writtend)
            if not file.exists():
                file.write_text("[]", encoding="utf-8")
        else:
            uuid = recentList[url]
            path_writtend = path_writtend + uuid + ".json"
        rcnt.close()
    
    # 입력되어진 문장 []
    with open(path_writtend, "r", encoding="utf-8") as wrt:
        wrtFilterList = json.load(wrt)
        wrt.close()
    # data load
    with open(path_temp_json, "r", encoding="utf-8") as f:
        js_obj = json.load(f)
        OptionList = []
        for key in js_obj:
            OptionList.append(key)
        f.close()
    # data load
    
    background_task(visible=False)
    
# 대용량 파일 (GB) 일시 chunksize 로 분할 로딩필요