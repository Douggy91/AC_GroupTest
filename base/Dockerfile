FROM apache/airflow
COPY ./dags/ \${AIRFLOW_HOME}/dags/
RUN python3 -m pip install -r requirements.txt
