from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import psycopg2


# Variables data
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=options)

act = ActionChains(driver)
url = "https://esp.cisco.com/"
term = "Business Applications"
usr_id = "soubhand@cisco.com"
pasword = "Personalac@07"
#app = "Certification Lablets"


def read_apps():
	file = open("app.txt")
	file_content = file.read()
	contents_list = file_content.splitlines()
	file.close()
	return contents_list

def open_the_website(url: str):
    driver.get(url)
    driver.maximize_window()


def login(usr_id: str, password: str):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "userInput")))
    driver.find_element_by_id("userInput").send_keys(usr_id)
    driver.find_element_by_id("passwordInput").send_keys(password)
    act.send_keys(Keys.ENTER).perform()


def mfa_auth():
    btn = '//*[@id="auth_methods"]/fieldset/div[1]/button'
    success = 'xpath://*[@id="messages-view"]/div/div/div/span' 
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="auth_methods"]/fieldset/div[1]/button')))   
    driver.find_element_by_xpath(btn).click()


def search_for(term: str):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "filter")))
    driver.find_element_by_id("filter").send_keys(term)
    input_class = '//*[@id="7f772e65dbb212002e1a7a1ebf96195f"]/div/div' #//*[@id="7f772e65dbb212002e1a7a1ebf96195f"]/div
    #input_class = "data-id:7f772e65dbb212002e1a7a1ebf96195f"
    time.sleep(5)
    #browser.wait_until_page_contains_element(input_class, timeout = 10)
    driver.find_element_by_xpath(input_class).click()


def search_app(application: str):
    #driver.find_element_by_xpath("//input[contains(@id, '_text')]").send_keys(application)
	refresh()
	try:
		driver.find_element_by_id("cmdb_ci_business_app_table_header_search_control").send_keys(application)
		act.send_keys(Keys.ENTER).perform()
		refresh()
		time.sleep(5)
    #driver.find_element_by_xpath('/html/body/div[1]/div[1]/span/div/div[6]/table/tbody/tr/td/div/table/tbody/tr[1]/td[3]/a').click()
    #driver.find_element_by_xpath('(//tr[contains(@id,"row_cmdb_ci_business_app_")]/td[3]/a)[1]').click()
		#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '(//tr[contains(@class,"list_row list_odd")]/td[3]/a)[1]')))
		elements = driver.find_elements_by_xpath('(//tr[contains(@class,"list_row list_odd")]/td[3]/a)[1]')
		if len(elements)>0:
			elements[0].click()
			return "True"
		else:
			driver.back()
			time.sleep(5)
			print("Element Not available")
			return "False"
	except Exception as e:
		print(e)
		


def refresh():
	#content = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '(//tr[contains(@class,"list_row list_odd")]/td[3]/a)[1]')))
	try:
		if len(driver.find_elements_by_id("sub-frame-error")) > 0:
			driver.refresh()
			WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "gsft_main")))
			driver.switch_to.frame('gsft_main')
			driver.find_element_by_id("cmdb_ci_business_app_table_header_search_control").send_keys(application)
			act.send_keys(Keys.ENTER).perform()
		else:
			pass
	except Exception as e:
		print(e)


def fetch_data():
	Op_locater = driver.find_element_by_xpath('//select[@id="sys_readonly.cmdb_ci_business_app.operational_status"]/option[@selected="SELECTED"]')
	Op_status = Op_locater.text
	Install_locater = driver.find_element_by_id("cmdb_ci_business_app.install_type_label")
	Install_type = Install_locater.text
	return Op_status, Install_type


def store_data(application):
	name = application
	dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	op_status, install_type = fetch_data()
	#Establishing the connection
	conn = psycopg2.connect(database="Automation", user='postgres', password='Personalac@07', host='127.0.0.1', port= '5432')
	#Setting auto commit false
	conn.autocommit = False
	#Creating a cursor object using the cursor() method
	cursor = conn.cursor()
	query = """INSERT INTO "TBL_APPLICATION"(name, date_time, op_status, install_type, threat_model, threat_model_update
	) VALUES (%s, %s, %s, %s, %s, %s)"""
	values = (name, dt, op_status, install_type, '', '')
	cursor.execute(query, values)
	cursor.close()
	conn.commit()
	conn.close()


def back():
	try:
		driver.back()
		print("1st back")
		#WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "gsft_main")))
		driver.back()
		print("2nd back")
		# WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "gsft_main")))
		# driver.switch_to.frame('gsft_main')
		
		# WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "cmdb_ci_business_app_table_header_search_control")))
		# search_bar = driver.find_element_by_id("cmdb_ci_business_app_table_header_search_control")
		# search_bar.clear()
		clear()
	except Exception as e:
		print(e)


def clear():
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "gsft_main")))
	driver.switch_to.frame('gsft_main')
	print("exception")
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "cmdb_ci_business_app_table_header_search_control")))
	driver.find_element_by_id("cmdb_ci_business_app_table_header_search_control").clear()

def main():
    try:
        open_the_website(url)
        time.sleep(4)
        login(usr_id, pasword)
        time.sleep(5)
        mfa_auth()
        search_for(term)
        apps = read_apps()
        driver.switch_to.frame('gsft_main')
        for app in apps:
        	time.sleep(2)
        	searched = search_app(app)
        	print(searched)
        	if searched == "False":
        		print("Enterd")
        		clear()
        		continue
        	store_data(app)
        	back()
    except Exception as e:
        print(e)
    # finally:
    # 	time.sleep(4)
    # 	driver.close()

if __name__ == "__main__":
    main()
