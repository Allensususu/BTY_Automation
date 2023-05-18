from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as Soup
import os
import re
from datetime import datetime
from module import function

def login(account,password,browser):
    url = 'https://www.bsportstest.com/'  
    browser.get(url)
    #點擊右上角登入
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,'login')))
    browser.find_element(By.CLASS_NAME,'login').click()
    time.sleep(0.5)

    #點選帳號密碼登入
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"tab-item")))
    browser.find_elements(By.CLASS_NAME,"tab-item")[1].click()
    time.sleep(0.5)

    #輸入帳號密碼
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-input__inner')))
    browser.find_elements(By.CLASS_NAME,"el-input__inner")[0].send_keys(account)
    browser.find_elements(By.CLASS_NAME,"el-input__inner")[1].send_keys(password)
    time.sleep(0.5)
    #點擊登入
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"el-button--primary")))
    browser.find_elements(By.CLASS_NAME,"el-button--primary")[0].click()
    time.sleep(0.5)

    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,'bi')))
    currency = browser.find_element(By.CLASS_NAME, 'bi').get_attribute('alt')
    return currency

def language(language_type,currency,browser):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'lang-selected')))
    browser.find_elements(By.CLASS_NAME,"lang-selected")[0].click()
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'lang-list')))
    class_list = browser.find_element(By.CLASS_NAME,"lang-list")
    divs = class_list.find_elements(By.CSS_SELECTOR,"div")
    main = ['CNY','VND','THB','USDT','MYR']
    if currency in main:
        if language_type.lower() == 'chinese':
            divs[0].click()
        elif language_type.lower() == 'english' or language_type == 'eng':
            divs[1].click()
        elif language_type.lower() == 'viet':
            divs[2].click()
        elif language_type.lower() == 'thai':
            divs[3].click()
    elif currency in "BRL":
        if language_type.lower() == 'english' or language_type.lower() == 'eng':
            divs[0].click()
        elif language_type.lower() == 'brasil':
            divs[1].click()
    elif currency in "MXN":
        if language_type.lower() == 'english' or language_type.lower() == 'eng':
            divs[0].click()
        elif language_type.lower() == 'espanol':
            divs[1].click()
    elif currency in "EGP":
        if language_type.lower() == 'english' or language_type.lower() == 'eng':
            divs[0].click()
        elif language_type.lower() == 'arabic':
            divs[1].click()

    

def PG_Automation(now,currency,excel,browser):
    #init
    sheet = function.get_sheet(excel,"PC_PG")
    row = function.checkrow(sheet)
    sheet.range('A'+str(i+3)).value = name[i]
    sheet.range(row+str(1)).value = 'PG_'+currency
    #跳轉PG電子
    browser.get("https://www.bsportstest.com/digital?gameId=38001&channelId=38&gameType=3&platFormId=38003&gameName=PG%E7%94%B5%E5%AD%90")
    

    #計算場館數量
    browser.set_window_size(3000, 3000)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'game-item')))
    game_count = len(browser.find_elements(By.CLASS_NAME,"game-item"))
    game_name = browser.find_elements(By.CSS_SELECTOR,'h3.title')  
    name = [game_name[i].text for i in range(0, game_count)]

    #進入各場館
    for i in range(0,game_count):
        #調整網頁進入遊戲場館
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"game-item")))
        browser.execute_script("arguments[0].click();", browser.find_elements(By.CLASS_NAME,"game-item")[i])
        browser.execute_script("arguments[0].click();", browser.find_elements(By.CLASS_NAME,"play-btn")[i])

        #調整畫面，並選擇遊戲場館頁面
        browser.switch_to.window(browser.window_handles[1])
        browser.set_window_size(1024, 768)

        #寫入場館遊戲名稱
        sheet.range('A'+str(i+3)).value = name[i]
        try:

            try:
                time.sleep(20)
                if browser.find_element(By.ID,'ca-button-0'):
                    browser.find_element(By.ID,'ca-button-0').click()
                    sheet.range('B'+str(2)).value = "have free game"
            except:
                pass
            #等待開始按鈕並點擊
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME,"start-button-inner")))
            browser.find_element(By.CLASS_NAME,"start-button-inner").click()

            #獲得canvas
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"gameCanvas")))
            canvas = browser.find_element(By.CLASS_NAME,"gameCanvas")
            browser.get_screenshot_as_file('.\\output\\'+now+'\\'+ name[i] +".jpg")
            time.sleep(0.5)
            #獲取帳戶餘額
            attempt = 1
            while attempt <= 5:
                try:
                    for y in range(620,400,-20):
                        ActionChains(browser).move_to_element_with_offset(canvas,80,y).click().perform()
                    time.sleep(5)
                    balance = browser.find_elements(By.CLASS_NAME,"sc-breuTD")[1].text
                    balance  = int(''.join(re.findall(r'\d+',balance2)))
                    break
                except :
                    attempt += 1

            ActionChains(browser).move_to_element_with_offset(canvas,100,100).click().perform()
            time.sleep(2)

            #點擊投注按鈕
            for _ in range(0,5):
                ActionChains(browser).move_to_element_with_offset(canvas,180,560).click().perform()
                time.sleep(5)
            time.sleep(5)

            #再次獲取帳戶餘額
            attempt = 1
            balance2 = balance
            while attempt <= 5:
                try:
                    for y in range(620,400,-20):
                        ActionChains(browser).move_to_element_with_offset(canvas,80,y).click().perform()
                    time.sleep(5)
                    balance2 = browser.find_elements(By.CLASS_NAME,"sc-breuTD")[1].text
                    balance2  = int(''.join(re.findall(r'\d+',balance2)))
                    break
                except :
                    attempt += 1

            #關閉遊戲網頁
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(3)
            #寫入資料
            if balance2 != balance :
                sheet.range(row+str(i+3)).value = "PASS"
            else:   
                sheet.range(row+str(i+3)).value = "balance error"

        except :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            sheet.range(row+str(i+3)).value = "error"
