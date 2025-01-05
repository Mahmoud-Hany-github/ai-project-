import sys
print("Python path:", sys.path)

from qlib import init
from qlib.data import D
from dateutil.relativedelta import relativedelta
import requests
import numpy as np
import pandas as pd

# Initialize QLib
init(provider_uri='~/.qlib/qlib_data/cn_data')

# Load data
try:
    data = D.features(['SH600000'], ['$close', '$volume'], start_time='2020-01-01', end_time='2021-01-01')
    print("Data loaded successfully!")
    print(data.head())
except Exception as e:
    print(f"Error: {e}")
