import os
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base_feature_path = os.path.join(base_dir , 'Data\\base feature data\\')
base_feature_path = base_feature_path.replace(os.sep, '/')

full_kinematic_ts_data_path = os.path.join(base_dir , 'Data\\full kinematic ts data\\')
full_kinematic_ts_data_path = full_kinematic_ts_data_path.replace(os.sep, '/')


# meta data
num_of_subjects = 23
subject_range = range(1, num_of_subjects+1)
