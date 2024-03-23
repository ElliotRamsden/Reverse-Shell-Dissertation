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

import socket
import sys
import os
from src.connection_manager import ConnectionManager
from src.messages import Messages
from src.server_command_handler import ServerCommandHandler
from src.thread_handler import ThreadHandler
from src.logging import Logging


# Requires a ServerConfig instance to be passed to the server, creates a ConnectionManager object to store and manage
# client connections and also creates a ServerCommandHandler instance which is responsible for most of the user
# interaction to the program, it is where the menu options are handled.

class Server:
    def __init__(self, config):
        self.config = config
        self.socket = None
        self.logging = Logging(os.getcwd())
        self.connection_manager = ConnectionManager(self.logging)
        self.command_handler = ServerCommandHandler(self.connection_manager, self.shutdown, self.logging)
        self.thread_handler = ThreadHandler(self)
        self.messages = Messages()

    # Responsible cor creating the server socket and listening for connections, also displays a message to let the user
    # know which ip address and port number is listening for those connections.

    def initialize_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind((self.config.host, self.config.port))
            self.socket.listen(self.config.max_connections)
            print(self.messages.display_listening_for_connections_message(self.config.host, self.config.port))
        except socket.error as error:
            self.logging.add_error_to_log(error)
            self.shutdown(error="server_binding_error")

    # Starts the server socket and also starts the threads needed to listen for connections.

    def run(self):
        self.initialize_socket()
        self.thread_handler.initialize_threads()
        self.thread_handler.enqueue_tasks()

    # Displays a shutdown message and closes all connected clients sessions, also closes the actual server socket.
    # Program will also use sys.exit to ensure all threads are terminated and thus the program can easily be restarted.

    def shutdown(self, error=None):
        try:
            if error:
                print(self.messages.shutdown_message(error))
            else:
                print(self.messages.shutdown_message())
            self.connection_manager.close_all_connections()
            self.socket.close()
        except OSError as error:
            print(self.messages.display_errors("server_shutdown_error"))
            self.logging.add_error_to_log(error)
        finally:
            sys.exit(0)
