import redis, math, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from custom_module import get_tools as getkrw
from flask import Flask, render_template, Response, request, session, redirect, url_for, make_response, jsonify


r=redis.Redis(host="localhost", port=6379, db=0)
df_all = pd.DataFrame()

for sort in r.keys("*"):
    s_date = sort.decode("utf-8")
    data_pre = json.loads("{"+r.get(s_date).decode("utf-8")+"}")
    df_pre = pd.DataFrame(data_pre).T.reset_index().rename(columns={"index":"items"})
    df_pre['datetime'] = pd.to_datetime(s_date.replace("\"datetime\":","").replace("\"",""), format='%Y-%m-%d %H:%M:%S')
    df_all = pd.concat([df_all, df_pre]).reset_index(drop=True)


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
        item_data = item_data.map(lambda x: round((x - i_min)/(i_max-i_min),3))
        print(item_data)
        data[item_d] = item_data.to_dict()
    print(item)
    data = json.dumps((data))
    return data, time, item


app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
@app.route("/")
def index():
    return render_template('linechart.html')

@app.route('/linechart', methods=['GET', 'POST'])
def drawing_chart():
    if request.method == 'POST':
        target_column = request.form['target_column']
        target_item = request.form['target_item']
        # print(target_column)
        # print(target_item)
        data, time, item = making_bar_chart(target_column, target_item)
        print(item)
        # print(time)
        return render_template('linechart.html',  target_data=data, target_time=time, target_item = item)
    else:
        return render_template('linechart.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7710)  