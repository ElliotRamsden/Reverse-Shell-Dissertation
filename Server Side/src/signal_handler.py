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

import signal


# Takes a server parameter as this is needed to perform its main role.

class SignalHandler:
    def __init__(self, server):
        self.server = server

    # In the event the user presses Ctrl C the program will execute a function called handle shutdown.

    def register_signals(self):
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    # This function executes the server.shutdown method which will close everything down gracefully and without error.

    def handle_shutdown(self, signum, frame):
        self.server.shutdown()
