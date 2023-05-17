from ctypes.wintypes import WORD
from email import message
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as Soup
import os
from module import PC,function
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


#init
now = str(datetime.now().strftime("%m%d_%H_%M")) 
if not os.path.exists(".\\output\\" + now):
        os.mkdir(".\\output\\" + now)
url = 'https://www.bsportstest.com/'  

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)


if __name__ == '__main__' :
        currency = PC.login("coreyegp1","1qaz2wsx",browser)
        PC.PG_Automation(now,currency,browser)


