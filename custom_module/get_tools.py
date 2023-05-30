import requests, redis, json
import time 

def get_timestamp(time_val):
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(time_val))

def get_all_krw(host,port,db):
    r = redis.Redis(host=host, port=port, db=db)
    url = "https://api.bithumb.com/public/ticker/ALL_KRW"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    json_data = response.json()['data']
    pairs_list = [[key, value] for key, value in json_data.items()]

    for pair in pairs_list[:-1]:
        if not r.exists(pair[0]):
            r.set(pair[0], json.dumps(pairs_list[-1][1])+":"+json.dumps(pair[1]))
        else:
            r.append(pair[0],","+"\n" + json.dumps(pairs_list[-1][1])+":"+json.dumps(pair[1]))

# get_all_krw("localhost",6379,0)
