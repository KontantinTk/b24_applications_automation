from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

options = webdriver.ChromeOptions()
# options.add_argument("headless")
# options.add_argument('window-size=900x900')

path_to_driver = "C:\\tools\\chromedriver.exe"

path_to_portal = "https://portal.consult-info.ru/"

path_to_app = "https://portal.consult-info.ru/marketplace/app/7/"

driver = webdriver.Chrome(executable_path=path_to_driver, chrome_options=options)

input_login_name = "USER_LOGIN"
input_password_name = "USER_PASSWORD"

driver.get(path_to_portal)
login_input = driver.find_element_by_name(input_login_name)
login_input.send_keys("my_login")

password_input = driver.find_element_by_name(input_password_name)
password_input.send_keys("my_password")

submit_button = driver.find_element_by_css_selector("input[type=submit]")
submit_button.click()

try:
    workarea = driver.find_element_by_id("workarea-content")
    print("Logged in successfully")
except:
    print("Error while logging")

driver.get(path_to_app)

#Connecting application
driver.switch_to_frame(1)
driver.switch_to_frame("partner_application")
print("Found frame")

#click on Filter
time.sleep(6)
driver.find_element_by_css_selector("input[name=FIND]").click()
print("Show filter list")
#click on lead variant
time.sleep(2)
driver.find_element_by_css_selector(".main-ui-control.main-ui-select").click()
time.sleep(2)
print("Show lead variants")

driver.execute_script("console.log(frameElement)")
print("Test script")

driver.execute_script('''
frameElement.contentDocument.querySelector("[data-type=SELECT][data-name=PARTNERSHIP] > [data-name=PARTNERSHIP]").setAttribute('data-value', '{"NAME":"Битрикс24","VALUE":"B24"}')
''')

#click find button
driver.find_element_by_css_selector("button.main-ui-filter-find").click()
print("Try to find")

# time.sleep(10)
# driver.close()