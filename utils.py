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
            #Creates new information file in the begging of the day else does noting
            filename = generate_daily_information_text_file()

            #Gets the current amount of uploaded files 
            current_uploads_amount = find_request_amount_by_city("RishonLezion")
            
            #Reads the last amount of uploaded files from the information file
            last_line = ""
            with open("InformationFiles/" + filename, "r+") as information_file:
                information_file.write(datetime.now().strftime("%H:%M:%S*") + " " + str(current_uploads_amount) +"\n")
                for line in information_file:
                        last_line = line
            
            last_uploads_amount = int(last_line.split("*")[1])

            #In case theres new uploaded files- sends mail to the relevant emails
            if current_uploads_amount > last_uploads_amount:
                print("New requests")
                send_email("RishonLezion")
            else:
                print("Noting new")
            
            #Waiting an hour then checking again
            print("Waiting for an hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(3600)
        else:
            #Waiting half an hour then checking again
            print("Waiting half an hour " + datetime.now().strftime("%H:%M:%S"))
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


def find_request_amount(driver_path, url, from_date_table_id, today_button_class_name, submit_button_xpath, request_table_xpath, request_table_first_cell_xpath, plan_table_xpath, plan_table_first_cell_xpath, no_data_found_hebrow):
    """Gets the information about one site and returns the amount of requests"""
    #Sets the Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    #Creating the driver
    try:
        driver = webdriver.Chrome(executable_path= driver_path, chrome_options=chrome_options)
    except:
        time.sleep(1)
        driver = webdriver.Chrome(executable_path= driver_path, chrome_options=chrome_options)
    time.sleep(2)

    #Opening the URL
    driver.get(url)
    time.sleep(2)

    #Starting the process of extracting the data

    #Finding and clicking on the "from date" input
    try:
        from_date = driver.find_element_by_id(from_date_table_id)
    except:
        time.sleep(1)
        from_date = driver.find_element_by_id(from_date_table_id)
    from_date.click()
    time.sleep(2)

    #Setting the date to today`s date
    today_button = driver.find_element_by_class_name(today_button_class_name)
    today_button.click()
    time.sleep(2)

    #Submiting the date
    submit_button = driver.find_element_by_xpath(submit_button_xpath)
    submit_button.click()
    time.sleep(2)
    
    #Getting the amount of requests in the site
    request_table = driver.find_elements_by_xpath(request_table_xpath)
    request_amount = len(request_table)
    #Checking if theres no requests
    if request_amount == 1 and driver.find_element_by_xpath(request_table_first_cell_xpath).text == no_data_found_hebrow:
        request_amount = 0      
    print(request_amount)        

    #Getting the amount of plans in the site
    plans_table =  driver.find_elements_by_xpath(plan_table_xpath)
    plan_amount = len(plans_table)
    #Checking if theres no plans
    if plan_amount == 1 and driver.find_element_by_xpath(plan_table_first_cell_xpath).text == no_data_found_hebrow:
        plan_amount = 0     
    print(plan_amount)

    driver.close()

    return(request_amount+plan_amount)

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
        json_data[city][0]["request_table_first_cell_xpath"],
        json_data[city][0]["plan_table_xpath"],
        json_data[city][0]["plan_table_first_cell_xpath"],
        json_data["NoDataFoundHebrow"]       
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
    """Gets a city and sends mail that theres new uploads"""
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('nesahbot@gmail.com', 'Abcd1234!')

    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)
   
    smtpObj.sendmail('nesahbot@gmail.com','nadav28223@gmail.com','Subject: New Uploads at - ............................ ' + json_data[city][0]["url"])
    print("Sent Mail")
    smtpObj.quit()
            
