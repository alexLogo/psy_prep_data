import os
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ts_data_path = os.path.join(base_dir , 'Data\\simple ts data\\')
ts_data_path = ts_data_path.replace(os.sep, '/')

full_kinematic_ts_data_path = os.path.join(base_dir , 'Data\\full kinematic ts data\\')
full_kinematic_ts_data_path = full_kinematic_ts_data_path.replace(os.sep, '/')


# meta data
num_of_subjects = 24
subject_range = range(1, num_of_subjects+1)


# padding
padding_value = -10