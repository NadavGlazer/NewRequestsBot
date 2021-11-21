# NewRequestsBot
Extracts information from city`s websites, and sends mails to given people when there`s new updates.

Creating and running the docker :
Open CMD

enter youre machine
# ssh name@ip
# password

cd .....
#cd docker file location

docker build --rm -t munitcipal[version] .
#Build the docker : for example:
docker build --rm -t munitcipal0.1 .

docker run -ti -d  munitcipal0.21
#Run the docker- for example : 
docker run -ti -d  munitcipal0.1
----------------------------------- 
Finished - the docker is now up.


Adding new city`s website : 
Open winSCP
Go to the JSON file (config.json) 
Copy the last cell of the array "Citys"
Paste it after it
Add 1 to the number
Change the name of the cell (one word - no space)
Change the URL of the cell
#For Example :

"1": [
                {
                    "Name": "Holon",
                    "url": "https://www.holon.muni.il/Residents/Engineering/LocatingInformation/Pages/pirsumim2.aspx",
                    "from_date_table_id": "PubsDateFrom",
                    "today_button_class_name": "today",
                    "submit_button_xpath": "//*[@id='btnShow']",
                    "request_table_xpath": "//*[@id=\"bk-results-table\"]/tbody/tr",
                    "request_table_first_cell_xpath": "//*[@id=\"bk-results-table\"]/tbody/tr/td[1]",
                    "plan_table_xpath": "//*[@id=\"tb-results-table\"]/tbody/tr",
                    "plan_table_first_cell_xpath": "//*[@id=\"tb-results-table\"]/tbody/tr/td[1]"
                }
            ] 
Changes to :

"2": [
                {
                    "Name": "CityName",
                    "url": "CityURL",
                    "from_date_table_id": "PubsDateFrom",
                    "today_button_class_name": "today",
                    "submit_button_xpath": "//*[@id='btnShow']",
                    "request_table_xpath": "//*[@id=\"bk-results-table\"]/tbody/tr",
                    "request_table_first_cell_xpath": "//*[@id=\"bk-results-table\"]/tbody/tr/td[1]",
                    "plan_table_xpath": "//*[@id=\"tb-results-table\"]/tbody/tr",
                    "plan_table_first_cell_xpath": "//*[@id=\"tb-results-table\"]/tbody/tr/td[1]"
                }
            ] 
            
Kill the old docker - docker kill [Docker ID]
Create The updated one (look line 4)


