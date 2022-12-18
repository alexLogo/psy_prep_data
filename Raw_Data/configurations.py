import os
import pathes
# pathes
# generate path of to data directories, without dependency on out locaation
# relational data directories location should be fixed

exclusion_list = [13, 24]

# tracker data preprocessing configurations
tracker_file_name = "TrackersOutputData.csv"
tracker_file_name_prefix = 'TrackersOutput'

relevant_rows_filter = [(3, "Room"), (4, "NoBlockView")]
unrelevant_trials = (-1, 0)
tracker_idx_col = 'idx'
to_drop = 0

if pathes.data_mode == "kinematic":
    tracker_relevant_data = [(1, tracker_idx_col), (6, 'timestamp'), (27, 'Hand_loc_X'), (28, 'Hand_loc_Y'), (29, 'Hand_loc_Z'),]
elif pathes.data_mode == "eyes" and pathes.trial_mode.startswith("pupil"):
    tracker_relevant_data = [(1, tracker_idx_col), (6, 'timestamp'), (29, 'Hand_loc_Z'),  
                             (49, 'right_pupil'), (50, 'left_pupil'),
                             ]
    to_drop = ['Hand_loc_Z']
elif pathes.data_mode == "eyes" and pathes.trial_mode.startswith("gaze"):
    tracker_relevant_data = [(1, tracker_idx_col), (6, 'timestamp'), 
                             (17, 'Headset_global_x'), (18, 'Headset_global_y'), (19, 'Headset_global_z'),
                             (24, 'Headset_euler_x'), (25, 'Headset_euler_y'), (26, 'Headset_euler_z'),
                             (29, 'Hand_loc_Z'),  
                             (49, 'right_pupil'), (50, 'left_pupil'), (51, 'right_open'), (52, 'right_open'),
                             (59, 'right_gaze_x'), (60, 'right_gaze_y'), (61, 'right_gaze_z'),
                             (62, 'left_gaze_x'), (63, 'left_gaze_y'), (64, 'left_gaze_z'),
                             ]
    # to_drop = ['Headset_global_x', 'Headset_global_y', 'Headset_global_z',
    #           'Headset_euler_x', 'Headset_euler_y', 'Headset_euler_z', 
    #           'Hand_loc_Z', 'right_pupil', 'left_pupil', 'right_open', 'right_open',
    #           'right_gaze_x', 'right_gaze_y', 'right_gaze_z', 'left_gaze_x','left_gaze_y','left_gaze_z']
  
else:
    pass
start_signal = 0
interpolate = True
# for hand: tracker_relevant_data = [(1, tracker_idx_col), (6, 'timestamp'), (27, 'Hand_loc_X'), (28, 'Hand_loc_Y'), (29, 'Hand_loc_Z'),]
# for pupil: tracker_relevant_data = [(1, tracker_idx_col), (6, 'timestamp'), (29, 'Hand_loc_Z'), (49, 'right_pupil'), (50, 'left_pupil'),]
    
tracker_relevant_data_cols = [x[0] for x in tracker_relevant_data]
tracker_relevant_data_names = [x[1] for x in tracker_relevant_data]



# answers preprocessing configurations
answer_relevant_cols = ['QuestionResult']
answers_index = 'TrialNumber'
relevant_question = 'Trial'
answers_file_name = "Answers.csv"
answer_question_col_name = "QuestionID"

# trials preprocessing configurations
trial_question_col_name = "line type"
trial_index = "#trial number"
trial_relevant_cols = ['setup task Number']
filter_training = -1
trials_file_name = ['trials.csv']
trial_labels_dic = {(60,): 0, (61,): 1, (62,):0, (63,):1}
part_of_movement = pathes.trial_mode
trials_file_name_prefix = 'trial'


# for asaf:trial_labels_dic = {(0,0): 0, (0.05,0): 1, (0.1,0):2, (0.15,0):3, (0,0.2126):4, (0,0.2867):5, (0,0.364):6}
# for yoni:trial_labels_dic = {(0): 0, (0.033):1, (0.044):2, (0.066):3, (0.099):4, (0.154):5, (0.231):6, (0.352):7}
# for ophir:trial_labels_dic = {(0,0): 0, (0.05,0): 1, (0.1,0):2, (0.15,0):3, (0.2,0):4}


# reading files configuration
participant_dir_name = 'Sub'
numbers_mode = 3

# chossing part conf
timestamp_col_name = 'timestamp'
window_start = 0
window_end = 300

# filters
filter_column_of_interest = 'Hand_loc_Z'
filter_time_short = 600
filter_movement_short = 0.15
filter_movement_long = 0.8
filter_expected_low = 0.75
filter_expected_high = 0.94
min_reaching = .1
hesitation_threshold = 100
too_short_trial = 10

# interpolation
rate_hz = 11


# padding
padding_value = -10


# subjects threshold
threshold = 20