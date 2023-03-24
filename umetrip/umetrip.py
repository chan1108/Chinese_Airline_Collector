import json
import requests
import time
import os

Airline_Company = "MU"

with open("umetrip\\Air_Port_List.json", "r", encoding="utf-8") as f:
    Air_Port_List = json.load(f)
    f.close()


base_url = "https://static.umetrip.com/gateway/api/web/airline/airlinearea/getairlineroutemap?airline=" + Airline_Company + "&airlineName=&dept="


def get_json(airline_text):
    airline_text = airline_text.replace(r"\"", "\"")
    airline_text = airline_text.replace(r'"{', "{")
    airline_text = airline_text.replace(r'}"', "}")
    airline_json = json.loads(airline_text)
    return airline_json

result = []

for airport in Air_Port_List:
    print(airport.get("iata"))
    file = "umetrip\\" + Airline_Company + "_Airport_Data\\" + airport.get("iata") +".txt"
    os.makedirs(os.path.dirname(file), exist_ok=True)

    # with open(file, "r", encoding="utf-8") as f:
    #     airline_text = f.read()
    #     f.close()

    res = requests.get(base_url + airport.get("iata"))
    airline_text = res.text
    with open(file, "w", encoding="utf-8") as f:
        f.write(airline_text)
        f.close()
    
    res_json = get_json(airline_text)

    if(res_json.get("errMsg")==None): 
        result_line = ""
        result_line += res_json["airportName"] + "\t"
        airline_json = sorted(res_json["airlineStatRoutePOList"], key=lambda k: k['destlat'])
        count = 0
        for airline in airline_json:
            count += 1

            
            result_line += airline["destName"] + "，"
            airport_json = {"iata": airline["destcode"]}
            if airport_json not in Air_Port_List:
                Air_Port_List.append(airport_json)
                with open("umetrip\\Air_Port_List.json", "w", encoding="utf-8") as f:
                    json.dump(Air_Port_List, f, indent=2, ensure_ascii=False)
                    f.close()

        result_line = result_line.rstrip("，") + "\n"
        result_item = {"content": result_line,
                    "count": count}
        result.append(result_item)

    time.sleep(3)

result = sorted(result, key=lambda k: k['count'],reverse=True)

# with open("Air_Port_List.json", "w", encoding="utf-8") as f:
#     json.dump(Air_Port_List, f, indent=2, ensure_ascii=False)
#     f.close()

with open("UMETrip_" + Airline_Company + "_Airlines.txt", "w", encoding="utf-8") as f:
    s = ""
    for each in result:
        s += each["content"]
    f.write(s)
    f.close()

