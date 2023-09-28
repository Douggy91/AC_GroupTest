import redis, math, json
import numpy as np
import pandas as pd
from custom_module import get_tools as getkrw
from flask import Flask, render_template, Response, request, session, redirect, url_for, make_response, jsonify


r=redis.Redis(host="localhost", port=6379, db=0)
df_all = getkrw.get_redis_data(r)
try:
    tt = df_all['datetime'].sort_values(ascending=False).unique()[:20]
    df_all = df_all[df_all['datetime'].isin(tt)]
except:
    print("아직 데이터가 없습니다.")
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
        target_chart = request.form['target_chart']
        if (target_chart == 'line') or( target_chart == 'bar'):
            try:
                data, time, item = getkrw.making_bar_chart(target_column, target_item, df_all)
                return render_template('linechart.html',  target_data=data, target_time=time, target_item = item, target_chart = json.dumps(target_chart))
            except Exception as e:
                print(e)
                return render_template('linechart.html',  target_data=[], target_time=[], target_item = [], target_chart = [], message = "종목을 찾을 수 없습니다. \n종목은 대문자로 공백없이 입력해주세요.")
        elif (target_chart == 'doughnut') or (target_chart == 'polarArea'):
            try:
                data, time, item = getkrw.making_other_chart(target_column, target_item, df_all)
                return render_template('otherchart.html',  target_data=data, target_time=time, target_item = item, target_chart = json.dumps(target_chart))
            except Exception as e:
                            print(e)
                            return render_template('otherchart.html',  target_data=[], target_time=[], target_item = [], target_chart = [], message = "종목을 찾을 수 없습니다. \n종목은 대문자로 공백없이 입력해주세요.")
    else:
        return render_template('linechart.html')

@app.route('/chart_treemap', methods=['GET', 'POST'])
def chart_treemap():
    if request.method == 'POST':
        target_column = request.form['target_column']
        try:
            data, item = getkrw.making_treemap_chart(target_column, df_all)
            return render_template('treemap.html', target_data=data, target_item = item)
        except Exception as e:
            print(e)
            return render_template('treemap.html', target_data=[], target_item = [], message = "종목을 찾을 수 없습니다. \n종목은 대문자로 공백없이 입력해주세요.")
    else:
        return render_template('treemap.html')

@app.route('/bubble_chart', methods=['GET', 'POST'])
def draw_bubble_chart():
    try:
        data, columns, items = getkrw.making_bubble_chart(df_all)
        return render_template('bubble_chart.html', target_data=data, target_column=columns, target_item=items)
    except Exception as e:
            print(e)
            return render_template('bubble_chart.html', target_data=[], message = "종목을 을 수 없습니다. \n종목은 대문자로 공백없이 입력해주세요.")        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7710, debug=True)  
