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
if x != "n" and x != 'no':
    chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)

landing = r"https://prodweb.snu.in/psp/CSPROD/EMPLOYEE/HRMS/?cmd=login"
driver.get(landing)

delay = 3

exe_delay = 1000 * 60 * float(os.getenv("DELAY")) if os.getenv("DELAY") is not None else 5

## credentials
userid = os.getenv("SNUID")
password = os.getenv("SNUPWD")

while True:
    time.sleep(delay)

    # Login
    driver.find_element(By.ID, "userid").send_keys(userid)
    driver.find_element(By.ID, "pwd").send_keys(password)
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

    classes = {'1685': "", '1679': "", '1682':""}
    auto_swap = []
    available = []
    enrolled = False

    for c in classes.keys():
        try:
            x = driver.find_element(By.LINK_TEXT, c)
            available.append(c)
            mail.send(c, classes[c])

        except Exception as e:
            pass


    print(available)
    time.sleep(exe_delay)

# try:
#     i = 0
#     while True:
#         curr = driver.find_element(By.XPATH, f"//tr[@id='trSSR_CLSRCH_MTG1{i}_row1']//td[1]")
#         i += 1
# except Exception as e:
#     pass


