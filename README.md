# NewRequestsBot
Extracts information from citys websites, and sends mails to given people when theres new updates.

Creating and running the docker :
----------------------------------- 

Open cmd

enter youre machine
          ssh name@ip
          password

cd docker file location

docker build --rm -t munitcipal[version] .
Build the docker - for example:
          docker build --rm -t munitcipal0.1 .

docker run -ti -d  munitcipal0.21
Run the docker - for example : 
          docker run -ti -d  munitcipal0.1
          
Finished - the docker is up.


#Adding new citys website :
----------------------------------- 

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
                    "url": "https://www.holon.muni.il/Residents/Engineering/LocatingInformation/Pages/pirsumim2.aspx"
                }
            ] 
'Changes to :'

"2": [
                {
                    "Name": "CityName",
                    "url": "CityURL"
                }
            ] 
            

Kill the old docker - docker kill [Docker ID]

Create The updated one (look line 4)

Finished - The docker is up and updated.
