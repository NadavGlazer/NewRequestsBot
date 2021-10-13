from datetime import datetime
import time
import utils
import os 


def run_on_working_hours():
    """Runs the program"""
    while(utils.check_if_working_hours()):
        filename = utils.generate_daily_information_text_file()
        current_request_amount = utils.find_request_amount_by_city("RishonLezion")
        last_line = ""
        with open("InformationFiles/" + filename, "r+") as information_file:
            information_file.write(datetime.now().strftime("%H:%M:%S*") + " " + str(current_request_amount) +"\n")
            for line in information_file:
                    last_line = line
        
        last_request_amount = int(last_line.split("*")[1])
        
        if current_request_amount > last_request_amount:
            print("New requests")
            utils.send_email("RishonLezion")
        else:
            print("Noting new")
        
        time.sleep(3600)


if __name__ == "__main__":
    run_on_working_hours()    
        


