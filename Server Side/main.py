#############################################################################################################
# Author - Elliot Ramsden
# Email - R016796k@student.staffs.ac.uk
# Date Created - 02-02-24
# Last Modified -
# Version - 1.0.0
# License - GPLv3

# Description:
#   This program is the server side code for the Reverse Shell that I have created as part of my FYP,
#   this does not need to be running before client side code as the clients will join as soon as the server
#   becomes available.
#
# Notes:
#   This was created based of the following GitHub repository: https://github.com/buckyroberts/Turtle
#   As such there may be some similarity in parts of the code, but this is a much more refined, modular
#   and readable version with additional functionality that the original does not have.
#
# Change Log:
#
# Known Issues:
#
#############################################################################################################

# Import necessary classes from other files

from src.server import Server
from src.server_config import ServerConfig
from src.signal_handler import SignalHandler

# Main function of the program where the server is created and started


def main():
    config = ServerConfig()
    server = Server(config)
    signal_handler = SignalHandler(server)
    signal_handler.register_signals()
    server.run()


# Calls the main function and actually runs the program

if __name__ == "__main__":
    main()
