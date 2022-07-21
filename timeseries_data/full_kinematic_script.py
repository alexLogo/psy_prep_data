import timeseries_data.configurations as cfg
import timeseries_data.util as util
from timeseries_data.Timeseries_Data import TimeseriesData
from timeseries_data.import_data import import_subject

hand_location_names = ['Hand_loc_X', 'Hand_loc_Y', 'Hand_loc_Z']
hand_velocity_names = ['Hand_vel_X', 'Hand_vel_Y', 'Hand_vel_Z']
hand_acceleration_names = ['Hand_acc_X', 'Hand_acc_Y', 'Hand_acc_Z']


pupil_size_names = ['right_pupil', 'left_pupil']
pupil_velocity_names = ['right_vel', 'left_vel']
pupil_acceleration_names = ['right_acc', 'left_acc']



def hand_kinematics():
    for idx in cfg.subject_range:
        print(f'preprocessing participant {idx}')
        # read subject
        data = import_subject('base', idx)
        
        # add velocity_ts
        for i in [0,1,2]:
            data.create_new_ts(hand_location_names[i:i+1], hand_velocity_names[i], util.deravative)
            
        # add acceleration ts 
        for i in [0,1,2]:
            data.create_new_ts(hand_velocity_names[i:i+1], hand_acceleration_names[i], util.deravative)
            
        # add total_velocity
        data.create_new_ts(hand_velocity_names, 'total_vel', util.euclidian_combination)
        
        # add acceleration
        data.create_new_ts(hand_acceleration_names, 'total_acc', util.euclidian_combination)
        
        # write subject 
        path = util.path_resolver('full kinematic', idx)
        data.to_csv(path)

def pupil_diameter_kinematics():
    for idx in cfg.subject_range:
        print(f'preprocessing participant {idx}')
        # read subject
        data = import_subject('base', idx)
        
        # add velocity_ts
        for i in [0,1]:
            data.create_new_ts(pupil_size_names[i:i+1], pupil_velocity_names[i], util.deravative)
            
        # add acceleration ts 
        for i in [0,1]:
            data.create_new_ts(pupil_velocity_names[i:i+1], pupil_acceleration_names[i], util.deravative)
                    
        # write subject 
        path = util.path_resolver('full kinematic', idx)
        data.to_csv(path)



if __name__ == "__main__":
    if cfg.cfg.pathes.trial_mode.startswith('pupil'):
        pupil_diameter_kinematics()
    else:
        hand_kinematics()
