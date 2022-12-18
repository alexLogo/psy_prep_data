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


gaze_right_loc = ['right_gaze_x', 'right_gaze_y']
gaze_left_loc = ['left_gaze_x', 'left_gaze_y']
gaze_right_vel = ['vel_right_gaze_x', 'vel_right_gaze_y']
gaze_left_vel = ['vel_left_gaze_x', 'vel_left_gaze_y']
gaze_right_acc = ['acc_right_gaze_x', 'acc_right_gaze_y']
gaze_left_acc = ['acc_left_gaze_x', 'acc_left_gaze_y']



def gaze_kinematics():
    for idx in cfg.subject_range:
        print(f'preprocessing participant {idx}')
        # read subject
        data = import_subject('base', idx)
        
        # add velocity_ts to right
        for i in [0,1]:
            data.create_new_ts(gaze_right_loc[i:i+1], gaze_right_vel[i], util.deravative)
            
        # add velocity_ts to left
        for i in [0,1]:
            data.create_new_ts(gaze_left_loc[i:i+1], gaze_left_vel[i], util.deravative)
         
        # add acceleration ts to right
        for i in [0,1]:
            data.create_new_ts(gaze_right_vel[i:i+1], gaze_right_acc[i], util.deravative)
            
        # add acceleration ts to left
        for i in [0,1]:
            data.create_new_ts(gaze_left_vel[i:i+1], gaze_left_acc[i], util.deravative)
  
                     
        # add total_velocity right
        data.create_new_ts(gaze_right_vel, 'total_vel_right', util.euclidian_combination)

        # add total_velocity left
        data.create_new_ts(gaze_left_vel, 'total_vel_left', util.euclidian_combination)
        
        # add total_velocity right
        data.create_new_ts(gaze_right_acc, 'total_acc_right', util.euclidian_combination)

        # add total_velocity left
        data.create_new_ts(gaze_left_acc, 'total_acc_left', util.euclidian_combination)

        
        # write subject 
        path = util.path_resolver('full kinematic', idx)
        data.to_csv(path)


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
    if cfg.pathes.trial_mode.startswith('pupil'):
        pupil_diameter_kinematics()
    elif cfg.pathes.trial_mode.startswith('gaze'):
        gaze_kinematics()
    else:
        hand_kinematics()
