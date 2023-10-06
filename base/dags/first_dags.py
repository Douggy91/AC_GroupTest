from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import sys     #custom module을 가져오기 위해 추가한 모듈


sys.path.append('/opt/airflow/dags/repo/base')




args = {'owner':'douglas kim'}
# owner는 해당 작업을 실행할 호스트 계정


with DAG(dag_id = 'get_bithumb_api',
    default_args=args,
    start_date=datetime(2023, 10, 6, 15, 25) ,
    schedule_interval='0 * * * *') as dag:

# start_date는 작업을 시작할 일자를 표시하여 
# 해당 시점부터 현재까지 실행하지 못한 작업이 있다면 해당 시간부터 데이터를 가져오는 개념
# schedul_interval은 crontab과 동일한 형식으로 작성

    get_bithumb_api_data = BashOperator(
        task_id='get_bithumb_api_data',
        depends_on_past=False,
        bash_command='/usr/bin/python3 /opt/airflow/dags/repo/base/dags/crawling_data.py',
        dag = dag)

    get_bithumb_api_data
# 사용할 task를 적어준다