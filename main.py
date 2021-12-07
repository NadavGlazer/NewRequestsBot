import utils
import json
from selenium import webdriver
import time
from datetime import datetime


def run_on_working_hours():
    """Runs the program"""
    while(True):
        if (utils.check_if_working_hours()):
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
                
                filename = utils.generate_city_daily_information_text_file(city_name)
                
                print("\n" + "Started checking " + city_name)
                #Gets the current amount of uploaded files and the data, will return [] if none
                is_new_updates = utils.get_request_amount(driver, filename, city_data)
                                        
                if is_new_updates:
                    city_with_updates.append(is_new_updates)
                    print("Finished" + city_name) 
                else:
                    print("Noting changed in " + city_name)
                counter += 1
            
            if city_with_updates:
                utils.send_email(city_with_updates)
            

            driver.close()

            #Waiting an hour then checking again
            print("Waiting half an hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(1800)
        else:
            #Waiting half an hour then checking again
            print("Waiting half an hour " + datetime.now().strftime("%H:%M:%S"))
            time.sleep(1800)

if __name__ == "__main__":
    #json_file = open("config.json", encoding="utf8")
    #json_data = json.load(json_file)
    # for city in json_data["Citys"]:
    #     print(json_data["Citys"][0][str(0)][0]["Name"])
    # c = []
    # c.append(json_data["Citys"][0][str(0)][0])
    # utils.send_email(c)
    run_on_working_hours()

