from datetime import datetime
from selenium import webdriver
import time
import json
import os
import smtplib
from email.message import EmailMessage

from selenium.webdriver.chrome import options


def run_on_working_hours():
    """Runs the program"""
    while(True):
        if (check_if_working_hours()):
            #Creates new information file in the begging of the day else does noting
            json_file = open("config.json", encoding="utf8")
            json_data = json.load(json_file)

            city_with_updates = []
            counter = 0
            #Sets the Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  
            options.add_argument("--hide-scrollbars")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
    
            #Creating the driver
            try:
                driver = webdriver.Chrome(executable_path = json_data["MainComputerDriverPath"], chrome_options=options)
            except:
                time.sleep(1)
                driver = webdriver.Chrome(executable_path = json_data["MainComputerDriverPath"], chrome_options=options)
            time.sleep(2)

            while counter < len(json_data["Citys"][0]):
                city_data = json_data["Citys"][0][str(counter)][0]         
                city_name = city_data["Name"]

                filename = generate_city_daily_information_text_file(city_name)
                
                #Gets the current amount of uploaded files 
                current_uploads_amount = find_request_amount_by_city(city_data, driver)            
                
                #Reads the last amount of uploaded files from the information file
                last_line = ""
                with open("InformationFiles/" + filename, "r+") as information_file:
                    information_file.write(datetime.now().strftime("%H:%M:%S*") + " " + str(current_uploads_amount) +"\n")
                    for line in information_file:
                            last_line = line
            
                last_uploads_amount = int(last_line.split("*")[1])

                #In case theres new uploaded files- sends mail to the relevant emails
                if current_uploads_amount > last_uploads_amount:
                    print("New Uploads In - " + city_name)
                    
                    city_with_updates.append(city_data)
                else:
                    print("Noting new In - " + city_name)
                counter += 1
            
            if city_with_updates:
                send_email(city_with_updates)
            driver.close()
            #Waiting an hour then checking again
            print("Waiting half an hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(1800)
        else:
            #Waiting half an hour then checking again
            print("Waiting half an hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(1800)

def check_if_working_hours():
    """Returns True if its working hours else returns False"""
    """Working hours are set from 8:00 to 17:00"""

    #Checks if its Friday or Saturday
    if datetime.today().weekday() == 4 or datetime.today().weekday() == 5:
        print("Rest days")
    elif int(datetime.now().strftime("%H")) >=18 :
        print("too late")           
    elif int(datetime.now().strftime("%H")) <7:
        print("too early")
    else:
        return True
    return False      


def find_request_amount(driver, url, from_date_table_id, today_button_class_name, submit_button_xpath, request_table_xpath, request_table_first_cell_xpath, plan_table_xpath, plan_table_first_cell_xpath, no_data_found_hebrow):
    """Gets the information about one site and returns the amount of requests"""
    #Opening the URL
    driver.get(url)
    time.sleep(3)

    #Starting the process of extracting the data

    #Finding and clicking on the "from date" input
    try:
        from_date = driver.find_element_by_id(from_date_table_id)
    except:
        time.sleep(2)
        from_date = driver.find_element_by_id(from_date_table_id)
    from_date.click()
    time.sleep(2)

    #Setting the date to today`s date
    try:
        today_button = driver.find_element_by_class_name(today_button_class_name)
    except:
        time.sleep(2)
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

    return(request_amount+plan_amount)

def find_request_amount_by_city(city_data, driver):
    """Gets a city, calls for 'find_request_amount' function and takes the information from the json"""
    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)

    return(find_request_amount(
        driver,
        city_data["url"],
        city_data["from_date_table_id"],
        city_data["today_button_class_name"],
        city_data["submit_button_xpath"],
        city_data["request_table_xpath"],
        city_data["request_table_first_cell_xpath"],
        city_data["plan_table_xpath"],
        city_data["plan_table_first_cell_xpath"],
        json_data["NoDataFoundHebrow"]       
    ))

def generate_city_daily_information_text_file(city):
    """generates the filename and the file"""

    filename = str(city) + "_Information_" + datetime.now().strftime("%d_%m_%y")
    is_new_day = os.path.exists("InformationFiles/" + filename)

    with open("InformationFiles/" + filename,"a") as information_file:
        if not is_new_day:
            information_file.write(datetime.now().strftime("%H:%M:%S") + "* " +"0" +"\n")

    return(filename)

def send_email(city_data_array):
    """Gets a city and sends mail that theres new uploads"""
    
    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)  


    EMAIL_ADDRESS = json_data["BotEmailInfo"][0]["EmailAdress"]
    EMAIL_PASSWORD = json_data["BotEmailInfo"][0]["Password"]

    contacts = json_data["MailingList"]

    massage = ""
    for city_data in city_data_array:
        massage = massage + "New Uploads in " + city_data["Name"] + " site -- " + city_data["url"] + "\n"

    msg = EmailMessage()
    msg['Subject'] = 'New Updates'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    msg.set_content(massage)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Sent Mail")


            
