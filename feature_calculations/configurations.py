import pathes
# meta data
num_of_subjects = pathes.num_of_subjects
participants_range = range(1, num_of_subjects+1)

subjects_for_multi_calculation = num_of_subjects
minimum_unnan = 2




loc_range = range(3)
vel_range = range(3,7)
acc_range = range(7,11)
full_range = range(11)
pupil_range = range(6)

if pathes.data_type == 'location':    
    current_range = loc_range
elif pathes.data_type == 'velocity':    
    current_range = vel_range 
elif pathes.data_type == 'acceleration':    
    current_range = acc_range
elif pathes.trial_mode == 'pupil' or pathes.trial_mode == 'pupil_cut':
    current_range = pupil_range
else:
    current_range = full_range
    
    
    
# deprecated
'''
filtering_base = ['clean', 'mult1', 'mult2', 'mult3', 'mult4', 'mult5', 'mult6']
filtering_to_path = [pathes.multicoll_1_feature_path, pathes.multicoll_2_feature_path,
                     pathes.multicoll_3_feature_path, pathes.multicoll_4_feature_path,
                     pathes.multicoll_5_feature_path, pathes.multicoll_6_feature_path,
                     pathes.multicoll_7_feature_path]
'''