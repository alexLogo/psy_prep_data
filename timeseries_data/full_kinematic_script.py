import timeseries_data.configurations as cfg
import timeseries_data.util as util
from timeseries_data.Timeseries_Data import TimeseriesData
from timeseries_data.import_data import import_subject

location_names = ['Hand_loc_X', 'Hand_loc_Y', 'Hand_loc_Z']
velocity_names = ['Hand_vel_X', 'Hand_vel_Y', 'Hand_vel_Z']
acceleration_names = ['Hand_acc_X', 'Hand_acc_Y', 'Hand_acc_Z']


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
        
        # write subject 
        path = util.path_resolver('full kinematic', idx)
        data.to_csv(path)
        
