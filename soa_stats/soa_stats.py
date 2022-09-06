import pandas as pd
import numpy as np
from scipy import stats

import pathes
import timeseries_data.configurations as cfg
from feature_calculations.read_features import read_features

# this function gets subject header data and return sensitivity and bias measures
# after stanislaw & Todorov (1999) correction
def signal_detection(correct, manipulation):
    # manipulation array is 0 when manipulated and when when not
    to_hit = correct.astype(np.int8) + manipulation.astype(np.int8)
    
    # hit is trial where the subject was correct and there was no manipulation, 
    # meaning the to_hits array will be equal 2
    hits = np.sum(to_hit == 2)
    
    
    agency_trials = np.sum(manipulation)
    hit = (hits + .5)/(agency_trials + 1)
    
    # all trials stats
    # miss is trial where the subject was wrong and there was manipulation, meaning the to_hit array would be zero
    miss = np.sum(to_hit == 0)
    no_agency_trials = np.sum(manipulation == 0)
    #false_alarm = miss/no_response
    false_alarm = (miss + .5)/(no_agency_trials + 1)
    
    # all trials sdt
    hit_z = stats.norm.ppf(hit)
    fa_z = stats.norm.ppf(false_alarm)
    dprime = hit_z - fa_z
    criterion = -(hit_z + fa_z)/2
    
    
    
    return dprime, criterion


# this functions gets subject data and calculate the sensitivity (dprime) and the bias
def signal_detection_calculations(subject):
    value = 1
    
    manipulated = subject[subject[:,1] > 0]
    not_manipulated = subject[subject[:,1] == 0]
    
    fa = manipulated[manipulated[:,2] == 1]
    hits = not_manipulated[not_manipulated[:,2] == 1]
    
    hit_rate = (len(hits) + value/2) / (len(not_manipulated) + value)   
    fa_rate = (len(fa) + value/2) / (len(manipulated) + value)

    hit_z = stats.norm.ppf(hit_rate)
    fa_z = stats.norm.ppf(fa_rate)
    dprime = hit_z - fa_z
    criterion = -(hit_z + fa_z)/2
    
    return dprime, criterion
    
    
#this function gets subject data and return the general stats:
# agency rate, accuracy and sensitivity 
def subject_agency_statistics(subject_data):
    # take only the header part of the data
    header = subject_data[:, :cfg.header_size]
    
    #calculate the agency rate
    agency_rate = np.sum(header[:,2])
    agency_rate /= len(subject_data)
    
    # calculate accuracy
    manipulation = header[:,1] == 0
    correct = header[:,2] == manipulation
    accuracy_rate = np.sum(correct) / len(correct)
    
    dprime, criterion = signal_detection(correct, manipulation)
    
    return agency_rate, accuracy_rate, dprime, criterion

def filter_out(data, idx=1, exclude=[4]):
    data = data[~np.isin(data[:,idx], exclude)]
    return data


def accuracy_calculation(data):
    congruency = data[:,1] == 0
    
    correct = congruency == data[:,2]
    
    return sum(correct) / len(correct)
    

  
def subject_sensitivity_stats(subject_num, idx=-1,exclude=-1):
    results = []
    data = np.array(read_features(subject_num, mode='mult1'))
    
    if idx != -1:
        data = filter_out(data, idx=idx, exclude=exclude)
    
    dprime, criterion = signal_detection_calculations(data)
    accuracy = accuracy_calculation(data)
    
    # add results to results list
    results.append(dprime)
    results.append(criterion)
    results.append(accuracy)
    
    return results
 


def all_sensitivity_stats(idx=-1,exclude=-1):
    results = []
    for i in range(cfg.num_of_subjects):
        results.append(subject_sensitivity_stats(i+1, idx=idx,exclude=exclude))
    
    
    
    results = pd.DataFrame(results, columns=['dprime', 'bias', 'accuracy'])
    
    results.to_csv(pathes.sdt_path + "sensitivity_acc.csv", index=None)
    
    return results

 


x = all_sensitivity_stats()
