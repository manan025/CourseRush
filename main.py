import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import mail

load_dotenv()

chrome_options = Options()
x = input("Enable headless mode [Y/n]: ").lower()

delay = 3

exe_delay = int(os.getenv("DELAY")) if os.getenv("DELAY") is not None else 5

## credentials
userid = os.getenv("SNUID")
password = os.getenv("SNUPWD")

prev_available_mail = ""

while True:
    try:
        if x != "n" and x != 'no':
            chrome_options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=chrome_options)

        landing = r"https://prodweb.snu.in/psp/CSPROD/EMPLOYEE/HRMS/?cmd=login"
        driver.get(landing)

        time.sleep(delay)

        # Login
        driver.find_element(By.ID, "userid").send_keys(userid)
        driver.find_element(By.ID, "pwd").send_keys(password)
        time.sleep(delay)
        driver.find_element(By.NAME, "Submit").click()

        time.sleep(delay)

        # Home page
        driver.find_element(By.LINK_TEXT, "Search").click()

        time.sleep(delay)

        # search page

        frame_0 = driver.find_element(By.ID, "ptifrmtgtframe")
        driver.switch_to.frame(frame_0)

        # //div[@id='win1divSSR_CLSRCH_WRK_SUBJECT_SRCH$0']//select[1]
        subject = Select(driver.find_element(By.XPATH, "//div[@id='win1divSSR_CLSRCH_WRK_SUBJECT_SRCH$0']//select[1]"))
        subject.select_by_value("CCC")

        # select subject
        driver.find_element(By.ID, "SSR_CLSRCH_WRK_SUBJECT_SRCH$0").click()



        time.sleep(2)
        driver.find_element(By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()

        time.sleep(delay)

        # search results
        driver.switch_to.default_content()
        frame = driver.find_element(By.ID, "ptifrmtgtframe")
        driver.switch_to.frame(frame)

        # classes = {'1533': "", '1679': "", '1682':""}
        classes_not = ['1533', '1536', '1539', '1541', '1546', '1547', '1548', '1551', '1552', '1553', '1556', '1557', '1558', '1559', '1561', '1562', '1565', '1566', '1569', '1570'] # swayam course
        # auto_swap = []
        enrolled = False

        xpath_total = '/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[9]/td[2]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]/div/table/tbody/tr[1]/td'
        total = int(driver.find_element(By.XPATH, xpath_total).text.strip().split()[0])
        xpath_classes = [f'//*[@id="MTG_CLASS_NBR${i}"]' for i in range(total)]
        xpath_names = [f'//*[@id="win1divSSR_CLSRSLT_WRK_GROUPBOX2GP${i}"]' for i in range(total)]
        available = [(driver.find_element(By.XPATH, i).text.strip(), driver.find_element(By.XPATH, j).text.strip()) for i, j in zip(xpath_classes, xpath_names)]


        available_mail = f""
        for i, j in available:
            if i not in classes_not:
                available_mail += f"{i} {j}\n"

        if available_mail == prev_available_mail:
            available_mail = ""
        if available_mail != "":
            try:
                mail.send(available_mail, "REGISTER NOW.")
                prev_available_mail = available_mail
            except Exception as e:
                print(e)
        else:
            mails_sent = False

        driver.close()


        print(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}:", [i[0] for i in available])
        if available_mail != "":
            print(f"AVAILABLE: {available_mail}")
        time.sleep(exe_delay)
    except Exception as e:
        print(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec} Error Occurred:", e)

# try:
#     i = 0
#     while True:
#         curr = driver.find_element(By.XPATH, f"//tr[@id='trSSR_CLSRCH_MTG1{i}_row1']//td[1]")
#         i += 1
# except Exception as e:
#     pass


