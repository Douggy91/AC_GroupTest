from custom_module import get_tools as getkrw
import requests, redis, json, time, math
import numpy as np
import pandas as pd

def get_all_krw(host,port,db):
    r = redis.Redis(host=host, port=port, db=db)
    url = "https://api.bithumb.com/public/ticker/ALL_KRW"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    json_data = response.json()['data']
    items_list = list(json_data.keys())[:-1]
    time_val=getkrw.get_timestamp(math.floor(int(json_data["date"]))/1000)
    first_item = items_list[0]
    last_item = items_list[-1]
    r.set("\"datetime\":" + "\""+time_val.replace("\"","")+ "\"", "\""+first_item+"\"" + ":" +json.dumps(json_data[first_item])+",\n")
    for item in items_list[1:-1]:
        item_data = json.dumps(json_data[item])
        r.append("\"datetime\":" + "\""+time_val.replace("\"","")+ "\"", "\""+item+"\"" + ":" +item_data+",\n")
    r.append("\"datetime\":" + "\""+time_val.replace("\"","")+ "\"", "\""+last_item+"\"" + ":" +json.dumps(json_data[last_item]))

    
getkrw.get_all_krw("redis-db.test-app.svc.cluster.local", 6379, 0)
