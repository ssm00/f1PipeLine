import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exception
import CustomException

class Selenium:
    def __init__(self):
        # options
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('log-level=3')
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--test-third-party-cookie-phaseout")
        driver = webdriver.Chrome(options=options)
        self.driver = driver

    def login(self, id, password):
        try:
            self.driver.get('https://www.pinterest.co.kr/')
            self.driver.implicitly_wait(30)
            original_window = self.driver.current_window_handle
            print("id : ", id, "password : ", password, " login processing")
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CLASS_NAME, 'tBJ.dyH.iFc.sAJ.B1n.tg7.H2s')).click()
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CLASS_NAME, 'nsm7Bb-HzV7m-LgbsSe-BPrWId')).click()
            #창 전환
            for window_handle in self.driver.window_handles:
                if window_handle != original_window:
                    self.driver.switch_to.window(window_handle)
                    break
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.CLASS_NAME, 'whsOnd.zHQkBf')).send_keys(id)
            WebDriverWait(self.driver, 3).until(lambda x: x.find_elements(By.CLASS_NAME, 'VfPpkd-vQzf8d')[1]).click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="비밀번호 입력"]')))
            time.sleep(1)
            WebDriverWait(self.driver, 5).until(lambda x: x.find_element(By.CLASS_NAME, 'whsOnd.zHQkBf')).send_keys(password)
            WebDriverWait(self.driver, 5).until(lambda x: x.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.BqKGqe.Jskylb.TrZEUc.lw1w4b')).click()
            print("login DONE!")
            #구글 로그인 창으로 바꿔뒀던 창 선택 다시 바꿔야 쿠키 가져올 수 있음
            self.driver.switch_to.window(original_window)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="검색 아이콘"]')))
        except selenium_exception.NoSuchWindowException as e:
            raise CustomException.TooMuchLogin()
        except Exception as e:
            print(e)


class TokenGenerator:
    def __init__(self, selenium):
        self.selenium = selenium
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

