#############################################################################################################
# Author - Elliot Ramsden
# Email - R016796k@student.staffs.ac.uk
# Last Modified - 19-03-24

# Description:
#
# Notes:
#
#############################################################################################################

# Import necessary classes from other files

import os
from datetime import datetime as dt


# Logging Object requires a current path, the way this is executed results in the programs root directory being the
# given path and thus the logs folder is only one child from that directory.

class Logging:
    def __init__(self, log_path):
        self.log_path = f"{log_path}/logs"
        self.error_log_file_full_path = None
        self.client_log_folder_name = ""

    # Adds an error message to the log file, uses \n to ensure the error is on a newline from any previous text.

    def add_error_to_log(self, error):
        if self.error_log_file_full_path is None:
            self.create_error_log_file()
        with open(self.error_log_file_full_path, "a+") as error_file:
            error_file.write(f"\n{error}")

    # Creates an error log file, this was inspired by another applications logging system, and thus it allows for
    # multiple logs to be created on the same day, the only difference is the ID at the end of the file.

    def create_error_log_file(self):
        os.makedirs(f"{self.log_path}/error_logs", exist_ok=True)
        current_date = dt.now().strftime("%d-%m-%Y")
        counter = 1
        error_file_name = f"{current_date}-{counter}.log"
        error_file_full_path = os.path.join(self.log_path, "error_logs", error_file_name)
        while os.path.exists(error_file_full_path):
            counter += 1
            error_file_name = f"{current_date}-{counter}.log"
            error_file_full_path = os.path.join(self.log_path, "error_logs", error_file_name)
        self.error_log_file_full_path = error_file_full_path
        with open(self.error_log_file_full_path, "w") as error_file:
            error_file.write(f"Logging has begun at {dt.now().strftime('%H:%M')}")
