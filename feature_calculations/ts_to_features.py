import pandas as pd
import tsfresh as ts
from tsfresh.utilities.dataframe_functions import impute

from timeseries_data.Timeseries_Data import TimeseriesData
from timeseries_data.import_data import import_subject


def to_ts_features(data):
    extracted_features = ts.extract_features(data, column_id="id")
    impute(extracted_features)
    return extracted_features 


# tranfrom each trial to suitable df for tsfresh
def ts_format(trial_data, idx):
    # tranfrom data into columns represenatation
    trial_data = trial_data.T
    
    # to DataFrame
    trial_df = pd.DataFrame(trial_data)
    
    # assign id value
    trial_df['id'] = idx
    
    return trial_df

# this function transfrom the timeseries data into dataframe in a format that suits the api of tsfresh
def construct_data_to_tsformat(data):
    # split each trial to different ts
    data = [data.get_all_ts(i) for i in range(len(data.data))]
    
    # build DataFrame in format that suits tsfresh
    data = [ts_format(trial, i) for i, trial in enumerate(data)]
    
    # concat all the dataframes together
    data = pd.concat(data, axis=0)
    
    return data



def participant_to_features(participant_num, mode='full kinematic'):
    # read timeseries data 
    subject_data = import_subject(mode, participant_num)
        
    ts_dataframe = construct_data_to_tsformat(subject_data)
    
    features_rep = to_ts_features(ts_dataframe)
    
    header = subject_data.get_all_header()
    header = pd.DataFrame(header)
    
    features_rep = pd.concat((header, features_rep), axis=1)
    
    return features_rep 
if __name__ == "__main__":
    x = participant_to_features(1)
