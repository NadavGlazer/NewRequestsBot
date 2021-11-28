import utils
import json
if __name__ == "__main__":
    #json_file = open("config.json", encoding="utf8")
    #json_data = json.load(json_file)
    # for city in json_data["Citys"]:
    #     print(json_data["Citys"][0][str(0)][0]["Name"])
    # c = []
    # c.append(json_data["Citys"][0][str(0)][0])
    # utils.send_email(c)
    utils.run_on_working_hours()