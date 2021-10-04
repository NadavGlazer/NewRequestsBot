from selenium import webdriver
from datetime import datetime
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(executable_path='C:\\Users\\Nadav1\\Downloads\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options ) 
driver.maximize_window()

url = "https://rishonlezion.complot.co.il/newengine/Pages/pirsumim2.aspx"

driver.get(url)
time.sleep(2)
#current_date = datetime.now().strftime("%d/%m/%Y")

from_date = driver.find_element_by_id('PubsDateFrom')
from_date.click()

today_button = driver.find_element_by_class_name('today')
today_button.click()

submit_button = driver.find_element_by_xpath('//*[@id="btnShow"]')
submit_button.click()

new_request_table = driver.find_elements_by_xpath("//table/tbody/tr")
print(len(new_request_table))