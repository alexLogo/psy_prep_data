import os
import pandas as pd
import numpy as np
from scipy import stats

from Raw_Data.answers.read_answers import read_answers
from Raw_Data.trials.read_trials import read_trials
import Raw_Data.configurations as cfg
from Raw_Data.utils.utils import extract_subject_number

def get_data(subject_num):
    trial_data = read_trials(subject_num)
    answer_data = read_answers(subject_num) 
    
    return trial_data, answer_data


# this functions gets subject data and calculate the sensitivity (dprime) and the bias
def signal_detection_calculations(subject):
    manipulated = subject[subject[:,0] == 0]
    not_manipulated = subject[subject[:,0] == 1]
    
    fa = manipulated[manipulated[:,1] == 1]
    hits = not_manipulated[not_manipulated[:,1] == 1]
    
    hit_rate = (len(hits) + 0.5) / (len(not_manipulated) + 1)   
    fa_rate = (len(fa) + 0.5) / (len(manipulated) + 1)

    hit_z = stats.norm.ppf(hit_rate)
    fa_z = stats.norm.ppf(fa_rate)
    dprime = hit_z - fa_z
    criterion = -(hit_z + fa_z)/2
    
    return dprime, criterion



def collect_data_integration(subject_num):
    # get data from different sources
    trial_data, answer_data = get_data(subject_num)
    
    merged_data = pd.merge(trial_data, answer_data, left_on=cfg.trial_index, right_on=cfg.answers_index)
    
    merged_data.iloc[:,1] = merged_data.iloc[:,1].apply(lambda x:x==0).astype(int)
    
    merged_data = merged_data.iloc[:,[1,3]]
    
    return np.array(merged_data)
    # filter trials that dont exist in all files
    #trial_data, answer_data, tracker_data = matching_id(trial_data, answer_data, tracker_data)


def subject_sdt(subject_num):
    subject_data = collect_data_integration(subject_num)
    dprime, criterion = signal_detection_calculations(subject_data)
    return dprime, criterion

if __name__ == "__main__":
    results = []
    for dir_name in os.listdir(cfg.pathes.raw_data_path):
        # checking if we are in a directory 
        path = os.path.join(cfg.pathes.raw_data_path, dir_name)
        if not os.path.isdir(path):
            continue
        
        # extract subject number
        subject_num = extract_subject_number(dir_name)
        print(subject_num)
        # get subject data
        dprime, criterion = subject_sdt(subject_num)
        
        results.append([dprime, criterion]) 
    
    results = pd.DataFrame(results)
    results.to_csv("sensitivity.csv", header=None, index=None)