import os

data_mode = 'kinematic'
trial_mode = 'all-minimal'

data_type = 'all'
#features_type = 'comprehensive'
features_type = 'minimal'

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir , f'Data\\{data_mode}\\{trial_mode}\\')


raw_data_path = os.path.join(base_dir , 'Data\\raw data\\')
raw_data_path = raw_data_path.replace(os.sep, '/')


ts_data_path = os.path.join(data_dir , 'simple ts data\\')
ts_data_path = ts_data_path.replace(os.sep, '/')


full_kinematic_ts_data_path = os.path.join(data_dir , 'full kinematic ts data\\')
full_kinematic_ts_data_path = full_kinematic_ts_data_path.replace(os.sep, '/')


base_feature_path = os.path.join(data_dir , 'base feature data\\')
base_feature_path = base_feature_path.replace(os.sep, '/')


base_clean_feature_path = os.path.join(data_dir , 'clean base feature data\\')
base_clean_feature_path  = base_clean_feature_path .replace(os.sep, '/')


base_kin_feature_path = os.path.join(data_dir , f'{data_type} {features_type} features\\')
base_kin_feature_path  = base_kin_feature_path .replace(os.sep, '/')


multicoll_1_feature_path = os.path.join(data_dir , 'multicollinearty 1 feature data\\')
multicoll_1_feature_path  = multicoll_1_feature_path .replace(os.sep, '/')


multicoll_2_feature_path = os.path.join(data_dir , 'multicollinearty 2 feature data\\')
multicoll_2_feature_path  = multicoll_2_feature_path .replace(os.sep, '/')


multicoll_3_feature_path = os.path.join(data_dir , 'multicollinearty 3 feature data\\')
multicoll_3_feature_path  = multicoll_3_feature_path .replace(os.sep, '/')


multicoll_4_feature_path = os.path.join(data_dir , 'multicollinearty 4 feature data\\')
multicoll_4_feature_path  = multicoll_4_feature_path .replace(os.sep, '/')


multicoll_5_feature_path = os.path.join(data_dir , 'multicollinearty 5 feature data\\')
multicoll_5_feature_path  = multicoll_5_feature_path .replace(os.sep, '/')

multicoll_6_feature_path = os.path.join(data_dir , 'multicollinearty 6 feature data\\')
multicoll_6_feature_path  = multicoll_6_feature_path .replace(os.sep, '/')


multicoll_7_feature_path = os.path.join(data_dir , 'multicollinearty 7 feature data\\')
multicoll_7_feature_path  = multicoll_7_feature_path .replace(os.sep, '/')



handcraft_features = os.path.join(base_dir, 'Data\\handcraft\\all\\' , 'features\\')
handcraft_features  = handcraft_features .replace(os.sep, '/')


result_path = os.path.join(base_dir , f'results\\classification\\{data_mode}\\{trial_mode}\\')
result_path = result_path.replace(os.sep, '/')


result_base_clean_feature_path = os.path.join(base_dir , 'results\\classification\\base clean feature auc\\')
result_base_clean_feature_path = result_base_clean_feature_path.replace(os.sep, '/')


result_no_mult_feature_path = os.path.join(base_dir , 'results\\classification\\base clean feature auc\\')
result_no_mult_feature_path = result_no_mult_feature_path.replace(os.sep, '/')

models_path = os.path.join(base_dir , f'results\\models\\{data_mode}\\{trial_mode}\\')
models_path = models_path.replace(os.sep, '/')
