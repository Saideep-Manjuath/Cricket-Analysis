import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

url = 'https://www.cricbuzz.com/live-cricket-stream/130069/ind-vs-pak-6th-match-group-a-asia-cup-2025'
path = '/Users/saideepmanjunath/Downloads/chromedriver-mac-arm64/chromedriver'
driver=webdriver.Chrome(service=Service(path))
driver.get(url)
print(driver.title)
print(driver.current_url)
time.sleep(5)
scorecard = driver.find_element(By.XPATH,"//a[contains(@href,'live-cricket-scorecard')]")
scorecard.click()
print(driver.title)
print(driver.current_url)
'''
data=[] 
for i in range(1,3): 
    innings= driver.find_elements(By.CSS_SELECTOR, f'div[id="innings_{i}"] div.cb-col.cb-col-100.cb-scrd-itms') 
    for b in innings: 
        r=[] 
        if b.find_elements(By.CSS_SELECTOR,"div.cb-col.cb-col-25") and b.find_elements(By.CSS_SELECTOR,"div.cb-col.cb-col-33"): 
            col = b.find_elements(By.CSS_SELECTOR,"div.cb-col") 
            for c in col: 
                if c.text!='': 
                    r.append(c.text) 
            r.append(f"innings_{i}") 
            data.append(r)
                     #print(batter) print(data) input("press enter") driver.close()
'''
data=[]
for c in range(1,3):
    innings= driver.find_elements(By.CSS_SELECTOR, f'div[id="innings_{c}"] div.cb-col.cb-col-100.cb-scrd-itms')
    for i in innings:
        rows = i.find_elements(By.CSS_SELECTOR,'div.cb-col')
        tmp=[]
            #cl_str = r.get_attribute("class")
        batter = any("cb-col-25" in r.get_attribute("class") for r in rows)
        wicket = any("cb-col-33" in r.get_attribute("class") for r in rows)
        if batter and wicket :
            for r in rows:
                if r.text!='':
                    tmp.append(r.text)
            if tmp:
                tmp.append(f"innings_{c}")
            data.append(tmp)

#print(batter)
print(data)
input("press enter")
driver.close()
