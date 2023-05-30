from custom_module import get_tools as getkrw
import redis 
from ast import literal_eval
import numpy as np
import pandas as pd
import math

# getkrw.get_all_krw("localhost", 6379, 0)
r=redis.Redis(host="localhost", port=6379, db=0)

data=literal_eval("{"+r.get("XYM").decode("utf-8")+"}")

data_all={}
for sort in r.keys("*"):
    data_all[sort.decode("utf-8")]=literal_eval("{"+r.get("XYM").decode("utf-8")+"}")

df = pd.DataFrame.from_dict(data).T
# index 용 시간설정
new_index = list(map(lambda x: getkrw.get_timestamp(math.floor(int(x)/1000)),df.index.tolist()))
df["time"]=new_index
print(df.reset_index(drop=True).set_index("time"))
