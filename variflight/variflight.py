import hashlib
import json
import requests
import time
import urllib.parse
import random
import os

Airline_Company = "MU"

with open("variflight\City_List.json", "r", encoding="utf-8") as f:
    City_List = json.load(f)
    f.close()

def getmd5(s):
    m1 = hashlib.md5()
    m1.update(s.encode(encoding="utf-8"))
    return m1.hexdigest().upper()

def gettimestamp():
    return str(round(time.time() * 1000))

url = "https://app.variflight.com/v4/plane_ticket_h5/proxy"

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Origin': 'https://app.variflight.com',
    'Referer': 'https://app.variflight.com/html/activity/ticket/flightline/index.html?feeyo_nav_background=0xff1e71ff&feeyosharetype=url',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
    'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

result = []

for city in City_List:
    print(city.get("CityCode"))
    file = "variflight\\" + Airline_Company + "_City_Data\\" + city.get("CityCode") +".json"
    os.makedirs(os.path.dirname(file), exist_ok=True)

    timestamp = gettimestamp()

    data = {
        'action': 'alLine',
        'appKey': 'undefined',
        'channel': 'ticketbanner',
        'dep': city.get("CityCode"),
        'feeyo_nav_background': '0xff1e71ff',
        'feeyosharetype': 'url',
        'timestamp': timestamp,
        'type': Airline_Company,
    }


    signature = getmd5("d7Eohd8h-tFdKG2ddtZ-7z3AbsInLitZ" + getmd5(urllib.parse.urlencode(data)) + "d7Eohd8h-tFdKG2ddtZ-7z3AbsInLitZ")

    data.update({'signature': signature})

    # with open(file, "r", encoding="utf-8") as f:
    #     res_json = json.load(f)["data"]["result"]
    #     f.close()

    res = requests.post(url=url,data=data,headers=headers)
    res_json = res.json()["data"]["result"]
    with open(file, "w", encoding="utf-8") as f:
        json.dump(res.json(), f, indent=2, ensure_ascii=False)
        f.close()

    if(len(res_json)!=0): 
        result_line = ""
        result_line += res_json[0]["depCityName"] + "\t"
        airline_json = sorted(res_json, key=lambda k: k['lat'])
        count = 0
        for airline in airline_json:
            if(airline["price"]!=0):
                count += 1

                result_line += airline["arrCityName"] + "，"
                airport_json = {"CityCode": airline["arrCityCode"]}
                if airport_json not in City_List:
                    City_List.append(airport_json)
                    with open("variflight\\City_List.json", "w", encoding="utf-8") as f:
                        json.dump(City_List, f, indent=2, ensure_ascii=False)
                        f.close()

        result_line = result_line.rstrip("，") + "\n"
        result_item = {"content": result_line,
                    "count": count}
        if(count!=0):
            result.append(result_item)
    
    time.sleep(random.randint(3000, 6000)/1000)

result = sorted(result, key=lambda k: k['count'],reverse=True)

with open("VariFlight_" + Airline_Company + "_Airlines.txt", "w", encoding="utf-8") as f:
    s = ""
    for each in result:
        s += each["content"]
    f.write(s)
    f.close()
