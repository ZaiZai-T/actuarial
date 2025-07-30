import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# 自动获取本文件的上级路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE_PATH = os.path.join(CURRENT_DIR, "../sql/generate_paid_triangle.sql")

def run_triangle_generation():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        print("Connected to DB")
        sql = open(SQL_FILE_PATH).read()
        df = pd.read_sql(sql, conn)

        # Pivot 表格：accident_month 作为行，development_month 作为列
        triangle = df.pivot(index='accident_month', columns='development_month', values='incremental_paid')

        # 将 development_month 从列名变成整数，确保顺序正确
        triangle.columns = triangle.columns.astype(int)
        triangle = triangle.sort_index(axis=1)

        # 生成 cumulative triangle（按行累加）
        triangle_cumulative = triangle.cumsum(axis=1)

        # 输出保存到 CSV（可选）
        triangle_cumulative.to_csv('output/cumulative_triangle.csv')
        print("Succeed and Exported to CSV! ")

    except Exception as e:
        print("failed: ", e)
    finally:
        conn.close()

if __name__ == '__main__':
    run_triangle_generation()
