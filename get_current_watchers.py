from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
options = webdriver.ChromeOptions()
# options.add_extension("./Phantom.crx")
# options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
options.add_argument("window-size=1400,600")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--test-third-party-cookie-phaseout")
    # Use ChromeDriverManager to automatically manage the ChromeDriver version
s = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

def get_current_watchers(token_address):

    window_name = driver.window_handles[0]
    driver.switch_to.window(window_name=window_name)
    url="https://birdeye.so/token/{0}".format(token_address)  
    driver.get(url)
    time.sleep(2)
    wait = WebDriverWait(driver, timeout=20)
    wait.until(lambda driver: driver.find_element(By.XPATH, '//div[text()="Watchers"]').is_displayed())
    watchers = driver.find_element(By.XPATH, '//div[text()="Watchers"]')
    next_element_watchers_count = watchers.find_element(By.XPATH, "following-sibling::*[1]").text

    views_24h = driver.find_elements(By.XPATH, '//div[text()="24h"]')[1]
    next_element_views_24h = views_24h.find_element(By.XPATH, "following-sibling::*[1]").text.split('\n')
    next_element_views_24h_count = next_element_views_24h[0]
    next_element_views_24h_perc=next_element_views_24h[1].replace('%','')

    current_time=datetime.now()
    # print(current_time)
    # print(next_element_watchers_count)
    driver.execute_script("window.open('');")
    driver.close()
    if int(next_element_watchers_count) > 0:
        return [int(next_element_watchers_count),current_time,int(next_element_views_24h_count),float(next_element_views_24h_perc)]
    else:
        return False
    

    



