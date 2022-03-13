import pandas as pd
from Raw_Data.tracker_data.read_trackers import read_tracker
from Raw_Data.tracker_data.filter_trials import filter_data, filter_short_trials
from Raw_Data.tracker_data.intepolate import data_interpolation
from Raw_Data.utils.timestamp_correction import timestamp_correction
from Raw_Data.utils.indices_of_interest import idx_of_return, idx_of_start, idx_of_back
import Raw_Data.configurations as cfg


def reset_index(data):
    for (_, df) in data:
        df.reset_index(inplace=True, drop=True)

    return data

def choose_relevent_parts(data, mode="all", ts_name='Hand_loc_Y'):
    # define filter function based on the chosen mode
    if mode == "all":
        fun = lambda x:x
    elif mode == "before":
        fun = lambda x:x.iloc[:idx_of_start(x[ts_name])]
    elif mode == "movement":
        fun = lambda x:x.iloc[idx_of_start(x[ts_name]):idx_of_back(x[ts_name])]
    elif mode == "reach":
        fun = lambda x:x.iloc[idx_of_start(x[ts_name]):idx_of_return(x[ts_name])]
    elif mode == "return":
        fun = lambda x:x.iloc[idx_of_return(x[ts_name]):idx_of_back(x[ts_name])]
    
    for i,(_, df) in enumerate(data): 
        data[i] = (data[i][0], fun(df))

    

    return data




def timestamp_to_ms(data):
    for (_, df) in data:
        df['timestamp'] = timestamp_correction(df['timestamp'])

    return data


def timestamp_from_zero(data):
    for (_, df) in data:
        zero = df['timestamp'].iat[0]
        df['timestamp'] = df['timestamp'] - zero

    return data
def tracker_preprocessing(subject_num):
    # read subject data
    data = read_tracker(subject_num)
    
    # reset dataframe index
    data = reset_index(data)
    
    # format timestamp in miliseconds
    data = timestamp_to_ms(data)
    
    # filter trials
    data = filter_data(data)
    
    # choose relevant part of the trial
    data = choose_relevent_parts(data, mode=cfg.part_of_movement)
    
    # filter trials with to little amount of data left
    data = filter_short_trials(data)
    
    # reset dataframe index
    data = reset_index(data)
    
    # start any trial's timestamp from zero
    data = timestamp_from_zero(data)
    
    # interpolate the data in order to hve even space between frames
    data = data_interpolation(data)
    
    
    return data 
data1 = tracker_preprocessing(7)