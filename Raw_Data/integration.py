import pandas as pd
import numpy as np
from Raw_Data.answers.read_answers import read_answers
from Raw_Data.trials.read_trials import read_trials
from Raw_Data.tracker_data.tracker_preprocessing import tracker_preprocessing
from Raw_Data.utils.subject_threshold import threshold_filter
from timeseries_data.Timeseries_Data import TimeseriesData
import Raw_Data.configurations as cfg

def get_data(subject_num):
    trial_data = read_trials(subject_num)
    answer_data = read_answers(subject_num) 
    tracker_data = tracker_preprocessing(subject_num)
    
    return trial_data, answer_data, tracker_data


def matching_id(trial_data, answer_data, tracker_data):
    # calculate indices to delete from the tracker data
    to_delete = []
    for idx, _ in tracker_data:
        if idx not in trial_data.iloc[:,0].values or idx not in answer_data.iloc[:,0].values:
            to_delete.append(idx)
    
    # delete these indeices from the tracker data
    tracker_data = [x for x in tracker_data if x[0] not in to_delete]
    
    # calculate indices to preserve
    to_preserve = [x[0] for x in tracker_data]
    
    # delete indices from answers and trial data
    answer_data = answer_data[answer_data.iloc[:,0].isin(to_preserve)]
    trial_data = trial_data[trial_data.iloc[:,0].isin(to_preserve)]
    
    return trial_data, answer_data, tracker_data


def create_header(trial_data, answer_data):
    header = pd.concat((trial_data.iloc[:,1:], answer_data.iloc[:,1:]), axis=1)
    header.reset_index(inplace=True, drop=True)
    header.reset_index(inplace=True)
    
    return header, header.shape[1]
    

def df_to_representation(df, desired_length):
    pad_length = desired_length - df.shape[0]
    
    assert pad_length >= 0, "desired length should be longer the any DataFrame"
        
    
    data = df.to_numpy().T
    
    # padding
    data = np.pad(data, ((0, 0), (0, pad_length)), mode='constant', constant_values=cfg.padding_value)
    
    # flatting the data
    data = data.flatten()
    
    return data



def tracker_ts_parsing(tracker_data):
    # extract the length of the longest trial
    max_len = max(tracker_data, key=lambda x:x[1].shape[0])[1].shape[0]
    
    # extract the number of timeseries
    num_of_ts = tracker_data[0][1].shape[1]
    
    num_of_trials = len(tracker_data)
    
    ts_representation = np.zeros((num_of_trials, max_len*num_of_ts))
    
    for i, (_, df) in enumerate(tracker_data):
        row = df_to_representation(df, max_len)
        ts_representation[i] = row
        
    ts_representation = pd.DataFrame(ts_representation)
    
    return ts_representation, num_of_ts, tracker_data[0][1].columns.to_list()
    

def raw_data_integration(subject_num):
    # get data from different sources
    trial_data, answer_data, tracker_data = get_data(subject_num)
    
    # filter trials that dont exist in all files
    trial_data, answer_data, tracker_data = matching_id(trial_data, answer_data, tracker_data)
    
    # create the header part of the data table
    header, header_size = create_header(trial_data, answer_data)
    
    # check if this subject meet data quantity thresholds
    if threshold_filter(header):
         return -1
    
    # create the data part of the data table
    data, num_of_ts, ts_names = tracker_ts_parsing(tracker_data)
    
    # integrate
    integrated_data = pd.concat((header, data), axis=1)
    
    # create TimeseriesData object
    integrated_data = TimeseriesData(integrated_data, header_size, num_of_ts, ts_names)
    
    return integrated_data 

raw_data_integration(10)