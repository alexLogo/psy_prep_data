import os
import pathes
# pathes
# generate path of to data directories, without dependency on out locaation
# relational data directories location should be fixed


# tracker data preprocessing configurations
tracker_file_name = "TrackersOutputData.csv"
relevant_rows_filter = [(3, "Room"), (4, "NoBlockView")]
unrelevant_trials = (-1, 0)
tracker_idx_col = 'idx'
tracker_relevant_data = [(1, tracker_idx_col), (6, 'timestamp'), (27, 'Hand_loc_X'), 
                         (28, 'Hand_loc_Y'), (29, 'Hand_loc_Z'),
                         ]
tracker_relevant_data_cols = [x[0] for x in tracker_relevant_data]
tracker_relevant_data_names = [x[1] for x in tracker_relevant_data]


# answers preprocessing configurations
answer_relevant_cols = ['QuestionResult']
answers_index = 'TrialNumber'
relevant_question = 88
answers_file_name = "Answers.csv"
answer_question_col_name = "QuestionID"

# trials preprocessing configurations
trial_question_col_name = "Question Number"
trial_index = "#trial number"
trial_relevant_cols = ['SensoMotoric Delay', 'angleChange']
filter_training = -1
trials_file_name = ['trials.csv']
trial_labels_dic = {(0,0): 0, (0.05,0): 1, (0.1,0):2, (0.15,0):3, (0,0.2126):4, (0,0.2867):5, (0,0.364):6}
part_of_movement = pathes.trial_mode

# for yoni:trial_labels_dic = {(0): 0, (0.033):1, (0.044):2, (0.066):3, (0.099):4, (0.154):5, (0.231):6, (0.352):7}


# reading files configuration
participant_dir_name = 'participant'
numbers_mode = 3




# filters
filter_column_of_interest = 'Hand_loc_Y'
filter_time_short = 600
filter_movement_short = 0.15
filter_movement_long = 0.65
filter_expected_low = 0.75
filter_expected_high = 0.94
min_reaching = .07
hesitation_threshold = 100
too_short_trial = 10

# interpolation
rate_hz = 11


# padding
padding_value = -10