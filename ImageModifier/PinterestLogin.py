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


se = Selenium()
generator = TokenGenerator(se)
generator.generate_token("titan0724ex2","qwe100312@")
cookies = """
csrftoken=36965480027b268da1264bbd2aeb63b0; g_state={"i_l":0}; cm_sub=none; ar_debug=1; _routing_id="7d5cf6ad-02eb-46dd-97a3-8786200a7b3e"; sessionFunnelEventLogged=1; l_o=RlBVRVd0cHI0WUdvOTNtZklLRUxINnVSbVBOZDFzcFBlaGw4M1REampkUEV1TlBWb2NlWWtJQ1VLSjI1bnpKT2JReGU5Q2taTHY4OUwvVkkzeUkyMEJOVHpkYnVXaVBoVEZWUGZZWWFRc289JnJBUmZ6Mi9OSXU1VG80KzJMbExYc1lvUitGcz0=; _auth=1; _pinterest_sess=TWc9PSY4eWttUmVERGtIK09GNXB1TUZGcWhmZ2NyMnh3WitKclAvZHNCNFVLWk9JVzJZSVNvZWtkNXJLeEh6VXVncWtFTGNZVzgxTS9Cc0dYTkd5Z200V3hpMlQrdlU3dDR4K2hQZmFraEIzRkFwcnkyZ0VRa3MxWlhQVzlaS01UWTczS2YzWmNjczFNeWRxY3Z4aHZZNC9yV2pWaCtONnFmbHVyRjNjVlNoTDNHTjhuNEZVRSt0N2pZZzA5azkvdjI5UUpXaXdOTmMzaUhhR1ZWZU02a1k5TVV5aDlRNE55VFNXM2JWNVhGdE9IaUNJYWxmRUNXTFNSbVBiZWxKVFdYa29vT0JMUjVDTlVhTzFzNHp1cVlhcS9QUnArdGlJMTB0ZHNSVlMvYXhFZFZ6aC9jVUlLMG00emhSOWEza0xsZTdrd2RiMWZjV1RDNnJCeEJNQzRHb3ZFWnllb3ZoT1Z4SWFPV2cySkhhTGJIVmVQSTdlb3UyTHZUZ2Fxb0ZhTDJVY28xeE54YTlSdTlSVzFFUzdZOUJTMnJBdlBIYjNIK3RLMUVMNmxQU0lrUG81d2ZkU3o4ZXRrcFNleGZkUWRYZEUwa3kzUW1oWjdtVExHRGxOeDNiVzBPZGRFUVpmbGQ3eVFiNyt1Z0xuWDdKcDdhVWtwaThRT2hlczNlQUJaTDdOT3JmSnJwS1NCWWtjaHZoaW9rc2JNTUFvRFZiZndqL1hJQzRSSEpVRElzQ3o1TjJHbVhmTXZvV2NLaFV3bjkybDFlVTNvd0tRZ1c0U1hpQ1ZNYmNQY09aaDMvQ0pLaFVKenZCd2Q2Ujg3VGVTVUNYT3FNNjBSSUZoeE5tSzdmMmZhcU9NUVY5cS9uT1VraFNOQUZGY1Y4WFZKbFJIMlJUdnIrb0JjSkYrc2RvMmY1ZW8xZXlHeXcrWHlsZGhPTE1IRm1PQWpXS1V1WW55NTlWM09yZG5nU2F3T0VqRWx5Yzg3dDYyZVJqS0FDUDJXRXkvRzRBdFpEQ3UvTHlxYnVNb0NtZ2lBOEZvZ2xsUlFBbUtFTFoycGxyNUVSTWd3V1lnb1VuZnV5MTA1WnlvY0tBcFpuaDJjcFEzdWNGVVFqdG5CcHVtK093MnNHclNPeFptL2FLdUxKN010dG95UGt0azdjRk1yNGhwSVUzTzdtYzJ6N0I2Ukl1ZFZGSi8vdFM3Z2xmS1lKRGpVMHBQRjZjSXlRb0hJNXZqU21RSkU3cmRUQmlSZk14NnJJalEvR0pBSTZ2Ni9KaFZ2NW1GcnZFc0RpczNmM3VoVjZwcFJraU5HcktsRVQ4NDI4UTFMc0dybEhGUVN3bmNKeGY5eUZweUhkdS9LSG0wUW9Ja2pzenJ3by8xUG9pajdrVFVxZDVyaWlVa1dWczdGWXVyV1l6blNHN2dpWkZ6U0RoUkRUcjlmU0x4L3NxTFEzeFA4c0FBWW1yT3I1NERUUDhRaXhDeUNkZStFZ1Q2bFgxd1RrRlBrR1FTaFhxQ2c5c2hCRHdweWIwQStZYzNQNnhtbmtkLy9Ta1o2OFBJbHQrZXBBRzlsazIrcDUrUnVnR0lJUS92WTVDV1BHRlZEeUpsVUhtdUs3ZDJkcTFmaUkwWTFXVE0xSnRscExGYnYwMVVrTGNTVWpPdWVZSE1iQ0xCd1lKQWJWak5XdVVKYStIeXdsZEZjQkpJSlFQS0h2RVBKdGJ2V2xIQVRVbnpmSXFPLzREUlJGMHdiNnZzdkNQZTYvcEJZQkpLNmpYWGhiSUsvS0hHUzNLK2d4ZDdpVG5uc0xMbW4mSyt4T202WFFESDVjeXRNMlliSVJpN3RwZ2JRPQ==; __Secure-s_a=emQ4aERoMm1uams5MnBIY25aVGFJZU1EdThXSFB1UUlxQXlVdFBuNWlkbkFmMzl1OW1aRUFsb0VwelJjUzlMajM4NTNTcWRGSDlzbW9peGFUNllWZHQxK1FwdStyekRUTjJyOWtiUVFhUm42alp3VUpvOXppQW5XdWNHMFJXR3BmQm5KWTQveThLbmZqTkhJN3YwdHlPbkxqYkQrK0FXajhoSXpGL0ltYklGdkhMUWRNMFdrRjVvdEdoMHF4NUZWbTF4Q2J5T2N2Q3ZWYnZuYlZsNFRkRnRGNHFMM2lrZmlFV2Z1Y0pTWElUcVpzeHdESEU1NUhCbFZPUDVNMGFOaFdoalVKT3dib1A5ZmRHM0kwK0x5RkI0YXZqZlpWTVlKbWZtTWxCRU5KMVFpdi9PdnMwZEdqVjlsNS9aeUtqQnBadVUxcVhFbnVEZVZTdElmUUlVbmxkazV2K1d0VE9tOVlBMi9KbDdsQmovNWRDZWRXbGdpWmxMVlZMMzdKbjd0TW1TV2RzeGRYZUN0ZXluaFhZUGJaVDJMODRIaHdCU2E0azVXZmtacHNKUk1BOTBqZS83OGZEZGNXVTVVK0VlalFlV2E2VTNuNkxSTk84UGFPZnNpQnF2cEJDYm9LdUxMOWR3bXpRYm1kYmh3SERvc2ZvK0l5azVuVDRPdjJ3N3FDMW5oaW83UGp2SW1BSmxJTVlKQ0s1THZOYzlsdHV0aGFlSElFQ2pNVVJSVmpWL1kvMlc3UTh6N3E0eE9WdGw4Um5BVVQ0b0Vha1lwT09yRHFaL1Q2V2tVUkZjUWRYaG1DV1hYaEFad3pPWllvUFczZE93RzB3YmR1QlZFY0xuMnc5Q2kvaWRJQUltSTFzSTk1S1lhK3RQZUJjTC9EeUYrdFlEUWpNNzNqVm1SMm5XYjRaTDc0a3ZIOUdYYS9JR1h2SUtRSngzelF5VnlITVJVMVlIZnpEZ055WWJ4NnRCYXByT01EanA3djVTS1lhN1VEZnJTZkh3QnYwRUxFU2k5d25GaUJ4OUpNclp0Tis4ajYwbEIxWElvV0FuS1NTRHpIa3RIcjYybm5hRDF4emhMTEtXbm00OGVJaFI1ZER1enczQWRpSFRFTWVjWUNWRkw0RUk0SFpiTVAwaFNyeXVTV2lyakl6dm1sMHh6OEdMcjErU1VydTBSUzJVbnZYWVNSdmx4UkpqbmxOUWFRdk1rSW5jbWFlQ1EzVnlvSk9vNkNqaDRtS1h2c1Fuc0FzMHZIUmFEQksrYW1TVEQweldkbzJRaDgyeW00OUpGdjdWRjUvbVFOR2tPM3VPU3h2UmFqMi9KRW5CN0VCaz0mWThna0xDU3cySGZhWDRwQUo0bDEvdlM0M1NjPQ==
"""