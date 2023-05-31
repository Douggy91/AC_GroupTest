import redis, math, json
import numpy as np
import pandas as pd


r=redis.Redis(host="localhost", port=6379, db=0)
data = json.loads("{"+r.get("\"datetime\":\"23-05-31 16:10\"").decode("utf-8")+"}")
df = pd.DataFrame(data).T.reset_index().rename(columns={"index":"items"})

df_all = pd.DataFrame()
for sort in r.keys("*"):
    s_date = sort.decode("utf-8")
    data_pre = json.loads("{"+r.get(s_date).decode("utf-8")+"}")
    df_pre = pd.DataFrame(data_pre).T.reset_index().rename(columns={"index":"items"})
    df_pre['datetime'] = s_date
    df_all = pd.concat([df_all, df_pre]).reset_index(drop=True)
print(df_all)