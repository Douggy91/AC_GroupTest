import redis, math, json
import numpy as np
import pandas as pd

r=redis.Redis(host="localhost", port=6379, db=0)
data = json.loads("{"+r.get("\"datetime\":\"23-05-31 16:10\"").decode("utf-8")+"}")

print(type(data))
print(pd.DataFrame(data).T)

data_all={}
for sort in r.keys("*"):
    s_date = sort.decode("utf-8")
    data_pre = json.loads("{"+r.get(s_date).decode("utf-8")+"}")
    data_all[s_date] = data_pre
df_all = pd.DataFrame.from_dict(data_all).T
print(df_all)