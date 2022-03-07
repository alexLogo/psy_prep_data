import pandas as pd
import numpy as np
from Raw_Data.tracker_data.read_trackers import read_tracker
import matplotlib.pyplot as plt
def calculate_time(df):
    ts = df['timestamp']
    start = ts.iat[0]
    end = ts.iat[-1]
    return end - start

def ts_diff(df):
    ts = df['timestamp']
    diff = ts.diff()
    return diff.iloc[1:].tolist()

idx = 14
len_list = []
diff_list = []
data = read_tracker(idx)
for x in data:
    len_list.append(calculate_time(x[1]))
    diff_list += ts_diff(x[1])
plt.hist(diff_list, bins=10)