from datetime import datetime
from selenium import webdriver
import time
import json
import os
import smtplib
from email.message import EmailMessage

from selenium.webdriver.chrome import options
from selenium.common.exceptions import WebDriverException   

def check_if_working_hours():
    """Returns True if its working hours else returns False"""
    """Working hours are set from 8:00 to 17:00"""

    #Checks if its Friday or Saturday
    if datetime.today().weekday() == 4 or datetime.today().weekday() == 5:
        print("Rest days")
    elif int(datetime.now().strftime("%H")) >= 18 :
        print("too late")           
    elif int(datetime.now().strftime("%H")) < 7:
        print("too early")
    else:
        return True
    return False      


def get_request_amount(driver, filename, city_data):
    """Gets the information about one site and returns the amount of requests"""
    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)

    #Getting all the needed information from the json file
    city_name = city_data["Name"]
    url = city_data["url"]
    from_date_table_id = city_data["from_date_table_id"]
    today_button_class_name = city_data["today_button_class_name"]
    submit_button_xpath = city_data["submit_button_xpath"]
    request_table_xpath =  city_data["request_table_xpath"]
    request_table_first_cell_xpath = city_data["request_table_first_cell_xpath"]
    plan_table_xpath = city_data["plan_table_xpath"]
    plan_table_first_cell_xpath = city_data["plan_table_first_cell_xpath"]
    request_number_template_xpath = city_data["request_number_template_xpath"]
    plan_number_template_xpath = city_data["plan_number_template_xpath"]
    no_data_found_hebrow = json_data["NoDataFoundHebrow"]

    #Opening the URL
    try:
        driver.get(url)
    except WebDriverException:
        print("page down")
        return []
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
    
    #Calculating the total amount of updates
    current_uploads_amount = plan_amount + request_amount
    current_uploads_amount_seperated =  str(request_amount) + "*" + str(plan_amount)

    #Reads the last amount of uploaded files from the information file
    last_uploads_data = get_last_updates_amount_of_city(filename)
    
    #Return False if no uploads
    if current_uploads_amount == 0:
        return []
    
    current_request_numbers = []
    for i in range(1, request_amount + 1) :        
        current_request_numbers.append((driver.find_element_by_xpath(request_number_template_xpath.replace("COUNTER", str(i))).text))
    
    current_plan_numbers = []
    for i in range(1, plan_amount + 1) :        
        current_plan_numbers.append((driver.find_element_by_xpath(plan_number_template_xpath.replace("COUNTER", str(i))).text))
    print(current_request_numbers, current_plan_numbers)
    
    if current_plan_numbers:
        total_current_updates_numbers = current_request_numbers.append(current_plan_numbers)
    else:
        total_current_updates_numbers = current_request_numbers 

    last_requests_numbers = []  
    last_plans_numbers = []

    last_number_of_requests = int(last_uploads_data.split("*")[0])
    last_number_of_plans = int(last_uploads_data.split("*")[1])

    #Extracting the data from the information file to two seperate lists   
    if last_number_of_plans + last_number_of_requests > 0:      
        last_uploads_data = last_uploads_data.split("*", 2)[2]        
        
        counter = 0
        for number in last_uploads_data.split("*"):
            if counter < last_number_of_requests :
                last_requests_numbers.append(number.replace("\n", ""))
            else:
                last_plans_numbers.append(number.replace("\n", ""))
            counter += 1        
    print(last_requests_numbers, last_plans_numbers)      
    
    new_requests_numbers = list(set(current_request_numbers) - set(last_requests_numbers))
    new_plans_numbers = list(set(current_plan_numbers) - set(last_plans_numbers))
    
    if not new_plans_numbers and not new_requests_numbers:
        set_data_in_information_file(filename, current_uploads_amount_seperated , total_current_updates_numbers)
        return []    
    
    information = []
    information.append(city_name)
    information.append(url)
    information.append(str(len(new_plans_numbers+new_requests_numbers)))

    counter = 1
    for number in new_requests_numbers:
        information.append(get_data_of_specific_update_number(driver, number, city_data, json_data, "request", counter))
        counter += 1

    counter = 1
    for number in new_plans_numbers:
        information.append(get_data_of_specific_update_number(driver, number, city_data, json_data, "plan", counter))
        counter += 1

    #Writing the new data in the infomation file       
    set_data_in_information_file(filename, current_uploads_amount_seperated , total_current_updates_numbers)

    return information


def generate_city_daily_information_text_file(city):
    """generates the filename and the file"""

    filename = str(city) + "_Information_" + datetime.now().strftime("%d_%m_%y")
    file_path = "InformationFiles/"+ datetime.now().strftime("%d_%m_%y/")
    is_new_day = os.path.exists(file_path + filename)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open("InformationFiles/" + datetime.now().strftime("%d_%m_%y/") + filename,"a") as information_file:
        if not is_new_day:
            information_file.write(datetime.now().strftime("%H:%M:%S") + "*" +"0" + "*" +"0"+"\n")
        

    return(filename)

def send_email(city_data_array):
    """Gets a city and sends mail that theres new uploads"""
    
    json_file = open("config.json", encoding="utf8")
    json_data = json.load(json_file)  


    EMAIL_ADDRESS = json_data["BotEmailInfo"][0]["EmailAdress"]
    EMAIL_PASSWORD = json_data["BotEmailInfo"][0]["Password"]

    contacts = json_data["MailingList"]

    massage = ""
    for city in city_data_array:        
        details_list = []
        for i in range (len(city)):
            if i > 2:
                details_list.append(city[i])

        massage = massage + city[2] + " New Uploads in " + city[0] + " site -- " + city[1] + "\n"
        print(details_list)
        for data in details_list:
            massage = massage + data[0] + " , " + data[1] + " , " + data[2] + " , " + data[3] + " , " + data[4] + "\n"
            massage = massage + "\n"
        massage = massage + "\n"


    msg = EmailMessage()
    msg['Subject'] = 'New Updates'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    msg.set_content(massage)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        except:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    print("Sent Mail")

def get_last_updates_amount_of_city(filename):
    """Gets filename and uploads amount and returns last amount and adds to the the file the current amount"""
    last_line = ""
    with open("InformationFiles/"+ datetime.now().strftime("%d_%m_%y/") + filename, "r+") as information_file:
        for line in information_file:
                last_line = line 

    last_uploads_data = last_line.split("*",1)[1]
    return str(last_uploads_data)

def set_data_in_information_file(filename, current_uploads_amount , current_uploads_numbers):
    """Gets filename and uploads numbers and writes them in the file"""
    
    current_uploads_numbers_string = ""
    if current_uploads_numbers:
        for number in current_uploads_numbers:
            current_uploads_numbers_string = current_uploads_numbers_string + "*" + str(number)     
    
    with open("InformationFiles/"+ datetime.now().strftime("%d_%m_%y/") + filename, "r+") as information_file:
        for line in information_file:
            pass
        information_file.write(datetime.now().strftime("%H:%M:%S*") + str(current_uploads_amount) +current_uploads_numbers_string +"\n")  
            
def get_data_of_specific_update_number(driver, number, city_data, json_data, type_of_update, counter):
    """Gets the needed data and returns the names and type of project"""  
    
    information = []
    #Getting all the needed information from the json file
    url = city_data["url"]
    from_date_table_id = city_data["from_date_table_id"]
    today_button_class_name = city_data["today_button_class_name"]
    submit_button_xpath = city_data["submit_button_xpath"]

    if type_of_update == "request":
        number_template_xpath = city_data["request_number_template_xpath"]
        type_of_project_xpath = city_data["request_type_of_project_xpath"]

    else:
        number_template_xpath = city_data["plan_number_template_xpath"]
        type_of_project_xpath = city_data["plan_type_of_project_xpath"]

    man_of_interest_table_button_xpath = city_data["man_of_interest_table_button_xpath"]
    man_of_interest_table_xpath = city_data["man_of_interest_table_xpath"]
    type_of_man_of_interest_xpath = city_data["type_of_man_of_interest_xpath"]
    name_of_man_of_interest_xpath = city_data["name_of_man_of_interest_xpath"]

    asking_hebrow = json_data["AskingHebrow"]
    editing_hebrow = json_data["EditingHebrow"]

    information.append(number)
    if type_of_update == "request":
        information.append("בקשה")
    else:
        information.append("תוכנית")

    #Opening the URL
    try:
        driver.get(url)
    except WebDriverException:
        print("page down")
        information.append("")
        information.append("")
        information.append("")
        return information
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

    #Getting the type of the project from the table
    try:
        type_of_project = driver.find_element_by_xpath(type_of_project_xpath.replace("COUNTER", str(counter))).text
    except:
        time.sleep(2)
        type_of_project = "Error"
    information.append(type_of_project)

    #Entering to the specific project number site
    try:
        number_button = driver.find_element_by_xpath((number_template_xpath.replace("COUNTER", str(counter))))
    except:
        time.sleep(2)
        number_button = driver.find_element_by_xpath((number_template_xpath.replace("COUNTER", str(counter))))   
    number_button.click()
    time.sleep(2)    

    try:
        man_of_interest_table_button = driver.find_element_by_xpath(man_of_interest_table_button_xpath)
    except:
        try:
            man_of_interest_table_button = driver.find_element_by_xpath(man_of_interest_table_button_xpath)
        except:        
            information.append("")
            information.append("")
            return information
    if not man_of_interest_table_button.get_attribute('aria-expanded'):
        man_of_interest_table_button.click()

    man_of_interest_table =  driver.find_elements_by_xpath(man_of_interest_table_xpath)
    man_of_interest_amount = len(man_of_interest_table)
    print(man_of_interest_amount)  

    name_asking_man_of_interest = ""
    name_editing_man_of_interest = ""
    for i in range(1, man_of_interest_amount + 1):
        print(driver.find_element_by_xpath((type_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text)

        try:
            type_of_man_of_interest = driver.find_element_by_xpath((type_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text
        except:
            time.sleep(2)
            type_of_man_of_interest = driver.find_element_by_xpath((type_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text
        if type_of_man_of_interest == asking_hebrow :
            try:
                name_asking_man_of_interest = name_asking_man_of_interest + driver.find_element_by_xpath((name_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text + "," 
            except:
                time.sleep(2)
                name_asking_man_of_interest = name_asking_man_of_interest + driver.find_element_by_xpath((name_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text + "," 
        elif type_of_man_of_interest == editing_hebrow :
            try:
                name_editing_man_of_interest = name_editing_man_of_interest + driver.find_element_by_xpath((name_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text + "," 
            except:
                time.sleep(2)
                name_editing_man_of_interest = name_editing_man_of_interest + driver.find_element_by_xpath((name_of_man_of_interest_xpath.replace("COUNTER", str(i)))).text + "," 
    
    print(name_editing_man_of_interest, name_asking_man_of_interest)
    information.append(name_asking_man_of_interest)
    information.append(name_editing_man_of_interest)
    return information


