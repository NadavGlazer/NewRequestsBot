from datetime import datetime
from selenium import webdriver
import time
import json
import os
import smtplib


def run_on_working_hours():
    """Runs the program"""
    while(True):
        if (check_if_working_hours()):
            filename = generate_daily_information_text_file()
            current_request_amount = find_request_amount_by_city("RishonLezion")
            last_line = ""
            with open("InformationFiles/" + filename, "r+") as information_file:
                information_file.write(datetime.now().strftime("%H:%M:%S*") + " " + str(current_request_amount) +"\n")
                for line in information_file:
                        last_line = line
            
            last_request_amount = int(last_line.split("*")[1])

            if current_request_amount > last_request_amount:
                print("New requests")
                send_email("RishonLezion")
            else:
                print("Noting new")
            
            print("Waiting for an hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(3600)
        else:
            print("Waiting half a hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(1800)

def check_if_working_hours():
    """Returns True if its working hours else returns False"""
    """Working hours are set from 8:00 to 17:00"""
    if int(datetime.now().strftime("%H")) >=18 :
        print("too late")           
    elif int(datetime.now().strftime("%H")) <7:
        print("too early")
    else:
        return True
    return False      


def find_request_amount(driver_path, url, from_date_table_id, today_button_class_name, submit_button_xpath, request_table_xpath, main_request_table_xpath):
    """Gets the information about one site and returns the amount of requests"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--headless")  


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

    #To take off options of 0 elements - 0 requests. 
    try:
        requests_table = driver.find_element_by_xpath(main_request_table_xpath)
    except:
        driver.close()
        print(0)
        return(0)

    request_table = driver.find_elements_by_xpath(request_table_xpath)
    request_amount = len(request_table)
    
    print(request_amount)

    driver.close()

    return(request_amount)

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
        json_data[city][0]["request_table_xpath"],
        json_data[city][0]["main_request_table_xpath"]
    ))

def generate_daily_information_text_file():
    """generates the filename and the file"""

    filename = "Information_" + datetime.now().strftime("%d_%m_%y")
    is_new_day = os.path.exists("InformationFiles/" + filename)

    with open("InformationFiles/" + filename,"a") as information_file:
        if not is_new_day:
            information_file.write(datetime.now().strftime("%H:%M:%S") + "* " +"0" +"\n")

    return(filename)

def send_email(city):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('nesahbot@gmail.com', 'Abcd1234!')

    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)
   
    smtpObj.sendmail('nesahbot@gmail.com','nadav28223@gmail.com','Subject: New Requests at - ............................ ' + json_data[city][0]["url"])
    print("Sent Mail")
    smtpObj.quit()
            
