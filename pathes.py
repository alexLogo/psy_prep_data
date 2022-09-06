import os

dataset_mode = 'ophir'
data_mode = 'kinematic'
#data_mode = 'eyes'
#trial_mode = 'pupil_cut'
#trial_mode = 'gaze'
trial_mode = 'all-minimal'

data_type = 'all'
#features_type = 'comprehensive'
features_type = 'minimal'



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.join(base_dir , f'{dataset_mode}\\')
# create needed folder structure for data 
if not os.path.isdir(base_dir):
    os.mkdir(base_dir)
if not os.path.isdir(base_dir + "/Data"):
    os.mkdir(base_dir + "/Data")
if not os.path.isdir(base_dir + f"/Data/{data_mode}"):
    os.mkdir(base_dir + f"/Data/{data_mode}")

data_dir = os.path.join(base_dir , f'Data\\{data_mode}\\{trial_mode}\\')
data_dir = data_dir.replace(os.sep, '/')
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

raw_data_path = os.path.join(base_dir , 'Data\\raw data\\')
raw_data_path = raw_data_path.replace(os.sep, '/')
if not os.path.isdir(raw_data_path):
    os.mkdir(raw_data_path)

ts_data_path = os.path.join(data_dir , 'simple ts data\\')
ts_data_path = ts_data_path.replace(os.sep, '/')
if not os.path.isdir(ts_data_path):
    os.mkdir(ts_data_path)

full_kinematic_ts_data_path = os.path.join(data_dir , 'full kinematic ts data\\')
full_kinematic_ts_data_path = full_kinematic_ts_data_path.replace(os.sep, '/')
if not os.path.isdir(full_kinematic_ts_data_path):
    os.mkdir(full_kinematic_ts_data_path)

base_feature_path = os.path.join(data_dir , 'base feature data\\')
base_feature_path = base_feature_path.replace(os.sep, '/')
if not os.path.isdir(base_feature_path):
    os.mkdir(base_feature_path)


base_clean_feature_path = os.path.join(data_dir , 'clean base feature data\\')
base_clean_feature_path  = base_clean_feature_path .replace(os.sep, '/')
if not os.path.isdir(base_clean_feature_path):
    os.mkdir(base_clean_feature_path)


multicoll_1_feature_path = os.path.join(data_dir , 'multicollinearty 1 feature data\\')
multicoll_1_feature_path  = multicoll_1_feature_path .replace(os.sep, '/')
if not os.path.isdir(multicoll_1_feature_path):
    os.mkdir(multicoll_1_feature_path)

# num of subjects is num of files in the timeseries data directory minus 1 (the log file)
num_of_subjects = len(os.listdir(ts_data_path)) - 1


# create needed folder structure for results
if not os.path.isdir(base_dir + "/results"):
    os.mkdir(base_dir + "/results")
if not os.path.isdir(base_dir + "/results/classification"):
    os.mkdir(base_dir + "/results/classification")   
if not os.path.isdir(base_dir + f"/results/classification/{data_mode}"):
    os.mkdir(base_dir + f"/results/classification/{data_mode}")
if not os.path.isdir(base_dir + "/results/models"):
    os.mkdir(base_dir + "/results/models")
if not os.path.isdir(base_dir + f"/results/models/{data_mode}"):
    os.mkdir(base_dir + f"/results/models/{data_mode}")
if not os.path.isdir(base_dir + "/results/confusion matrix"):
    os.mkdir(base_dir + "/results/confusion matrix")
if not os.path.isdir(base_dir + f"/results/confusion matrix/{data_mode}"):
    os.mkdir(base_dir + f"/results/confusion matrix/{data_mode}")

    





result_path = os.path.join(base_dir , f'results\\classification\\{data_mode}\\{trial_mode}\\')
result_path = result_path.replace(os.sep, '/')
if not os.path.isdir(result_path):
    os.mkdir(result_path)


models_path = os.path.join(base_dir , f'results\\models\\{data_mode}\\{trial_mode}\\')
models_path = models_path.replace(os.sep, '/')
if not os.path.isdir(models_path):
    os.mkdir(models_path)


matrices_path = os.path.join(base_dir , f'results\\confusion matrix\\{data_mode}\\{trial_mode}\\')
matrices_path = matrices_path.replace(os.sep, '/')
if not os.path.isdir(matrices_path):
    os.mkdir(matrices_path)


sdt_path = os.path.join(base_dir , 'results\\meta\\')
sdt_path = sdt_path.replace(os.sep, '/')
if not os.path.isdir(sdt_path):
    os.mkdir(sdt_path)



# redundent
'''
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

base_kin_feature_path = os.path.join(data_dir , f'{data_type} {features_type} features\\')
base_kin_feature_path  = base_kin_feature_path .replace(os.sep, '/')

handcraft_features = os.path.join(base_dir, 'Data\\handcraft\\all\\' , 'features\\')
handcraft_features  = handcraft_features .replace(os.sep, '/')

result_base_clean_feature_path = os.path.join(base_dir , 'results\\classification\\base clean feature auc\\')
result_base_clean_feature_path = result_base_clean_feature_path.replace(os.sep, '/')


result_no_mult_feature_path = os.path.join(base_dir , 'results\\classification\\base clean feature auc\\')
result_no_mult_feature_path = result_no_mult_feature_path.replace(os.sep, '/')
'''

