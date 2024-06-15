import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exception
import requests as re


class F1Selenium:
    def __init__(self):
        # options
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('log-level=3')
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver = driver

    def login(self, id, password):
        try:
            self.driver.get('https://account.formula1.com/#/en/login?redirect=http%3A%2F%2Fwww.formula1.com%2Fen%2Flatest%2Fall&lead_source=web_f1core')
            self.driver.implicitly_wait(30)
            original_window = self.driver.current_window_handle
            #
            # WebDriverWait(self.driver, 30).until(
            #     lambda d: d.execute_script('return document.readyState') == 'complete'
            # )
            # print("id : ", id, "password : ", password, " login processing")
            #
            # iframe = WebDriverWait(self.driver, 30).until(
            #     EC.presence_of_element_located((By.XPATH, '// *[ @ id = "sp_message_iframe_1148819"]'))  # iframe의 XPATH를 지정해야 합니다.
            # )
            # self.driver.switch_to.frame(iframe)
            # cookie_popup = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="REJECT ALL"]'))
            # )
            # cookie_popup.click()

            time.sleep(5)
            #WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, '[placeholder="Enter your username"]')).send_keys(id)
            #WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, '[placeholder="Enter your password"]')).send_keys(password)
            #time.sleep(5)
            #WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, '[data-i18n="login.login"]')).click()

        except Exception as e:
            print(e)


class F1OfficalTokenGenerator:
    def __init__(self):
        self.selenium = F1Selenium()
        self.cookie_list = ['csrftoken','g_state','cm_sub','ar_debug','_routing_id','sessionFunnelEventLogged','l_o','_auth','_pinterest_sess','__Secure-s_a']

    def generate_token(self,id,password):
        self.selenium.login(id,password)
        cookies = self.selenium.driver.get_cookies()
        print(cookies)
        result_cookies = ""
        for cookie in cookies:
            print(cookie['name'])
            if cookie['name'] in self.cookie_list:
                result_cookies += cookie['name'] + "=" + cookie['value'] + '; '
        print(result_cookies)


generator = F1OfficalTokenGenerator()

with open('../account_info.json', 'r') as file:
    account_info = json.load(file)["f1_account"]

generator.generate_token(account_info['id'],account_info['password'])
