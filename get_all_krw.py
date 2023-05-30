import requests, redis, json

def get_all_krw(host,port,db):
    r = redis.Redis(host=host, port=port, db=db)
    url = "https://api.bithumb.com/public/ticker/ALL_KRW"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    json_data = response.json()['data']
    pairs_list = [[key, value] for key, value in json_data.items()]

    for pair in pairs_list[:-1]:
        r.set(pair[0], json.dumps({pairs_list[-1][1]: pair[1]}))


# get_all_krw("localhost",6379,0)


