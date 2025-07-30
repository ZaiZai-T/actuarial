# reserve_chainladder.py
import pandas as pd
import numpy as np
from chainladder import Chainladder

def run_chainladder(triangle_csv_path):
    df = pd.read_csv(triangle_csv_path, index_col=0)
    cl = Chainladder().fit(df)
    full_triangle = cl.predict()
    return full_triangle
