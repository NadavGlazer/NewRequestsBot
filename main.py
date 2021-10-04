from datetime import datetime
import time
import utils
import os 

if __name__ == "__main__":
    while(True):
        current_minute = datetime.now().strftime("%M")
        print(current_minute)
        if current_minute == current_minute:
            break
        if(current_minute != 59):
            time.sleep(60)
    
    while(True):
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
        else:
            print("Noting new")
        
        time.sleep(3600)    


