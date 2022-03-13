import os

data_mode = 'handcraft'
trial_mode = 'all'


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


handcraft_features = os.path.join(data_dir , 'features\\')
handcraft_features  = handcraft_features .replace(os.sep, '/')

result_base_clean_feature_path = os.path.join(base_dir , 'results\\classification\\base clean feature auc\\')
result_base_clean_feature_path = result_base_clean_feature_path.replace(os.sep, '/')

