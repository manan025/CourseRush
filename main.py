import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import mail

load_dotenv()

x = input("Enable headless mode [Y/n]: ").lower()

delay = 3

exe_delay = int(os.getenv("DELAY")) if os.getenv("DELAY") is not None else 5

## credentials
userid = os.getenv("SNUID")
password = os.getenv("SNUPWD")

prev_available_mail = ""

profile_dir = os.path.join(os.getcwd(), "browser_profile")
os.makedirs(profile_dir, exist_ok=True)

while True:
    driver = None
    try:
        if os.getenv("BROWSER") in ["firefox", "zen", "gecko"]:
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
            firefox_options = FirefoxOptions()
            if x != "n" and x != 'no':
                firefox_options.add_argument("--headless")
            if os.getenv("FIREFOX_BINARY"):
                firefox_options.binary_location = os.getenv("FIREFOX_BINARY")
            firefox_profile_path = os.path.join(profile_dir, "firefox_profile")
            os.makedirs(firefox_profile_path, exist_ok=True)
            firefox_profile = FirefoxProfile(firefox_profile_path)
            firefox_options.profile = firefox_profile
            service = FirefoxService() if not os.getenv("GECKODRIVER_PATH") else FirefoxService(executable_path=os.getenv("GECKODRIVER_PATH"))
            driver = webdriver.Firefox(service=service, options=firefox_options)
        else:
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            if x != "n" and x != 'no':
                chrome_options.add_argument("--headless=new")
            chrome_profile_path = os.path.join(profile_dir, "chrome_profile")
            chrome_options.add_argument(f"--user-data-dir={chrome_profile_path}")
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
        classes_not = [i for i in range(2036, 2054)] + [i for i in range(2114, 2121)] + [1947, 2109, 2110] # SWC courses for spring 26
        # auto_swap = []
        enrolled = False

        xpath_total = '/html/body/form/div[4]/table/tbody/tr/td/div/table/tbody/tr[9]/td[2]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]/div/table/tbody/tr[1]/td'
        total = int(driver.find_element(By.XPATH, xpath_total).text.strip().split()[0])

        available = []
        for i in range(total):
            class_nbr = int(driver.find_element(By.XPATH, f'//*[@id="MTG_CLASS_NBR${i}"]').text.strip())
            class_row = driver.find_element(By.XPATH, f'//*[@id="MTG_CLASS_NBR${i}"]/ancestor::table[contains(@id, "SSR_CLSRCH_MTG")]')
            course_group = class_row.find_element(By.XPATH, './ancestor::div[contains(@id, "win1divSSR_CLSRSLT_WRK_GROUPBOX2$")]')
            course_name = course_group.find_element(By.XPATH, './/td[contains(@class, "PAGROUPBOXLABELLEVEL1")]').text.strip()
            available.append((class_nbr, course_name))


        available_mail = f""
        for i, j in available:
            if i not in classes_not:
                available_mail += f"{i} {j}\n"

        available_log = available_mail
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

        driver.quit()


        print(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}:", [i[0] for i in available])
        if available_mail != "":
            print(f"AVAILABLE: {available_log}")
        time.sleep(exe_delay)
    except Exception as e:
        print(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec} Error Occurred:", e)
        if driver is not None:
            try:
                driver.quit()
            except:
                pass

# try:
#     i = 0
#     while True:
#         curr = driver.find_element(By.XPATH, f"//tr[@id='trSSR_CLSRCH_MTG1{i}_row1']//td[1]")
#         i += 1
# except Exception as e:
#     pass
