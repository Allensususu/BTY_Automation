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
now="test"
os.makedirs(".\\output\\" + now, exist_ok=True)
excel = function.create_excel(now)
#添加緩存
os.makedirs('cache', exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument('--disk-cache-dir='+ os.path.join(os.getcwd(), 'cache') )
options.add_argument('--mute-audio')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
currency="EGP"
language = "ENG"

if __name__ == '__main__' :
        H5.login("coreyegp2","1qaz2wsx",browser)
        H5.language("ENG",currency,browser)
        H5.PG_Automation(now,currency,"ENG",excel,browser)

        #PC.login("coreyegp1","1qaz2wsx",browser)
        #PC.language("eng",currency,browser)
        #PC.KAG_Automation(now,currency,"eng",excel,browser)
