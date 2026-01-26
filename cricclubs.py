from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def extract_innings(innings_num):
    ul_elements = driver.find_elements(By.CSS_SELECTOR, "ul[id^='ballid_']")
    r_dict={"1":"Normal","2":"Normal","3":"Normal","4":"Boundary","6":"Boundary","0":"Dot","W":"Wicket","E":"Extra"}
    over_dict = {}
    for ul in ul_elements:
        try:
            over_value = ul.find_element(By.CSS_SELECTOR, "li.col2 span.ov").text.strip()
        except:
            over_value = None

        try:
            col3_text = ul.find_element(By.CSS_SELECTOR, "li.col3").text.strip()
        except:
            col3_text = None

        if over_value:
            over_dict[over_value] = col3_text

    #print(f"{'Over':<8} | Commentary | Innings {innings_num}")
    #print("-" * 80)
    #for over, commentary in over_dict.items():
        #print(f"{over:<8} | {commentary} | {innings_num}")
    print ("Bowler | Batter | Run | Direction | Event")
    for j in over_dict.items():
        comm  = j[1]
        if any(x in comm.upper() for x in ["WIDE","BYE","LEG BYE","NO BALL"]):
            if "\n" in comm:
                comm=comm.split("\n")[0]
            print("Extra")
            bowler = comm.split(" to ")[0]
            batter = comm.split(" to ")[1].replace("WIDE","").replace("BYE","").replace("LEG BYE","").replace("NO BALL","").strip()
            run = "E"
            dir = r_dict[run]
        else:
            if "\n" in comm:
                comm=comm.split("\n")[0]
            dia = comm.split(",",1)
            first = dia[0].split(" to ")
            bowler=first[0]
            if "OUT" not in comm:
                batter=first[1]
                #print(bowler," ",batter)
                #print(dia[1])
                run = re.search(r"\d+",dia[1]).group()
                run=run.strip()
                #print(run.group(), " ",dict[run.group()])
                dir=dia[1].split(',')[-1]
                dir = dir.replace('towards','').replace('FOUR','').replace('SIX','').strip()
                #print(dir)
            else:
                batter = first[1].replace("OUT!","").replace("BOWLED","").replace("LBW","").replace("RUN OUT","").replace("STUMPED","").replace("CAUGHT","").strip()
                run="W"
                dir="Wkt"
        print(bowler," | ",batter," | ",run," | ",dir," | ",r_dict[run])
        '''if "OUT" in delivery:
            print("Out")
        else:
            str=delivery.split(" , ",1)
            player = str[0].split(" to ")
            bowler = player[0]
            batter = player[1]
            run = re.search("\d+",str[1])
            event = dict(re)
            if run == "4" or run =="6":
                direction = str[1].split("FOUR|SIX")
                dir = direction[0]
            else:
                direction=str[1].split(" , ")
                dir = direction[1]
            print(bowler," ",batter," ",run, " ", event," ",dir) '''
            
    



# --- Config ---
url = 'https://cricclubs.com/InternationalScores/ballbyball.do?matchId=7549&clubId=11707'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

time.sleep(3)
innings = driver.find_elements(By.XPATH, '//li[contains(@id,"ballByBallTeamTab")]')

for idx, tab in enumerate(innings, start=1):
    driver.execute_script("arguments[0].click();", tab)
    time.sleep(2)
    extract_innings(idx)
    print("--------------")

driver.quit()

