import os
import psycopg2
from dotenv import load_dotenv

# 加载 .env 文件中的数据库连接参数
load_dotenv()

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# 读取 SQL 文件
SQL_FILE_PATH = 'Reserve/sql/clean_raw_claims.sql'

def run_etl():
    try:
        # 建立数据库连接
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        print("✅ 成功连接数据库")

        # 读取 SQL 文件内容
        with open(SQL_FILE_PATH, 'r') as file:
            sql = file.read()

        # 执行 SQL
        cur.execute(sql)
        conn.commit()
        print("Succeed! ")

    except Exception as e:
        print("Failed: ", e)
    finally:
        cur.close()
        conn.close()
        print("Exit")

if __name__ == '__main__':
    run_etl()
