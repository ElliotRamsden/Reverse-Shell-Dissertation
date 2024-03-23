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

import yaml
import os


# This is used by the Server class to create its socket, values are pulled from the config.yml file

class ServerConfig:
    def __init__(self):
        self.config_file = self.get_config_file()
        self.host = self.config_file["Config"]["ServerAddress"]
        self.port = self.config_file["Config"]["ServerPort"]
        self.max_connections = self.config_file["Config"]["MaximumConnections"]

    # Gets the path of the config.yml file, if it does not exist then one is created and given default values that
    # must be changed before starting the server for the first time.

    @staticmethod
    def get_config_file():
        config_folder = f"{os.getcwd()}/configs"
        os.makedirs(f"{config_folder}", exist_ok=True)
        config_file = f"{config_folder}/config.yml"
        if os.path.exists(config_file):
            with open(config_file, "r") as config_file:
                config_contents = yaml.safe_load(config_file)
            return config_contents
        else:
            config_contents = {
                "Config": {
                    "ServerAddress": "CHANGE_ME",
                    "ServerPort": 1234,
                    "MaximumConnections": 100
                }
            }
            with open(f"{config_folder}/config.yml", "w") as config_file:
                yaml.dump(config_contents, config_file, default_flow_style=False)
            return config_contents
