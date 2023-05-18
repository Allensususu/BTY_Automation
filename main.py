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
from module import PC,function,H5
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


#init
now = str(datetime.now().strftime("%m%d_%H_%M")) 
if not os.path.exists(".\\output\\" + now):
        os.mkdir(".\\output\\" + now)
excel = function.create_excel(now)

browser = webdriver.Chrome(ChromeDriverManager().install())

language = "ENG"

if __name__ == '__main__' :
        currency = H5.login("coreyegp1","1qaz2wsx",browser)
        H5.language(language,currency,browser)
        H5.PG_Automation(now,currency,excel,browser)

        currency = PC.login("coreyegp1","1qaz2wsx",browser)
        PC.language(language,currency,browser)
        PC.PG_Automation(now,currency,excel,browser)

