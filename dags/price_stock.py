from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta, date
import pandas as pd
import json
from urllib.request import Request, urlopen
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.postgres_hook import PostgresHook


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to get and store stock data
def craw_stock_price(**kwargs):
    to_date = kwargs["to_date"]
    from_date = "2020-01-01"

    stock_code = "VNM,VCB,VIC,BID,SSI,PNJ,HPG,GAS,MWG,VJC"

    url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:{}~date:gte:{}~date:lte:{}&size=9990&page=1".format(stock_code, from_date, to_date)
    print(url)

    req = Request(url, headers={'User-Agent': 'Mozilla / 5.0 (Windows NT 6.1; WOW64; rv: 12.0) Gecko / 20100101 Firefox / 12.0'})
    x = urlopen(req, timeout=10).read()

    json_x = json.loads(x)['data']

    stock_price_data = []  

    for stock in json_x:
        stock_price_data.append(stock)

    stock_price_df = pd.DataFrame(stock_price_data) 

    return stock_price_df

def create_table_and_insert(**kwargs):
    stock_price_df = kwargs["task_instance"].xcom_pull(task_ids="crawl_stock_price_task")

    try:
        # Create a PostgresHook to connect to the database
        hook = PostgresHook(postgres_conn_id='postgres_localhost')
        
        # SQL query to create the table if not exists
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS stock_price (
                code VARCHAR(50),
                date DATE,
                time TIME,
                floor VARCHAR(50),
                type VARCHAR(50),
                basicPrice FLOAT,
                ceilingPrice FLOAT,
                floorPrice FLOAT,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                average FLOAT,
                adOpen FLOAT,
                adHigh FLOAT,
                adLow FLOAT,
                adClose FLOAT,
                adAverage FLOAT,
                nmVolume FLOAT,
                nmValue FLOAT,
                ptVolume FLOAT,
                ptValue FLOAT,
                change FLOAT,
                adChange FLOAT,
                pctChange FLOAT
            );
        """

        # Execute the SQL query
        hook.run(create_table_sql)

        print("Bảng stock_price đã được tạo")

        # Kiểm tra xem dữ liệu đã tồn tại trong bảng chưa
        existing_data_sql = "SELECT MAX(date) FROM stock_price"
        max_date = hook.get_first(existing_data_sql)
        max_date = max_date[0] if max_date else None
        # Trước khi so sánh, chuyển đổi max_date từ datetime.date sang chuỗi
        if max_date:
            max_date_str = max_date.strftime("%Y-%m-%d")

        # Chỉ chọn dữ liệu mới hơn ngày cuối cùng trong cơ sở dữ liệu
        if max_date:
            stock_price_df = stock_price_df[stock_price_df['date'] > max_date_str]
        # Chuyển đổi DataFrame thành danh sách tuple
        data_values = stock_price_df.to_dict('records')

        # SQL query để chèn dữ liệu vào bảng
        insert_sql = """
            INSERT INTO stock_price
            (code, date, time, floor, type, basicPrice, ceilingPrice, floorPrice, open, high, low, close, average, adOpen, adHigh, adLow, adClose, adAverage, nmVolume, nmValue, ptVolume, ptValue, change, adChange, pctChange)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_values = stock_price_df.to_numpy().tolist()
        # Thực thi câu lệnh SQL với dữ liệu
        if data_values:
            hook.insert_rows(table="stock_price", rows=data_values)
            print("Dữ liệu đã được chèn thành công vào bảng.")
        else:
            print("Không có dữ liệu nào để chèn vào bảng.")
    except Exception as e:
        print(f"Lỗi khi tạo bảng hoặc chèn dữ liệu vào PostgreSQL: {e}")
        


# Define the DAG
with DAG('crawl_stock_data', 
         default_args=default_args,
         schedule_interval='0 0 * * *',  # Daily at midnight
         ) as dag:

    # Task to create the table


    crawl_stock_price_task = PythonOperator(
        task_id='crawl_stock_price_task',
        python_callable=craw_stock_price,
        op_kwargs={'to_date': "2024-12-31"},
        provide_context=True,
    )

    create_table_and_insert_task = PythonOperator(
        task_id='create_table_and_insert_task',
        python_callable=create_table_and_insert,
        provide_context=True,
    )
    


crawl_stock_price_task >> create_table_and_insert_task 
