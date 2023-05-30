import requests, redis, json


r = redis.Redis(host='localhost', port=6379, db=0)
url = "https://api.bithumb.com/public/ticker/ALL_KRW"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
json_data = response.json()['data']
pairs_list = [[key, value] for key, value in json_data.items()]
print(pairs_list)

for pair in pairs_list:
    print(pair[0], pair[1:])
# r.set('mydata', json_data)
