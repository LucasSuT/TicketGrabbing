from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import ddddocr
import requests
import base64
import json
import ssl

# hide broser
'''
option = webdriver.ChromeOptions()
option.add_argument('Upgarde-Insecure-Requests = 1')
option.add_argument(
    'User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
option.add_argument('--headless')
option.add_argument('--window-size=1920,1080')
option.add_argument('--disable-gpu')
option.add_argument('lang=zh_CN.UTF-8')
# option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver =webdriver.Chrome(options=option)
'''

def SelectSeats(need_seat,range):
    if(need_seat>4):return 0
    print("range = ",range)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[9]/div[7]/div[2]/div[3]/div[2]/div/button[2]'))).click()
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="TBL"]/tbody')))
    rows = driver.find_elements(
        By.XPATH, '//*[@id="TBL"]/tbody/tr')
    tempSeat = []
    seats = []
    start_time = time.time()
    for row in rows:
        colums = row.find_elements(By.TAG_NAME, 'td')
        for colum in colums:
            title = colum.get_attribute('title')
            if title:
                letter,rowNumber,Number = split_seat(title)
                if len(range) <=2 :
                    if Number >= range[0] and Number <= range[1]:seats.append(colum)
                else :
                    seats.append(colum)
    print("掃描title執行時間：%.2f 秒" % (time.time() - start_time))
    start_time = time.time()
    seats = sorted(seats, key=seat_key)
    print("sort title執行時間：%.2f 秒" % (time.time() - start_time))
    # for seat in seats:
    #     print(f"{seat.get_attribute('title')} ")
    preRow = ""
    preNumber = ""
    ConsecutiveSeats = 1
    buy_seat = 0
    start_time = time.time()
    for seat in seats:
        if buy_seat >=need_seat : break
        next = seat.get_attribute('title')
        letter,rowNumber,Number = split_seat(next)
        tempSeat.append(seat)
        # rowStartIndex = next.index("-")
        # rowEndIndex = next.index("排")
        # rowNumber = next[rowStartIndex+1:rowEndIndex]
        # numberStartIndex = next.rindex("-")
        # numberEndIndex = next.rindex("號")
        # Number = next[numberStartIndex+1:numberEndIndex]
        letter,rowNumber,Number = split_seat(next)
        # print(next)
        if (letter == 'B1' or letter == 'B2') and  int(preNumber) == 16:
            preRow = rowNumber
            preNumber = Number
            tempSeat = []
            tempSeat.append(seat)
            ConsecutiveSeats = 1
        else if preRow == rowNumber and int(preNumber) + 1 == int(Number):
            ConsecutiveSeats += 1
            preNumber = Number
            if need_seat == ConsecutiveSeats:
                # print("----------------------")
                for t in tempSeat:
                    # print(f"{t.get_attribute('title')} ")
                    driver.execute_script("arguments[0].click();", t)
                buy_seat += ConsecutiveSeats
                preRow = ""
                preNumber = ""
                tempSeat = []
                ConsecutiveSeats = 1
        else:
            preRow = rowNumber
            preNumber = Number
            tempSeat = []
            tempSeat.append(seat)
            ConsecutiveSeats = 1
    verify = driver.find_element('xpath', '//*[@id="CHK"]')
    print("選擇執行時間：%.2f 秒" % (time.time() - start_time))
    while(buy_seat>0):
        DownLoadVerifyCode('//*[@id="chk_pic"]')
        verify.clear()
        verify.send_keys(DecodeVerifyCode())
        # verify.send_keys('tet')
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="addcart"]'))).click()
        if CheckBuyVerifyCode() :
            break
        ClickDialog()
    driver.back()
    return buy_seat


def BuyTicket(url,num_ticket):
    # avoid over loading
    driver.execute_script("window.stop()")
    # driver.get('https://google.com')
    # driver.get('https://tix.fubonbraves.com/UTK0101_')
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    try:
        # wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[5]/div[1]/div[1]/div[2]/table/tbody/tr[5]/td[7]/a/span[1]/img'))).click() #日歷選擇
        # wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[7]/app-table[1]/div/table/tbody/tr[2]/td[5]/button'))).click() #購買button
        areas = json_object["area"]
        buy_seat = 0
        while(1) :
            if(len(areas) == 0 or buy_seat>=4):break
            refresh_flag = 0 #refresh_flag判斷有沒有刷新頁面過
            #抓取所有可選擇區
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody/tr')))
            rows = driver.find_elements(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody/tr') #抓取所有可選擇區
            del rows[0]
            for row in rows :
                area_index = 0
                colums = row.find_elements(By.TAG_NAME, 'td')
                for area in areas :
                    if area in colums[1].text :
                        if CheckAreaAvailable(area,colums):
                            row.click()
                            buy_seat += SelectSeats(num_ticket,json_object["range"][area])
                            print('Buy ',buy_seat,' Tickets')
                            driver.refresh()
                            refresh_flag = 1 
                        del areas[area_index]
                        break
                    area_index = area_index + 1
                if(refresh_flag ==1): #有刷新頁面會導致rows資料不正確需要重新抓取
                    break
    except:
        print('Buy Fail\n\n\n\n\n\n')
        return 0
    return 1

def Login():
    driver.execute_script("window.stop()")
    driver.get('https://tix.fubonbraves.com/UTK0101_')  # login page
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="userbutton"]/img'))).click()
        account = driver.find_element('xpath', '//*[@id="MASTER_ACCOUNT"]')
        account.clear()
        account.send_keys(json_object['account'])
        password = driver.find_element('xpath', '//*[@id="MASTER_PASSWORD"]')
        password.clear()
        password.send_keys(json_object['password'])
        verify = driver.find_element('xpath', '//*[@id="MASTER_CHK"]')
        DownLoadVerifyCode('//*[@id="master_chk_pic"]')
        verify.clear()
        verify.send_keys(DecodeVerifyCode())
        # verify.send_keys('test')
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="popupuser"]/div/div[2]/div[3]/button[2]'))).click()
        if not CheckVerifyCode():
            print('verify fail')
            return 0
    except:
        print('Login Fail\n\n\n\n\n\n')
        return 0
    return 1


def CheckAreaAvailable(area, elements):
    try:
        if area in elements[1].text and elements[3].text != "售完":
            print("contain ", area, " in ", elements[1].text)
            return 1
    except:
        return 0


def CheckVerifyCode():
    try:
        wait = WebDriverWait(driver, 1)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[7]/div[3]/div/button'))).click()
    except:  # cant capture alert represent verify success
        return 1
    return 0

def ClickDialog():
    try:
        wait = WebDriverWait(driver, 1)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'ui-button'))).click()
    except:  # cant capture alert represent verify success
        return 1
    return 0

def CheckBuyVerifyCode():
    try:
        wait = WebDriverWait(driver, 1)
        message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-dialog-content'))).text
        print('start ',message,' end')
        if '結帳' not in message:
            return 0
    except:  # cant capture alert represent verify success
        return 1
    return 1

def DecodeVerifyCode():
    ocr = ddddocr.DdddOcr()
    with open('captcha_login.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res


def DownLoadVerifyCode(xpath):
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)))
    img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);
    """, driver.find_element('xpath', xpath))
    with open("captcha_login.png", 'wb') as image:
        image.write(base64.b64decode(img_base64))

def seat_key(seat):
    # 將座位號拆分成排數、字母、號碼
    row, letter, number = seat.get_attribute('title').split('-')
    # 將排數轉成整數，並將字母轉成對應的數值
    # 'A' -> 0, 'B' -> 1, 'C' -> 2, 以此類推
    row_num = row.split('區')[0]
    letter_num = letter.split('排')[0]
    letter_num = ord(letter_num)-ord('A')
    # 將號碼轉成整數
    number_num = int(number.split('號')[0])
    return (letter_num,number_num)

def split_seat(seat):
    letter,row,number = seat.split('-')
    letter = letter.split('區')[0]
    row = row.split('排')[0]
    number = number.split('號')[0]
    return letter,row,number

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)
while 1:
    jsonFile = open('config.json','r')
    json_object = json.load(jsonFile)
    # for i in json_object:
    #     print(i, json_object[i])
    # print(json_object['range']['A2'])
    while not Login() :
        print('login again')
    while not BuyTicket('https://tix.fubonbraves.com/UTK0204_?PERFORMANCE_ID=P00KT9QT&PRODUCT_ID=P00JXL75',2) :
        print('buy again')
    print('Exit\n\n\n')

    # jsonFile = open('config.json','r')
    # json_object = json.load(jsonFile)
    # Login()
    # BuyTicket('https://tix.fubonbraves.com/UTK0204_?PERFORMANCE_ID=P00KT9QT&PRODUCT_ID=P00JXL75',2)
    # print('Exit\n\n\n')
    # time.sleep(15)
    # driver.quit()

    break
