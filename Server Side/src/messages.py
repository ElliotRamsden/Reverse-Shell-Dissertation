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
import yaml
from typing import Dict, Any


# Can be called without needing a Messages class and simply clears the terminal on all OS

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


# PyYAMl doesn't format the config the way I like when the dictionary is dumped into the file,
# this class fixes that by using the | option to denote multi line strings.

class CustomYamlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentation=False):
        return super(CustomYamlDumper, self).increase_indent(flow, False)


def multiline_string_presenter(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    else:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, multiline_string_presenter, Dumper=CustomYamlDumper)


# Messages class stores many functions that mostly just return formatted versions of messages stored in the lang.yml.

class Messages:
    def __init__(self):
        # Dict[str, Any] isn't required but removes a linter warning in pycharm (The warning is a false positive).
        self.messages_file: Dict[str, Any] = self.get_messages_file()
        self.separator_amount = self.messages_file["MessageConfig"]["SeperatorCount"]
        self.view_page_amount = self.messages_file["MessageConfig"]["ClientsPerListPage"]

    # Uses lang.yml settings to create a seperator for between messages.

    def _display_separator(self):
        return f"{(self.messages_file['MessageConfig']['SeperatorCharacter']) * self.separator_amount}"

    # Displays the message with a seperator above and below, with the option of having another message below the second
    # seperator that is displayed.

    def _display_header_and_footer(self, header_content, footer_content=''):
        return f"{self._display_separator()}\n{header_content}\n{self._display_separator()}{footer_content}"

    # Displays the message with only one seperator above it.

    def _display_header_only(self, header_content):
        return f"{self._display_separator()}\n{header_content}"

    # Displays the Artefact information, my name, student number, what the program is for.

    def display_artefact_information(self):
        artefact_info = self.messages_file["Messages"]["Headers"]["Artefact-Information"]
        return self._display_header_and_footer(artefact_info)

    # Displays the select title, e.g. when a user enters 1 or select at the main menu.

    def display_connect_to_client_header(self):
        connect_to_client_message = self.messages_file["Messages"]["Headers"]["Reverse-Shell-Select-Title"]
        return f"{self._display_header_and_footer(connect_to_client_message)}"

    # Displays the currently connected clients information in a nice format, this is displayed when a reverse shell is
    # opened by selecting a connected client id or by waiting for the next client to join the server.

    def client_connected_header(self, client):
        header = self.messages_file["Messages"]["Headers"]["Reverse-Shell-Client-Connected-Header"]
        if "{HOSTNAME}" in header:
            header = header.replace("{HOSTNAME}", client.hostname)
        if "{CLIENT_ID}" in header:
            header = header.replace("{CLIENT_ID}", str(client.client_id))
        sub_header = f"\n{self.messages_file['Messages']['Headers']['Reverse-Shell-Client-Connected-SubHeader']}"
        clear_terminal()
        return f"{self._display_header_and_footer(header, sub_header)}\n{self._display_separator()}"

    # Displays the waiting for client header, this is displayed when pressing option number 2 at the main menu.

    def display_waiting_for_client_header(self):
        header = self.messages_file["Messages"]["Headers"]["Reverse-Shell-Waiting-For-New-Connection-Header"]
        return f"{self._display_header_and_footer(header)}"

    # Displays the main menu, the most common message that will be seen during the program.

    def display_server_menu(self):
        menu_options = self.messages_file["Messages"]["Main-Menu"]
        return self._display_header_and_footer(menu_options)

    # Displays the help messages which is visible when pressing 4 or typing help at the main menu.

    def display_help_message(self):
        help_main_body = self.messages_file["Messages"]["Help-Page"]
        if "{VIEW_PAGE_AMOUNT}" in help_main_body:
            help_main_body = help_main_body.replace("{view_page_amount}", str(self.view_page_amount))
        help_message_contents = self._display_header_and_footer(
            self.messages_file["Messages"]["Headers"]["Help-Page-Header"])
        help_message_contents += f"\n{help_main_body}"
        help_message_contents += self.total_pages_footer(1, 1)
        return help_message_contents

    # Displays the currently connected clients in a nice easy to read format, if no clients are connected then a
    # no clients connected message is displayed.

    def connected_clients_header(self, current_connections):
        connected_clients_header_content = self.messages_file["Messages"]["Headers"]["Client-List-Header"]
        if "{CURRENT_CONNECTIONS}" in connected_clients_header_content:
            connected_clients_header_content = connected_clients_header_content.replace("{CURRENT_CONNECTIONS}",
                                                                                        str(current_connections))
        if "{VIEW_PAGE_AMOUNT}" in connected_clients_header_content:
            connected_clients_header_content = connected_clients_header_content.replace("{VIEW_PAGE_AMOUNT}",
                                                                                        str(self.view_page_amount))
        if "{SEPERATOR}" in connected_clients_header_content:
            connected_clients_header_content = connected_clients_header_content.replace("{SEPERATOR}",
                                                                                        self._display_separator())
        return f"{self._display_separator()}\n{connected_clients_header_content}\n"

    # Displays the current page and out of how many pages, page calculation logic is handled elsewhere, this only
    # displays the message of the calculated logic.

    def total_pages_footer(self, page_number, maximum_page):
        connected_clients_footer_content = f"\n{self._display_separator()}\n"
        connected_clients_footer_content_body = self.messages_file["Messages"]["Footers"]["Total-Pages"]
        if "{PAGE_NUMBER}" in connected_clients_footer_content_body:
            connected_clients_footer_content_body = connected_clients_footer_content_body.replace("{PAGE_NUMBER}",
                                                                                                  str(page_number))
        if "{MAXIMUM_PAGE}" in connected_clients_footer_content_body:
            connected_clients_footer_content_body = connected_clients_footer_content_body.replace("{MAXIMUM_PAGE}",
                                                                                                  str(maximum_page))
        connected_clients_footer_content += connected_clients_footer_content_body
        return f"{connected_clients_footer_content}\n{self._display_separator()}"

    # Clears the terminal and displays the menu, if an error has occurred then it can be passed to this function which
    # will display it above the menu.

    def clear_and_display_menu(self, error=None):
        clear_terminal()
        if error:
            return f"{self.display_errors(error)}\n{self.display_server_menu()}"
        return self.display_server_menu()

    # Displays errors, different errors are formatted differently and thus stored in different dictionary's, the
    # dictionary keys should not be changed as they are used in different files.

    def display_errors(self, error_type):
        header_and_footer = {}
        header_only = {
            "maximum_page": self.messages_file["Messages"]["Warnings"]["Maximum-Page"],
            "minimum_page": self.messages_file["Messages"]["Warnings"]["Minimum-Page"],
            "invalid_choice": self.messages_file["Messages"]["Warnings"]["Invalid-Choice"],
            "multiple_invalid_choices": self.messages_file["Messages"]["Warnings"]["Multiple-Invalid-Choices"],
            "client_connection_error": self.messages_file["Messages"]["Errors"]["Client-Connection-Error"],
            "shutdown_cancellation": self.messages_file["Messages"]["Notifications"]["Shutdown-Cancellation"],
            "invalid_client": self.messages_file["Messages"]["Warnings"]["Invalid-Client"],
            "stopped_waiting_for_new_client":
                self.messages_file["Messages"]["Notifications"]["Stopped-Waiting-For-New-Client"],
            "client_disconnected": self.messages_file["Messages"]["Notifications"]["Client-Disconnected"]
        }
        error_only = {
            "command_send_error": self.messages_file["Messages"]["Errors"]["Command-Send-Error"],
            "server_binding_error": self.messages_file["Messages"]["Errors"]["Server-Binding-Error"],
            "server_shutdown_error": self.messages_file["Messages"]["Errors"]["Server-Shutdown-Error"],
            "no_language_file": self.messages_file["Messages"]["Errors"]["No-Language-File-Error"]
        }
        if error_type in header_and_footer.keys():
            return self._display_header_and_footer(header_and_footer.get(error_type))
        elif error_type in header_only.keys():
            return self._display_header_only(header_only.get(error_type))
        else:
            return error_only.get(error_type)

    # Displays the shutdown message, if the program is shutting down due to an error then this can also be displayed.

    def shutdown_message(self, error=None):
        clear_terminal()
        shutdown_message = ""
        if error:
            shutdown_message += f"{self._display_header_only(self.display_errors(error))}\n"
        shutdown_message += self._display_header_and_footer(
            self.messages_file["Messages"]["Shutdown"]["Termination-Notice"])
        return shutdown_message

    # Displays a message asking the user if they are sure they want to close the program down.

    def shutdown_confirmation_message(self):
        clear_terminal()
        return self._display_header_and_footer(self.messages_file["Messages"]["Shutdown"]["Termination-Confirmation"])

    # Displays the listening for connections on socket message, this is displayed once when the program first starts
    # and allows the server user to know which IP and port number they are receiving connections on.

    def display_listening_for_connections_message(self, host_address, host_port):
        clear_terminal()
        listening_message = f"{self.messages_file['Messages']['Listening-For-Connections-Message']}\n"
        if "{HOST_ADDRESS}" in listening_message:
            listening_message = listening_message.replace("{HOST_ADDRESS}", host_address)
        if "{HOST_PORT}" in listening_message:
            listening_message = listening_message.replace("{HOST_PORT}", str(host_port))
        return f"{self.display_artefact_information()}\n{listening_message}{self.display_server_menu()}"

    # Gets the path of the lang.yml file, if it doesn't exist then it is created in the correct location.

    def get_messages_file(self):
        config_folder = f"{os.getcwd()}/configs"
        os.makedirs(f"{config_folder}", exist_ok=True)
        language_file = f"{config_folder}/lang.yml"
        if os.path.exists(language_file):
            with open(language_file, "r") as language_file:
                language_file_contents = yaml.safe_load(language_file)
            return language_file_contents
        else:
            language_file_contents = self.replace_missing_config()
            with open(f"{config_folder}/lang.yml", "w") as language_file:
                yaml.dump(language_file_contents, language_file, Dumper=CustomYamlDumper, allow_unicode=True,
                          default_flow_style=False)
            self.add_comments_to_config(f"{config_folder}/lang.yml")
            return language_file_contents

    # This is the default config and will return it as a dictionary

    @staticmethod
    def replace_missing_config():
        language_config_values = {
            "MessageConfig": {
                "SeperatorCount": 65,
                "ClientsPerListPage": 10,
                "SeperatorCharacter": "="
            },
            "Messages": {
                "Headers": {
                    "Artefact-Information": "Artefact Created by Elliot. R\n"
                                            "Student ID: 20016796\n"
                                            "Staffordshire University Cyber Security Final Year Project",
                    "Reverse-Shell-Select-Title": "Reverse Shell: Connect To Already Established Client",
                    "Reverse-Shell-Client-Connected-Header": "Reverse Shell: Connected to {HOSTNAME} | "
                                                             "Client ID - {CLIENT_ID}",
                    "Reverse-Shell-Client-Connected-SubHeader": "Type quit to exit the shell and return to the menu.",
                    "Reverse-Shell-Waiting-For-New-Connection-Header": "Reverse Shell: Currently waiting for the next "
                                                                       "client to join...",
                    "Help-Page-Header": "Reverse Shell | Help Page",
                    "Client-List-Header": "Current Connections: {CURRENT_CONNECTIONS} ({VIEW_PAGE_AMOUNT} are "
                                          "displayed per page)\n"
                                          "{SEPERATOR}\n\n"
                                          "Client ID: Client Name | Client Socket - Date Joined @ Time Joined"
                },
                "Main-Menu": "Please select an option from the list below:\n"
                             "1. Connect to specific connection\n"
                             "2. Connect to next new connection\n"
                             "3. View current connections\n"
                             "4. View help menu\n"
                             "5. Exit Program (Will terminate all connections)",
                "Help-Page": "This program can be controlled using the first 5 numbers of the keyboard,\n"
                             "as well as also being able to be controlled by 5 keywords.\n"
                             "{[1] or [select]} will allow you to enter a client id of a currently\n"
                             "connected client and then start a reverse shell with it.\n"
                             "[2] will wait for the next new connection and start a reverse shell\n"
                             "with it shell with the client once it connects.\n"
                             "{[3] or [list]} will display the currently connected clients in a list\n"
                             "displaying {VIEW_PAGE_AMOUNT} connections per page, this can be navigated.\n"
                             "{[4] or [help]} will display this help message.\n"
                             "{[5] or [exit] or [shutdown]} will terminate the program, this can also be\n"
                             "achieved using Ctrl C from anywhere within the program.\n"
                             "For a more detailed walkthrough of this program you should read the ReadMe.md file.",
                "Footers": {
                    "Total-Pages": "Page: {PAGE_NUMBER} / {MAXIMUM_PAGE}"
                },
                "Warnings": {
                    "Maximum-Page": "WARNING: You have already reached the maximum page.",
                    "Minimum-Page": "WARNING: You have already reached the minimum page.",
                    "Invalid-Choice": "WARNING: That was not a valid choice, please try again.",
                    "Multiple-Invalid-Choices": "WARNING: You have entered an incorrect choice 3 times, "
                                                "returning to menu.",
                    "Invalid-Client": "WARNING: That was not a valid Client ID, please try again."
                },
                "Errors": {
                    "Client-Connection-Error": "ERROR: An error occurred whilst accepting a connection.",
                    "Command-Send-Error": "ERROR: That command could not be sent to the target connection.",
                    "Server-Binding-Error": "ERROR: The server was unable to be bound to the socket.",
                    "Server-Shutdown-Error": "ERROR: The server was unable to be shutdown, try killing the server.",
                    "No-Language-File-Error": "ERROR: Language file was not present, it has been regenerated."
                },
                "Notifications": {
                    "Shutdown-Cancellation": "NOTIFICATION: Program termination has been cancelled.",
                    "Stopped-Waiting-For-New-Client": "NOTIFICATION: Waiting for new client has been cancelled."
                },
                "Shutdown": {
                    "Termination-Notice": "TERMINATED: Program has been terminated, goodbye.",
                    "Termination-Confirmation": "WARNING: Are you sure you want to exit the program? "
                                                "All connections will need to be re-established."
                },
                "Listening-For-Connections-Message": "Listening for connections on {HOST_ADDRESS}:{HOST_PORT}..."
            }
        }
        return language_config_values

    # Comments could not be stored in the config dictionary, and thus they must be added to the new lang.yml after.

    @staticmethod
    def add_comments_to_config(language_file_path):
        comment_lines = [
            "# --------------------------------------------------------------------------\n",
            "# Reverse Shell - Language Configuration\n",
            "# This file allows configuration for most of the messages within the program.\n",
            "# \n"
            "# In the event an error occurs after this file is modified then you should\n",
            "# delete this file as a default working one will regenerate. Be sure to back up\n",
            "# the old file as you will be able to copy and paste parts of your config back.\n"
            "# --------------------------------------------------------------------------\n",
            "# Created by Elliot as part of the FYP Artefact @ Staffordshire Cyber Security\n",
            "# --------------------------------------------------------------------------\n"
        ]
        with open(language_file_path, "r") as language_file:
            language_file_lines = language_file.readlines()
        language_file_lines = comment_lines + language_file_lines
        with open(language_file_path, "w") as language_file:
            language_file.writelines(language_file_lines)
