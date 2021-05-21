from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Variables data
driver = webdriver.Chrome()
act = ActionChains(driver)
url = "https://esp.cisco.com/"
term = "Business Applications"
usr_id = "soubhand@cisco.com"
pasword = "Personalac@07"
app = "Certification Lablets"


def open_the_website(url: str):
    driver.get(url)
    driver.maximize_window()


def login(usr_id: str, password: str):
    driver.find_element_by_id("userInput").send_keys(usr_id)
    driver.find_element_by_id("passwordInput").send_keys(password)
    act.send_keys(Keys.ENTER).perform()


def mfa_auth():
    btn = '//*[@id="auth_methods"]/fieldset/div[1]/button'
    success = 'xpath://*[@id="messages-view"]/div/div/div/span'    
    driver.find_element_by_xpath(btn).click()


def search_for(term: str):
    driver.find_element_by_id("filter").send_keys(term)
    input_class = '//*[@id="7f772e65dbb212002e1a7a1ebf96195f"]/div/div' #//*[@id="7f772e65dbb212002e1a7a1ebf96195f"]/div
    #input_class = "data-id:7f772e65dbb212002e1a7a1ebf96195f"
    time.sleep(5)
    #browser.wait_until_page_contains_element(input_class, timeout = 10)
    driver.find_element_by_xpath(input_class).click()


def search_app(application: str):
    time.sleep(5)
    #driver.find_element_by_css_selector('#cmdb_ci_business_app_table_header_search_control').send_keys(application)
    driver.switch_to_frame('gsft_main')
    driver.find_element_by_xpath("//input[contains(@id, '_text')]").send_keys(application)
    #browser.wait_until_page_contains_element(search_input, timeout=20)
    act.send_keys(Keys.ENTER).perform()
    #return lists
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/span/div/div[6]/table/tbody/tr/td/div/table/tbody/tr[1]/td[3]/a').click()


def fetch_data():
	driver.find_element_by_xpath('//*[@id="sys_readonly.cmdb_ci_business_app.operational_status"]')

def main():
    try:
        open_the_website(url)
        time.sleep(10)
        login(usr_id, pasword)
        time.sleep(6)
        mfa_auth()
        time.sleep(15)
        search_for(term)
        time.sleep(10)
        search_app(app)
    except Exception as e:
        print(e)
    finally:
    	time.sleep(4)
    	driver.close()

if __name__ == "__main__":
    main()
