import selenium
from datetime import datetime
from selenium import webdriver
import time
import json
import os

def find_request_amount(driver_path, url, from_date_table_id, today_button_class_name, submit_button_xpath, request_table_xpath):
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

    driver.close()

    return(len(request_table))

def find_request_amount_by_city(city):
    """Gets a city, calls for 'find_request_amount' function and takes the information from the json"""
    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)

    return(find_request_amount(
        json_data["MainComputerDriverPath"],
        json_data[city][0]["url"],
        json_data[city][0]["from_date_table_id"],
        json_data[city][0]["today_button_class_name"],
        json_data[city][0]["submit_button_xpath"],
        json_data[city][0]["request_table_xpath"]
    ))
def generate_daily_information_text_file():
    """generates the filename and the file"""

    filename = "Information_" + datetime.now().strftime("%d_%m_%y")
    is_new_day = os.path.exists("InformationFiles/" + filename)

    with open("InformationFiles/" + filename,"a") as information_file:
        if not is_new_day:
            information_file.write(datetime.now().strftime("%H:%M:%S") + "* " +"0" +"\n")

    return(filename)
            
