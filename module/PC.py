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
    time.sleep(3)

    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,'bi')))
    currency = browser.find_element(By.CLASS_NAME, 'bi').get_attribute('alt')
    return currency

def language(language_type,currency,browser):
    browser.set_window_size(3000, 3000)
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

    

def PG_Automation(now,currency,language,excel,browser):
    #init
    sheet = function.get_sheet(excel,"PC_PG")
    row = function.checkrow(sheet)
    sheet.range(row+str(1)).value = currency  + "_" + language
    #跳轉PG電子
    browser.get("https://www.bsportstest.com/digital?gameId=38001&channelId=38&gameType=3&platFormId=38003&gameName=PG%E7%94%B5%E5%AD%90")
    

    #計算場館數量
    browser.set_window_size(3000, 3000)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'game-item')))
    game_count = len(browser.find_elements(By.CLASS_NAME,"game-item"))
    game_name = browser.find_elements(By.CSS_SELECTOR,'h3.title')  
    name = [game_name[i].text for i in range(0, game_count)]

    #進入各場館
    for i in range(0,len(game_name)):
        #獲取餘額
        browser.set_window_size(1200, 1000)
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'refresh-icon')))
        browser.execute_script("arguments[0].click();", browser.find_element(By.CLASS_NAME, 'refresh-icon'))
        time.sleep(8)
        balance = browser.find_element(By.CLASS_NAME, 'integer').text + browser.find_element(By.CLASS_NAME, 'dot').text
        balance = int(''.join(re.findall(r'\d+',balance)))


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
                    sheet.range('B'+str(2)).value = browser.find_element(By.CLASS_NAME,'message message_padding ').text
            except:
                pass
            #等待開始按鈕並點擊
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME,"start-button-inner")))
            browser.find_element(By.CLASS_NAME,"start-button-inner").click()

            #獲得canvas
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"gameCanvas")))
            canvas = browser.find_element(By.CLASS_NAME,"gameCanvas")
            if not os.path.exists('.\\output\\'+now+'\\KAG_'+currency +"_" + language ):
                os.mkdir('.\\output\\'+now+'\\KAG_'+currency +"_" + language)
            browser.get_screenshot_as_file('.\\output\\'+now+'\\PC_PG_'+currency +"_" + language +"\\" + name[i] +".png")
            time.sleep(0.5)

            #點擊投注按鈕
            for _ in range(0,3):
                ActionChains(browser).move_to_element_with_offset(canvas,180,560).click().perform()
                time.sleep(5)
            time.sleep(5)


            #關閉遊戲網頁
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(3)

            #獲取餘額
            browser.set_window_size(1200, 1000)
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'refresh-icon')))
            browser.execute_script("arguments[0].click();", browser.find_element(By.CLASS_NAME, 'refresh-icon'))
            time.sleep(8)
            balance2= browser.find_element(By.CLASS_NAME, 'integer').text + browser.find_element(By.CLASS_NAME, 'dot').text
            balance2 = int(''.join(re.findall(r'\d+',balance2)))
            #寫入資料
            if balance2 != balance :
                sheet.range(row+str(i+3)).value = "PASS"
            else:   
                sheet.range(row+str(i+3)).value = "balance error"

        except Exception as e:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            sheet.range(row+str(i+3)).value = "error"


def KAG_Automation(now,currency,language,excel,browser):
    #init
    sheet = function.get_sheet(excel,"PC_KAG")    
    row = function.checkrow(sheet)
    sheet.range(row+str(1)).value = currency + "_" + language
    #跳轉KAG電子
    browser.get("https://www.bsportstest.com/digital?gameId=76001&channelId=76&gameType=3&platFormId=76003&gameName=KA%20%D9%85%D8%A7%D9%83%D9%8A%D9%86%D8%A7%D8%AA%20%D9%82%D9%85%D8%A7%D8%B1")

    #計算場館數量
    browser.set_window_size(3000, 3000)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'game-item')))
    game_count = len(browser.find_elements(By.CLASS_NAME,"game-item"))
    game_name = browser.find_elements(By.CSS_SELECTOR,'h3.title')  
    name = [game_name[i].text for i in range(0, game_count)]

     #進入各場館
    for i in range(0,len(game_name)):
        #獲取餘額
        browser.set_window_size(1200, 1000)
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'refresh-icon')))
        browser.execute_script("arguments[0].click();", browser.find_element(By.CLASS_NAME, 'refresh-icon'))
        time.sleep(8)
        balance = browser.find_element(By.CLASS_NAME, 'integer').text + browser.find_element(By.CLASS_NAME, 'dot').text
        balance = int(''.join(re.findall(r'\d+',balance)))

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
                    sheet.range('B'+str(2)).value = browser.find_element(By.CLASS_NAME,'message_padding').text
            except:
                pass

            #獲得canvas
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"gameCanvas")))
            canvas = browser.find_element(By.CLASS_NAME,"gameCanvas")
            time.sleep(15)
            if not os.path.exists('.\\output\\'+now+'\\KAG_'+currency +"_" + language ):
                os.mkdir('.\\output\\'+now+'\\KAG_'+currency +"_" + language)
            browser.get_screenshot_as_file('.\\output\\'+now+'\\PC_KAG_'+currency +"_" + language +"\\" + name[i] +".png")
            time.sleep(3)

            #點擊最低投注額按鈕
            ActionChains(browser).move_to_element_with_offset(canvas,636,504).click().perform()

            #點擊投注按鈕
            for _ in range(0,10):
                ActionChains(browser).move_to_element_with_offset(canvas,506,580).click().perform()
                time.sleep(5)
            time.sleep(5)

            #關閉遊戲網頁
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(3)

            #獲取投注後餘額
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'refresh-icon')))
            browser.execute_script("arguments[0].click();", browser.find_element(By.CLASS_NAME, 'refresh-icon'))
            time.sleep(8)
            balance2 = browser.find_element(By.CLASS_NAME, 'integer').text + browser.find_element(By.CLASS_NAME, 'dot').text
            balance2 = int(''.join(re.findall(r'\d+',balance2)))

            #寫入資料
            print(balance2)
            print(balance)
            if balance2 != balance :
                sheet.range(row+str(i+3)).value = "PASS"
            else:   
                sheet.range(row+str(i+3)).value = "balance error"

        except Exception as e:
            print(e)
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            sheet.range(row+str(i+3)).value = "error"
