FROM python:3.9.11
FROM apache/airflow:2.8.2
RUN pip install apache-airflow==${AIRFLOW_VERSION}
RUN pip install superset
# RUN pip install --user apache-superset


