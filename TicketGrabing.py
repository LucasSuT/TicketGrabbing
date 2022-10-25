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

#hide broser
'''
option = webdriver.ChromeOptions()
option.add_argument('Upgarde-Insecure-Requests = 1')
option.add_argument('User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
option.add_argument('--headless')
option.add_argument('--window-size=1920,1080')
option.add_argument('--disable-gpu')
option.add_argument('lang=zh_CN.UTF-8')
#option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver =webdriver.Chrome(options=option)
'''

driver = webdriver.Chrome()

def BuyTicket():
    #avoid over loading
    driver.execute_script("window.stop()")
    driver.get('https://google.com')
    driver.get('https://tix.fubonbraves.com/UTK0101_')
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/table/tbody/tr[2]/td[6]'))).click()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="PerformanceListTable"]/table/tbody/tr[2]/td[5]'))).click()
        wait = WebDriverWait(driver, 5)

        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody')))
        #elememt = driver.find_elements('xpath','/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody/tr[2]')
        rows = driver.find_elements(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div/div[3]/div/div/table/tbody/tr')
        print(len(rows))
        for row in rows :
            colums = row.find_elements(By.TAG_NAME, 'td')
            for colum in colums :
                print(colum.text)
    except:
        print('Buy Fail\n\n\n\n\n\n')
        sleep(5)
        #return 1
        return 1
    finally:
        print('Exit')
        return 1


def Login():
    driver.get('https://tix.fubonbraves.com/UTK0101_') #login page
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userbutton"]/img'))).click()
        account = driver.find_element('xpath','//*[@id="MASTER_ACCOUNT"]')
        account.clear()
        account.send_keys("your account")
        password = driver.find_element('xpath','//*[@id="MASTER_PASSWORD"]')
        password.clear()
        password.send_keys("your password")
        DownLoadVerifyCode()
        verify = driver.find_element('xpath','//*[@id="MASTER_CHK"]')
        verify.clear()
        verify.send_keys(DecodeVerifyCode())
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="popupuser"]/div/div[2]/div[3]/button[3]'))).click()
    except:
        print('Login Fail\n\n\n\n\n\n')
        sleep(5)
        return 1
    finally:
        print('Login Pass')
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
    """, driver.find_element('xpath','//*[@id="master_chk_pic"]'))
    with open("captcha_login.png", 'wb') as image:
        image.write(base64.b64decode(img_base64))

while Login() :
    print('again')
while BuyTicket() :
    input("Press Enter to continue.")
#driver.quit()