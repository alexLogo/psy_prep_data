from Raw_Data.utils.filters import *
import Raw_Data.configurations as cfg

# this function gets subject tracker data and a filtering function
# it filters the tracker data and return the number of filtered trials
# and returns movement data, the number of trials that where filtered
def filtering(data, filter_fun):
    # create a list of indices for filtering
    filter_lst = []
    
    for i, (_, trial) in enumerate(data):
        if filter_fun(trial):
            filter_lst.append(i)
    
    # save the number of those numbers 
    num_of_filtered = len(filter_lst)
    
    # delete them from kinematic array
    for i in sorted(filter_lst, reverse=True):
        del data[i]
    
    #print(filter_lst)
    return num_of_filtered



def filter_data(data):
    filtering_functions_hand = [filter_short_movement, 
                           filter_long_movement, filter_no_reach_movement,
                           filter_reach_hesitation]
    filtering_functions_pupil = []
    
    if False: #cfg.pathes.trial_mode == 'pupil':
        filtering_functions = filtering_functions_pupil
    else:
        filtering_functions = filtering_functions_hand
        
    filtered_trials = []
    
    for fun in filtering_functions:
        filtered = filtering(data, fun)
        filtered_trials.append(filtered)
        
    return data



def filter_short_trials(data):
    fun = lambda x:len(x) < cfg.too_short_trial
    filtered = filtering(data, fun)
    return data