import numpy as np
import pandas as pd

from timeseries_data.Timeseries_Data import TimeseriesData
import timeseries_data.configurations as cfg
import timeseries_data.util as util
from timeseries_data.import_data import import_subject

location_names = ['Hand_loc_X', 'Hand_loc_Y', 'Hand_loc_Z']
velocity_names = ['Hand_vel_X', 'Hand_vel_Y', 'Hand_vel_Z']
acceleration_names = ['Hand_acc_X', 'Hand_acc_Y', 'Hand_acc_Z']


def calculate_hand_features(header, vel, acc):
    start = int(header[3])
    ret = int(header[4])
    back = int(header[5])
    
    # movement length
    length = back - start

    
    # reaching mean velocity
    reach_vel = vel[start:ret]
    mean_reach_vel = np.mean(reach_vel)


    # reching mean acceleration
    reach_acc = acc[start:ret]
    mean_reach_acc = np.mean(reach_acc)
    
    
    # back mean velocity
    back_vel = vel[ret:back]
    mean_back_vel = np.mean(back_vel)

    
    # back mean acceleration
    back_acc = acc[ret:back]
    mean_back_acc = np.mean(back_acc)

    
    return [length, mean_reach_vel, mean_reach_acc, mean_back_vel, mean_back_acc]



if __name__ == "__main__":
    for idx in cfg.subject_range:
        
        print(f'preprocessing participant {idx}')
        # read subject
        data = import_subject('base', idx)
        # add velocity_ts
        
        for i in [0,1,2]:
            data.create_new_ts(location_names[i:i+1], velocity_names[i], util.deravative)
            
        # add acceleration ts 
        for i in [0,1,2]:
            data.create_new_ts(velocity_names[i:i+1], acceleration_names[i], util.deravative)
            
        # add total_velocity
        data.create_new_ts(velocity_names, 'total_vel', util.euclidian_combination)
        
        # add acceleration
        data.create_new_ts(acceleration_names, 'total_acc', util.euclidian_combination)
        
        hand_features = np.zeros((len(data.data), 5))
        
        for i in range(len(data.data)):
            header = data.get_header(i)
            vel = data.get_ts(i, 'total_vel')
            acc = data.get_ts(i, 'total_acc')
            hand_features[i] = calculate_hand_features(header, vel, acc)
            
            
        hand_features = pd.DataFrame(hand_features) 
        header = data.get_all_header()[:, :3]
        
        data = np.concatenate((header, hand_features), axis=1)
        
        data = pd.DataFrame(data)
        # write subject 
        path = util.path_resolver('handcraft', idx)
        data.to_csv(path, index=None)
