import redis, math, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from custom_module import get_tools as getkrw


r=redis.Redis(host="localhost", port=6379, db=0)
data = json.loads("{"+r.get("\"datetime\":\"2023-05-31 23:05:00\"").decode("utf-8")+"}")
df = pd.DataFrame(data).T.reset_index().rename(columns={"index":"items"})
df_all = pd.DataFrame()

for sort in r.keys("*"):
    s_date = sort.decode("utf-8")
    data_pre = json.loads("{"+r.get(s_date).decode("utf-8")+"}")
    df_pre = pd.DataFrame(data_pre).T.reset_index().rename(columns={"index":"items"})
    df_pre['datetime'] = pd.to_datetime(s_date.replace("\"datetime\":","").replace("\"",""), format='%Y-%m-%d %H:%M:%S')
    df_all = pd.concat([df_all, df_pre]).reset_index(drop=True)

# for sort in r.keys("*"):
#     s_date = sort.decode("utf-8")
#     data_pre = json.loads("{"+r.get(s_date).decode("utf-8")+"}")
#     df_pre = pd.DataFrame(data_pre).T.reset_index().rename(columns={"index":"items"})
#     df_pre['datetime'] = getkrw.get_timestamp(int(s_date.replace("\"datetime\":","").replace("\"","")))
#     df_all = pd.concat([df_all, df_pre]).reset_index(drop=True)

# ts_me = pd.date_range(df_all['datetime'].min(), 
#                 periods=len(df_all['datetime'].unique()), 
#                 freq='H', 
#                 tz='Asia/Seoul')
# print(ts_me)
# df_all['Date_D'] = df_all['datetime'].dt.to_period(freq='D')
# df_all['Date_H'] = df_all['datetime'].dt.to_period(freq='H')
# df_all['Date_30T'] = df_all['datetime'].dt.to_period(freq='30T')


def making_bar_chart(target_column, target_item):
    target_item=target_item.split(',')
    df_target = df_all.set_index('items').loc[target_item,[target_column, 'datetime']]
    df_target[target_column] = df_target[target_column].map(lambda x: float(x))
    df_target['datetime'] = df_target['datetime'].map(lambda x: str(x).split(".")[0])
    df_target = df_target.sort_values('datetime', ascending=True).reset_index().set_index('datetime')
    # print(df_target)
    item = json.dumps(target_item)
    time = json.dumps(list(df_target.index.values))
    data={}
    for item_d in target_item:
        item_data= df_target[df_target['items']==item_d][target_column]
        i_min = item_data.min()
        i_max = item_data.max()
        print(type(i_min), type(i_max))
        item_data = item_data.map(lambda x: round((x - i_min)/(i_max-i_min),3)*100)
        print(item_data)
        data[item_d] = item_data.to_dict()
    print(item)
    data = json.dumps((data))
    return data, time, item

    # plt.figure(figsize=(12,3))
    # sns.lineplot(x='datetime', y=target_column, data=df_target)
    # plt.savefig('./static/line.png')
# data, time, item = making_bar_chart('closing_price', 'BTC,ETH')
# print(data)
# print(df_all.set_index('items').loc[['BTC','ETH'],['closing_price']])

def making_other_chart(target_column, target_item, df_all):
    target_item=target_item.split(',')
    df_target = df_all.set_index('items').loc[target_item,[target_column, 'datetime']]
    df_target[target_column] = df_target[target_column].map(lambda x: float(x))
    df_target['datetime'] = df_target['datetime'].map(lambda x: str(x).split(".")[0])
    df_target = df_target.sort_values('datetime', ascending=True).reset_index().set_index('datetime')
    # print(df_target)
    item = json.dumps(target_item)
    time = json.dumps(list(df_target.index.values))
    data={}
    for item_d in target_item:
        item_data= df_target[df_target['items']==item_d][target_column]
        i_min = item_data.min()
        i_max = item_data.max()
        print(type(i_min), type(i_max))
        item_data = item_data.map(lambda x: round((x - i_min)/(i_max-i_min),3)*100)
        print(item_data)
        data[item_d] = item_data.mean()
    data = json.dumps((data))
    return data, time, item

# print(making_other_chart('closing_price', 'BTC,ETH', df_all))


def making_treemap_chart(target_column, df_all):
    df_target = df_all.set_index('items').loc[:,[target_column, 'datetime']]
    df_target[target_column] = df_target[target_column].map(lambda x: float(x))
    df_target['datetime'] = df_target['datetime'].map(lambda x: str(x).split(".")[0])
    df_target = df_target.sort_values('datetime', ascending=True).reset_index().set_index('datetime')
    print(df_target)
    # print(df_target["items"].unique())
    item = list(df_target["items"].unique())
    data_all=[]
    for item_d in item:
        data={}
        item_data= df_target[df_target['items']==item_d][target_column]
        data["tree"] = round(item_data.mean(),3)
        data["label"] = item_d
        data_all.append(data)

    data = json.dumps((data_all))
    print(data)
    return data, item

# making_treemap_chart('closing_price', df_all)   

def making_detail_chart(df_all,date):
    # date="2023-06-02 13:00:00"
    columns = df_all.columns.to_list()[1:-1]
    items = list(df_all['items'].unique())
    target_df = df_all[df_all['datetime']==date]
    target_df.set_index('items', inplace=True)
    data_send = {}
    for col in columns:
        data_send[col]=target_df.loc[:,col].sort_values(ascending=False).head(5).to_dict()
    return data_send, columns

# print(making_detail_chart(df_all, "2023-06-02 13:00"))



# 변동가 / 변동률/ 거래량
# date="2023-06-02 13:00:00"
def making_bubble_chart(df_all):
    columns = ["items","units_traded_24H","acc_trade_value_24H","fluctate_rate_24H"]
    target_df = df_all[columns].set_index('items')
    target_df['acc_trade_value_24H'] = target_df['acc_trade_value_24H'].map(lambda x: round((float(x)),3))
    target_df['fluctate_rate_24H'] = target_df['fluctate_rate_24H'].map(lambda x: round((float(x)),3))
    target_df['units_traded_24H'] = target_df['units_traded_24H'].map(lambda x: round((float(x)),3))
    v24 = target_df['acc_trade_value_24H']
    r24 = target_df['fluctate_rate_24H']
    u24 = target_df['units_traded_24H']
    target_df['acc_trade_value_24H'] = target_df['acc_trade_value_24H'].map(lambda x: (x-v24.min())/(v24.max()-v24.min()))
    target_df['fluctate_rate_24H'] = target_df['fluctate_rate_24H'].map(lambda x: (x-r24.min())/(r24.max()-r24.min()))
    target_df['units_traded_24H'] = target_df['units_traded_24H'].map(lambda x: (x-u24.min())/(u24.max()-u24.min()))
    items = list(df_all['items'].unique())
    data_send = {}
    for item in items:
        trade_value=target_df.loc[item,'acc_trade_value_24H'].mean()
        trade_unit=target_df.loc[item,'units_traded_24H'].mean()
        flucate_rate=target_df.loc[item,'fluctate_rate_24H'].mean()
        data_send[item]={"x":round(trade_value,3),"y":round(trade_unit,3),"r":round(flucate_rate,3)}
    data_send = json.dumps(data_send)
    return data_send, columns, items  
print(making_bubble_chart(df_all))