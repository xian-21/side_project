from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager


def login(acc,pd):
    try:
        driver.get('https://www.instagram.com/?hl=zh-tw')
        print('進入哀居')
        time.sleep(5)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
        '//button[@class="sqdOP yWX7d    y3zKF     "][text()="登入"]'))).click()
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
        '//input[@class="_2hvTZ pexuQ zyHYP"]')))
        account=driver.find_elements_by_xpath('//input[@class="_2hvTZ pexuQ zyHYP"]')[0]
        print('準備打帳號')
        account.click()
        account.send_keys(acc)
        time.sleep(3)
        print('輸入')
        password=driver.find_elements_by_xpath('//input[@class="_2hvTZ pexuQ zyHYP"]')[0]
        password.click()
        password.send_keys(pd)
        time.sleep(3)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
        '//*[@id="loginForm"]/div[1]/div[6]/button'))).click()
        time.sleep(3)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
        '//*[@id="react-root"]/section/main/div/div/div/button'))).click()
        print(acc,'登入成功')
        print('點擊關閉')
    except:
        print('失敗')
        driver.quit()
        login_error=1

                
    try:
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
        '/html/body/div[5]/div/div/div/div[3]/button[2]'))).click()
        print('再關閉')
    except:
        print('進入貼文')

def comment(人數,內容,次數,累加,target_url):#半小時留言30則+看限時
    driver.get(target_url)
    time.sleep(5)
    #點留言按鈕
    for 留言次數 in range(次數):
        print(datetime.now())
        type_second=[0.4,0.2,0.3,0.5]
        second=[45,39,48,45,36,50,56,100]
        second=random.choice(second)
        #等到留言框可以按下時 按留言框
        print('按留言框')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        '//textarea[@class="PUqUI Ypffh"]'))).click()
        #等到留言框出現  就輸入留言
        print('打名字')
        comment_go = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/section/div/form/textarea')[0]
        print('打名字')
        if 人數==1:
            comment_go.send_keys('@')
            a=list(name[留言次數+累加*次數].rstrip(','))
            for i in a:
                comment_go.send_keys(i)
                time.sleep(random.choice(type_second))
            comment_go.send_keys(' ')
        if 人數==2:
            comment_go.send_keys('@')
            a=list(name[留言次數*2+2*累加*次數].rstrip(','))
            for i in a:
                comment_go.send_keys(i)
                time.sleep(random.choice(type_second))
            comment_go.send_keys(' ')
            comment_go.send_keys('@')
            a=list(name[留言次數*2+2*累加*次數+1].rstrip(','))
            for i in a:
                comment_go.send_keys(i)
                time.sleep(random.choice(type_second))
            comment_go.send_keys(' ')
        if 人數==3:
            comment_go.send_keys('@')
            a=list(name[留言次數*3+3*累加*次數].rstrip(','))
            for i in a:
                comment_go.send_keys(i)         
                time.sleep(random.choice(type_second))
            comment_go.send_keys(' ')
            comment_go.send_keys('@')
            a=list(name[留言次數*3+3*累加*次數+1].rstrip(','))
            for i in a:
                comment_go.send_keys(i)         
                time.sleep(random.choice(type_second))
            comment_go.send_keys(' ')
            comment_go.send_keys('@')
            a=list(name[留言次數*3+3*累加*次數+2].rstrip(','))
            for i in a:
                comment_go.send_keys(i)         
                time.sleep(random.choice(type_second))
            comment_go.send_keys(' ')

        time.sleep(second)
        print('打內容')
        for i in 內容:
            comment_go.send_keys(i)         
            time.sleep(0.4)
        print('打完內容')

        留言框內容=driver.find_element_by_class_name('Ypffh').text
        print(留言框內容)
        print('留言框總字數',len(留言框內容))
        if len(留言框內容)>21*人數+len(內容): #名字最長20個字+1個空格
            error.append(acc+'留言出錯')
            acc2str=str(acc)
            跑數2str=str(跑數)
            driver.save_screenshot('出錯/'+acc2str+'第'+跑數2str+'次偵測不到禁言.png')
            driver.quit()
            print('留言被禁(偵測不到禁言)')
            break
                
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="react-root"]/section/main/section/div/form/button'))).click()
        print('送出留言')
        try:
            try:
                WebDriverWait(driver,4).until(EC.element_to_be_clickable((By.XPATH,
                '/html/body/div[3]/div/div/div/p'))).click()
            except:
                WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,
                '/html/body/div[2]/div/div/div/p'))).click()
            
            error.append(acc+'留言出錯')
            driver.quit()
            print('留言被禁')
            break
        except:
            print('成功留言!')
        time.sleep(4)
        print(留言次數+1)

def logout():
    driver.get('https://www.instagram.com/'+acc+'/')
    time.sleep(5)
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
    '//button[@class="_2I5My"]'))).click()
    time.sleep(5)
    print('進入設定')
    element=driver.find_element_by_xpath('//div[@class="y2E5d Yod9g"]')
    driver.execute_script("arguments[0].scrollIntoView();",element)
    print('往下')
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
    '//div[@class="y2E5d Yod9g"]/div'))).click()
    time.sleep(5)
    print('點登出')
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,
    '//button[@class="aOOlW  bIiDR  "]'))).click()
    print('成功登出')

login_error=1
error=['出錯']
account={'lin__19_98__':'hk23136415',
}
for 跑數 in range(1):
    for acc in account:
        try:
            if login_error==1:
                options = webdriver.ChromeOptions()
                options.add_argument('blink-settings=imagesEnabled=false')
                # options.add_argument('--headless')
                mobile_emulation = {"deviceName": "iPhone 6"}
                options.add_experimental_option("mobileEmulation", mobile_emulation)
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                login_error=0
            #匯入粉絲名字
            with open('fans_name.txt','r') as f:
                name=[]
                for x in f:
                    x=x.rstrip('\n').rstrip(',')
                    name.append(x)
            login(acc,account[acc])
            comment(2,'cute!',1,跑數,'https://www.instagram.com/p/CabSxtTpRcD/comments/')
            logout()
        except:
            print('出錯')
            login_error=1
            driver.quit()
            error.append(acc)
            print(error)