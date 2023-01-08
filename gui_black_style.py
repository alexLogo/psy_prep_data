import configparser
import logging
import tkinter as tk
from tkinter import filedialog

from mdt import MDT

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Set up the main window
root = tk.Tk()
root.title("Configuration Manager")
root.geometry("600x600")

# Create the MDT theme
theme = MDT(root)

# Create a frame to hold the input widgets
input_frame = tk.Frame(root)

# Create the input widgets
exclusion_list_label = tk.Label(input_frame, text="Exclusion list:")
exclusion_list_entry = tk.Entry(input_frame)
tracker_file_name_label = tk.Label(input_frame, text="Tracker file name:")
tracker_file_name_entry = tk.Entry(input_frame)
tracker_file_name_prefix_label = tk.Label(
    input_frame, text="Tracker file name prefix:"
)
tracker_file_name_prefix_entry = tk.Entry(input_frame)
relevant_rows_filter_label = tk.Label(input_frame, text="Relevant rows filter type:")
relevant_rows_filter_entry = tk.Entry(input_frame)
unrelevant_trials_label = tk.Label(input_frame, text="Unrelevant trials:")
unrelevant_trials_checkbox = tk.Checkbutton(input_frame)
tracker_idx_col_label = tk.Label(input_frame, text="Tracker index column:")
tracker_idx_col_entry = tk.Entry(input_frame)
to_drop_label = tk.Label(input_frame, text="Columns to drop:")
to_drop_entry = tk.Entry(input_frame)
answer_relevant_cols_label = tk.Label(input_frame, text="Answer relevant columns:")
answer_relevant_cols_entry = tk.Entry(input_frame)
answers_index_label = tk.Label(input_frame, text="Answers index:")
answers_index_entry = tk.Entry(input_frame)
relevant_question_label = tk.Label(input_frame, text="Relevant question:")
relevant_question_entry = tk.Entry(input_frame)
answers_file_name_label = tk.Label(input_frame, text="Answers file name:")
answers_file_name_entry = tk.Entry(input_frame)
answer_question_col_name_label = tk.Label(
    input_frame, text="Answer question column name:"
)
answer_question_col_name_entry = tk.Entry(input_frame)

# Continue creating the "Browse" buttons and the "Save" button
trials_file_location_button = tk.Button(input_frame, text="Browse", command=browse_trials_file)
trackers_output_data_file_location_button = tk.Button(
    input_frame, text="Browse", command=browse_trackers_output_data_file
)
reporter_file_location_button = tk.Button(
    input_frame, text="Browse", command=browse_reporter_file
)
save_button = tk.Button(input_frame, text="Save", command=save_config)

# Pack the widgets into the input frame
exclusion_list_label.pack()
exclusion_list_entry.pack()
tracker_file_name_label.pack()
tracker_file_name_entry.pack()
tracker_file_name_prefix_label.pack()
tracker_file_name_prefix_entry.pack()
relevant_rows_filter_label.pack()
relevant_rows_filter_entry.pack()
unrelevant_trials_label.pack()
unrelevant_trials_checkbox.pack()
tracker_idx_col_label.pack()
tracker_idx_col_entry.pack()
to_drop_label.pack()
to_drop_entry.pack()
answer_relevant_cols_label.pack()
answer_relevant_cols_entry.pack()
answers_index_label.pack()
answers_index_entry.pack()
relevant_question_label.pack()
relevant_question_entry.pack()
answers_file_name_label.pack()
answers_file_name_entry.pack()
answer_question_col_name_label.pack()
answer_question_col_name_entry.pack()
answers_file_location_button.pack()
trials_file_location_button.pack()
trackers_output_data_file_location_button.pack()
reporter_file_location_button.pack()
save_button.pack()

# Set up the functions to be called when the "Browse" buttons are clicked
def browse_answers_file():
    global answers_file_location
    answers_file_location = filedialog.askopenfilename(
        initialdir="/", title="Select answers file", filetypes=(("CSV files", "*.csv"),)
    )


def browse_trials_file():
    global trials_file_location
    trials_file_location = filedialog.askopenfilename(
        initialdir="/", title="Select trials file", filetypes=(("CSV files", "*.csv"),)
    )


def browse_trackers_output_data_file():
    global trackers_output_data_file_location
    trackers_output_data_file_location = filedialog.askopenfilename(
        initialdir="/",
        title="Select trackers output data file",
        filetypes=(("CSV files", "*.csv"),),
    )


def browse_reporter_file():
    global reporter_file_location
    reporter_file_location = filedialog.askopenfilename(
        initialdir="/", title="Select reporter file", filetypes=(("CSV files", "*.csv"),)
    )


# Set up the function to be called when the "Save" button is clicked
def save_config():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "exclusion_list": exclusion_list_entry.get(),
        "tracker_file_name": tracker_file_name_entry.get(),
        "tracker_file_name_prefix": tracker_file_name_prefix_entry.get(),
        "relevant_rows_filter": relevant_rows_filter_entry.get(),
        "unrelevant_trials": str(unrelevant_trials_checkbox.get()),
        "tracker_idx_col": tracker_idx_col_entry.get(),
        "to_drop": to_drop_entry.get(),
        "answer_relevant_cols": answer_relevant_cols_entry.get(),
        "answers_index": answers_index_entry.get(),
        "relevant_question": relevant_question_entry.get(),
        "answers_file_name": answers_file_name_entry.get(),
        "answer_question_col_name": answer_question_col_name_entry.get(),
        "Answers_file_Location": answers_file_location,
        "Trails_file_location": trials_file_location,
        "TrackersOutputData_file_location": trackers_output_data_file_location,
        "Reporter_file_location": reporter_file_location,
    }
    try:
        with open("config.ini", "w") as configfile:
            config.write(configfile)
    except Exception as e:
        logging.exception("Error saving config file")

# Pack the input frame into the main window
input_frame.pack()

# Run the main loop
root.mainloop()

