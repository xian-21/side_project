from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
from bs4 import BeautifulSoup
import os
from win32com import client as wc
import time
import subprocess

new_src = input('輸入wordpress 網址')  #圖片外部連結需要用到
folder_path = r"C:\Users\User\OneDrive\桌面\python\gpt生成文章\發布文章\docx轉html"

class html_upload2blog():
    def __init__(self, folder_path, new_src):
        self.folder_path = folder_path
        self.new_src = new_src
    def html2blog(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.pixnet.net/")
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//div[@class="login"]'))).click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signin__form--post"]/div[1]/input'))).send_keys('a8979401551+404@gmail.com')
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signin__form--post"]/div[2]/input'))).send_keys('zkc14658485')
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signin__form--post"]/button'))).click()
        driver.get('https://panel.pixnet.cc/#/create-article')
        file_paths = [folder_path + '\\' + f for f in os.listdir(folder_path) if f.endswith('.html')]
        for file_path in file_paths:
            print(file_path)
            with open(file_path, "r") as file:
                html_content = file.read()
            print('取得原始碼')
            new_html = BeautifulSoup(html_content, 'lxml')
            #取得body內的所有原始碼
            new_html = new_html.body
            images = new_html.find_all('img')
            for img in images:
                img_name = img['src'].split('/')[-1]
                img_name = img_name.split('.')[0] + '.' + img_name.split('.')[1]
                img['src'] = self.new_src + img_name
            print('成功將html所有img src換成圖片外部url')
            new_html_list = str(new_html).split('\n')
            # 把帶有 '這是分頁符號' 的html原始碼取代成純文字  '這是分頁符號'
            for i in range(len(new_html_list) ): 
                if '這是分頁符號' in  new_html_list[i]:
                    new_html_list[i] = '這是分頁符號'
            #以 '這是分頁符號' 分開每一篇文章
            new_html_list = '\n'.join(new_html_list).split('這是分頁符號')
            #將每一篇文章依序貼到匹客幫
            for article_num in range(len(new_html_list)):
                #從所有文章的list裡面 在轉回beautifulsoup解析 取得第一個<p><\p> 就會是標題了
                title = BeautifulSoup(new_html_list[article_num], 'html.parser').find('p').get_text()
                WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="editArticle-header-title"]'))).send_keys(title)
                WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cke_38_label"]'))).click()
                time.sleep(2)
                # new_html_list[article_num] 代表準備要貼到部落格的文章原始碼
                pyperclip.copy(new_html_list[article_num].replace(str(BeautifulSoup(new_html_list[article_num], 'html.parser').find('p') ), '' ) )
                WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cke_1_contents"]/textarea'))).click()
                
                action = ActionChains(driver)
                action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cke_1_contents"]/textarea'))).click()
                WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, "//button[text()='發表公開文章']"))).click()
                input('發表文章成功')


html_upload2blog = html_upload2blog(folder_path, new_src)
html_upload2blog.html2blog()


