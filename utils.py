from datetime import date
from selenium import webdriver
import time

def find_new_request(driver_path, url, from_date_table_id, today_button_class_name, submit_button_xpath, request_table_xpath):
    """Gets the information about one site and returns the amount of requests"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(executable_path= driver_path, chrome_options=chrome_options) 
    driver.maximize_window()
    
    driver.get(url)
    time.sleep(2)

    from_date = driver.find_element_by_id(from_date_table_id)
    from_date.click()

    today_button = driver.find_element_by_class_name(today_button_class_name)
    today_button.click()

    submit_button = driver.find_element_by_xpath(submit_button_xpath)
    submit_button.click()

    request_table = driver.find_elements_by_xpath(request_table_xpath)
    print(len(request_table))
    return(len(request_table))