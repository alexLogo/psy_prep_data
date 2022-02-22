# pathes
# generate path of to data directories, without dependency on out locaation
# relational data directories location should be fixed
import os
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw_data_path = os.path.join(base_dir , 'Data\\raw data\\')
raw_data_path = raw_data_path.replace(os.sep, '/')


# tracker data preprocessing configurations
tracker_file_name = "TrackersOutputData.csv"

# answers preprocessing configurations
answer_relevant_cols = ['QuestionResult']
answers_index = 'TrialNumber'
relevant_question = 88
answers_file_name = "Answers.csv"
answer_question_col_name = "QuestionID"

# trials preprocessing configurations
trial_question_col_name = "Question Number"
trial_index = "#trial number"
trial_relevant_cols = ['SensoMotoric Delay']
filter_training = -1
trials_file_name = ['UsedPlan/', 'trials']
trial_labels_dic = {0: 0, 0.033:1, 0.044:2, 0.066:3, 0.099:4, 0.154:5, 0.231:6, 0.352:7}


# reading files configuration
participant_dir_name = 'participant'