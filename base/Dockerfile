FROM apache/airflow:2.7.1
COPY ./dags/ \${AIRFLOW_HOME}/dags/
COPY ./requirements.txt \${AIRFLOW_HOME}/requirements.txt
RUN pip install -r \${AIRFLOW_HOME}/requirements.txt