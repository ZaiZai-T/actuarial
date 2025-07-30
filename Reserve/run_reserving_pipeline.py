import os
import sys

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'create_table'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'triangle'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

# 导入各阶段模块
from run_cleaning import run_etl
from generate_triangle import run_triangle_generation
from mack_model import run_mack_model
from replace_claims_table import replace_claims_table

INPUT_PATH = 'output/cumulative_triangle.csv'
OUTPUT_PATH_LONG = 'output/mack_long.csv'
OUTPUT_PATH_TRI = 'output/cumulative_triangle1.csv'


def main():
    print("Step 0: Importing data ...")
    replace_claims_table()
    
    print("Step 1: Running ETL cleaning ...")
    run_etl()

    print("Step 2: Constructing triangle ...")
    run_triangle_generation()

    print("Step 3: Running Mack model ...")
    run_mack_model(INPUT_PATH, OUTPUT_PATH_LONG, OUTPUT_PATH_TRI)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
