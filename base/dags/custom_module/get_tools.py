import requests, redis, json, time, math
import numpy as np
import pandas as pd

# r = redis.Redis(host=host, port=port, db=db)
# url = "https://api.bithumb.com/public/ticker/ALL_KRW"
# headers = {"accept": "application/json"}
# response = requests.get(url, headers=headers)
# json_data = response.json()['data']
# items_list = list(json_data.keys())[:-1]
# time_val=get_timestamp(math.floor(int(json_data["date"]))/1000)

def get_timestamp(time_val):
    return time.strftime("%Y-%m-%d %H:%M:00", time.localtime(time_val))

# def get_all_krw(host,port,db):
#     r = redis.Redis(host=host, port=port, db=db)
#     url = "https://api.bithumb.com/public/ticker/ALL_KRW"
#     headers = {"accept": "application/json"}
#     response = requests.get(url, headers=headers)
#     json_data = response.json()['data']
#     items_list = list(json_data.keys())[:-1]
#     time_val=math.floor(int(json_data["date"])/1000)
#     first_item = items_list[0]
#     last_item = items_list[-1]
#     r.set("\"datetime\":" + "\""+str(time_val)+ "\"", "\""+first_item+"\"" + ":" +json.dumps(json_data[first_item])+",\n")
#     for item in items_list[1:-1]:
#         item_data = json.dumps(json_data[item])
#         r.append("\"datetime\":" + "\""+str(time_val)+ "\"", "\""+item+"\"" + ":" +item_data+",\n")
#     r.append("\"datetime\":" + "\""+str(time_val)+ "\"", "\""+last_item+"\"" + ":" +json.dumps(json_data[last_item]))


def get_all_krw(host,port,db):
    r = redis.Redis(host=host, port=port, db=db)
    url = "https://api.bithumb.com/public/ticker/ALL_KRW"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    json_data = response.json()['data']
    items_list = list(json_data.keys())[:-1]
    time_val=get_timestamp(math.floor(int(json_data["date"]))/1000)
    first_item = items_list[0]
    last_item = items_list[-1]
    r.set("\"datetime\":" + "\""+time_val.replace("\"","")+ "\"", "\""+first_item+"\"" + ":" +json.dumps(json_data[first_item])+",\n")
    for item in items_list[1:-1]:
        item_data = json.dumps(json_data[item])
        r.append("\"datetime\":" + "\""+time_val.replace("\"","")+ "\"", "\""+item+"\"" + ":" +item_data+",\n")
    r.append("\"datetime\":" + "\""+time_val.replace("\"","")+ "\"", "\""+last_item+"\"" + ":" +json.dumps(json_data[last_item]))

def making_bar_chart(target_column, target_item, df_all):
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
        item_data = item_data.map(lambda x: round((x - i_min)/(i_max-i_min),3))
        print(item_data)
        data[item_d] = item_data.to_dict()
    print(item)
    data = json.dumps((data))
    return data, time, item

def get_redis_data(r):
    df_all = pd.DataFrame()
    for sort in r.keys("*"):
        s_date = sort.decode("utf-8")
        data_pre = json.loads("{"+r.get(s_date).decode("utf-8")+"}")
        df_pre = pd.DataFrame(data_pre).T.reset_index().rename(columns={"index":"items"})
        df_pre['datetime'] = pd.to_datetime(s_date.replace("\"datetime\":","").replace("\"",""), format='%Y-%m-%d %H:%M:%S')
        df_all = pd.concat([df_all, df_pre]).reset_index(drop=True)
    return df_all

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
        # i_min = item_data.min()
        # i_max = item_data.max()
        # print(type(i_min), type(i_max))
        # item_data = item_data.map(lambda x: round((x - i_min)/(i_max-i_min),3)*100)
        # print(item_data)
        data[item_d] = item_data.mean()
    data = json.dumps((data))
    return data, time, item

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

def making_detail_chart(df_all,date):
    # date="2023-06-02 13:00:00"
    columns = df_all.columns.to_list()[1:-1]
    items = df_all['items'].to_list()
    target_df = df_all[df_all['datetime']==date]
    target_df.set_index('items', inplace=True)
    data_send = {}
    for col in columns:
        data_send[col]=target_df.loc[:,col].sort_values(ascending=False).head(5).to_dict()
    return data_send, columns, items

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
        data_send[item]={"x":round(trade_value,3),"y":round(trade_unit,3),"r":round(flucate_rate,3)*50}
    data_send = json.dumps(data_send)
    return data_send, columns, items  
