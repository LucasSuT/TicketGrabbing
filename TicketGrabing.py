from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


def test():
    driver.get('https://google.com')
    driver.get(
        'https://tix.fubonbraves.com/UTK0205_?PERFORMANCE_ID=P00KS5VK&GROUP_ID=40&PERFORMANCE_PRICE_AREA_ID=P00KSHKR')
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[9]/div[7]/div[2]/div[3]/div[2]/div/button[2]'))).click()
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="TBL"]/tbody')))
    rows = driver.find_elements(
        By.XPATH, '//*[@id="TBL"]/tbody/tr')
    needSeat = 4
    tempSeat = []
    seats = []
    for row in rows:
        colums = row.find_elements(By.TAG_NAME, 'td')
        for colum in colums:
            if colum.get_attribute('title'):
                seats.append(colum)
    seats.sort(key=lambda x: x.get_attribute('title'))
    for seat in seats:
        print(f"{seat.get_attribute('title')} ")
    preRow = ""
    preNumber = ""
    ConsecutiveSeats = 1
    for seat in seats:
        next = seat.get_attribute('title')
        tempSeat.append(seat)
        rowStartIndex = next.index("-")
        rowEndIndex = next.index("排")
        rowNumber = next[rowStartIndex+1:rowEndIndex]
        numberStartIndex = next.rindex("-")
        numberEndIndex = next.rindex("號")
        Number = next[numberStartIndex+1:numberEndIndex]
        # print(next)
        if preRow == rowNumber and int(preNumber) + 1 == int(Number):
            ConsecutiveSeats += 1
            preNumber = Number
            if needSeat == ConsecutiveSeats:
                print("----------------------")
                for t in tempSeat:
                    print(f"{t.get_attribute('title')} ")
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

def test2(need_seat):
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="TBL"]/tbody')))
    rows = driver.find_elements(
        By.XPATH, '//*[@id="TBL"]/tbody/tr')
    tempSeat = []
    seats = []
    for row in rows:
        colums = row.find_elements(By.TAG_NAME, 'td')
        for colum in colums:
            if colum.get_attribute('title'):
                seats.append(colum)
    seats.sort(key=lambda x: x.get_attribute('title'))
    for seat in seats:
        print(f"{seat.get_attribute('title')} ")
    preRow = ""
    preNumber = ""
    ConsecutiveSeats = 1
    for seat in seats:
        next = seat.get_attribute('title')
        tempSeat.append(seat)
        rowStartIndex = next.index("-")
        rowEndIndex = next.index("排")
        rowNumber = next[rowStartIndex+1:rowEndIndex]
        numberStartIndex = next.rindex("-")
        numberEndIndex = next.rindex("號")
        Number = next[numberStartIndex+1:numberEndIndex]
        # print(next)
        if preRow == rowNumber and int(preNumber) + 1 == int(Number):
            ConsecutiveSeats += 1
            preNumber = Number
            if need_seat == ConsecutiveSeats:
                print("----------------------")
                for t in tempSeat:
                    print(f"{t.get_attribute('title')} ")
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


def BuyTicket():
    # avoid over loading
    driver.execute_script("window.stop()")
    driver.get('https://google.com')
    driver.get('https://tix.fubonbraves.com/UTK0101_')
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/table/tbody/tr[5]/td[6]/a/span[1]/img'))).click() #日歷選擇
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[7]/app-table[1]/div/table/tbody/tr[2]/td[5]/button'))).click() #購買button
        #抓取所有可選擇區
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody/tr')))
        rows = driver.find_elements(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody/tr') #抓取所有可選擇區
        print(len(rows))
        for row in rows :
            print(row)
            colums = row.find_elements(By.TAG_NAME, 'td')
            if CheckAreaAvailable(json_object["area"],colums):
                row.click()
                test2(4)
                driver.back()
            print(row)
    except:
        print('Buy Fail\n\n\n\n\n\n')
        return 1
    return 1

def SelectSeat():
    # wait = WebDriverWait(driver, 5)
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TBL"]/tbody')))
    # rows = driver.find_elements(By.XPATH, '//*[@id="TBL"]/tbody/tr') #抓取每排座位
    # print(len(rows))
    # driver.back()
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[9]/div[7]/div[2]/div[3]/div[2]/div/button[2]'))).click()
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TBL"]/tbody/tr[2]/td[1]')))
    driver.execute_script("arguments[0].click();", element)
    print(element)
    print(element.get_attribute('title'))
    input("ddddddd")

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
        DownLoadVerifyCode()
        verify.clear()
        verify.send_keys(DecodeVerifyCode())
        # verify.send_keys('test')
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="popupuser"]/div/div[2]/div[3]/button[3]'))).click()
        if not CheckVerifyCode():
            print('verify fail')
            return 0
    except:
        print('Login Fail\n\n\n\n\n\n')
        return 0
    return 1


def CheckAreaAvailable(json_array, elements):
    for area in json_array:
        if area == "down":
            area = "下"
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


def DecodeVerifyCode():
    ocr = ddddocr.DdddOcr()
    with open('captcha_login.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res


def DownLoadVerifyCode():
    img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);
    """, driver.find_element('xpath', '//*[@id="master_chk_pic"]'))
    with open("captcha_login.png", 'wb') as image:
        image.write(base64.b64decode(img_base64))

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)
while 1:
    jsonFile = open('config.json','r')
    json_object = json.load(jsonFile)
    # for i in json_object:
    #     print(i, json_object[i])
    # while not Login() :
    #     print('login again')
    while not BuyTicket() :
        print('buy again')
    print('Exit\n\n\n')
    #driver.quit()
    break
