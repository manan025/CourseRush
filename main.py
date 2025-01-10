import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import mail

load_dotenv()

driver = webdriver.Chrome()

landing = r"https://prodweb.snu.in/psp/CSPROD/EMPLOYEE/HRMS/?cmd=login"
# landing = 'https://whatismybrowser.com/'
driver.get(landing)
# allow cookies

delay = 3

## credentials
userid = os.getenv("SNUID")
password = os.getenv("SNUPWD")

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
        if c in auto_swap:
            # auto swap functionality
            pass

    except Exception as e:
        pass


print(available)

# try:
#     i = 0
#     while True:
#         curr = driver.find_element(By.XPATH, f"//tr[@id='trSSR_CLSRCH_MTG1{i}_row1']//td[1]")
#         i += 1
# except Exception as e:
#     pass


while True:
    pass
