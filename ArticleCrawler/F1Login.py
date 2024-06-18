import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exception
import requests as re
import undetected_chromedriver as uc

class F1Selenium:
    def __init__(self, driver):
        # options
        #options = webdriver.ChromeOptions()
        #driver = uc.Chrome(headless=False, use_subprocess=False)
        #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
        #options.add_argument('user-agent={0}'.format(user_agent))
        #options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('log-level=3')
        #options.add_experimental_option("detach", True)
        #options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #driver = webdriver.Chrome(options=options)
        self.driver = driver

    def login(self, id, password):
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

        print("HERE")
        #WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, '[placeholder="Enter your username"]')).send_keys(id)
        #WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, '[placeholder="Enter your password"]')).send_keys(password)
        #time.sleep(5)
        #WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, '[data-i18n="login.login"]')).click()


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


# generator = F1OfficalTokenGenerator()
#
# with open('../account_info.json', 'r') as file:
#     account_info = json.load(file)["f1_account"]
#


from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)  # headless=True로 설정하면 브라우저 창이 뜨지 않습니다.
    context = browser.new_context()

    # 로그인 페이지로 이동
    page = context.new_page()
    page.goto("https://account.formula1.com/#/en/login?https://account.formula1.com/#/en/login?redirect=http%3A%2F%2Fwww.formula1.com%2Fen%2Flatest%2Fall&lead_source=web_f1core")
    time.sleep(330)

    # 로그인 수행
    # page.fill('input[name="username"]', 'your_username')
    # page.fill('input[name="password"]', 'your_password')
    # page.click('button[type="submit"]')

    # 로그인 후 쿠키 추출
    context.storage_state(path="state.json")

with sync_playwright() as playwright:
    run(playwright)


