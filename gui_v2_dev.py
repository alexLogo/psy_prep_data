import os
import tkinter as tk
from tkinter import filedialog

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # create a frame to hold the widgets
        self.frame = tk.Frame(self)
        self.frame.pack()

        # create a label to display the logo image
        self.logo_label = tk.Label(self.frame, image='logo.png')
        self.logo_label.pack()

        # create an entry for the base directory
        self.base_dir_entry = tk.Entry(self.frame)
        self.base_dir_entry.pack()

        # create a button to browse for the base directory
        self.browse_base_dir_button = tk.Button(self.frame, text='Browse for base directory', command=self.browse_base_dir)
        self.browse_base_dir_button.pack()

        # create an entry for the configuration file
        self.config_entry = tk.Entry(self.frame)
        self.config_entry.pack()

        # create a button to browse for the configuration file
        self.browse_config_button = tk.Button(self.frame, text='Browse for configuration file', command=self.browse_config_file)
        self.browse_config_button.pack()

        # create a button to combine the CSV files
        self.combine_button = tk.Button(self.frame, text='Combine CSV files', command=self.combine_csv_files)
        self.combine_button.pack()

    # define the browse_base_dir function
    def browse_base_dir(self):
        base_dir = filedialog.askdirectory()
        if base_dir:
            self.base_dir_entry.insert(0, base_dir)

    # define the browse_config_file function
    def browse_config_file(self):
        options = {'filetypes': [('Python files', '*.py')]}
        config_file = filedialog.askopenfilename(**options)
        if config_file:
            self.config_entry.insert(0, config_file)

    # define the combine_csv_files function
    def combine_csv_files(self):
        base_dir = self.base_dir_entry.get()
        
     # define the combine_csv_files function
    def combine_csv_files(self):
        base_dir = self.base_dir_entry.get()
        config_file = self.config_entry.get()
        if base_dir and config_file:
            # create an instance of the Runner class
            runner = Runner()

            # get the InputProcessor instance
            input_processor = runner.input_processor

            # combine the CSV files using the specified configuration file
            input_processor.combine_csv_files(base_dir, config_file)

            # read the results.csv file and get the column names
            with open(os.path.join(base_dir, 'results.csv'), 'r') as f:
                header = f.readline().strip().split(',')

            # display the column names in the GUI
            self.logo_label.configure(image='')
            self.logo_label.configure(text=', '.join(header))
        else:
            # show an error message if either the base directory or configuration file is missing
            self.show_error_message('Please enter a base directory and a configuration file')
