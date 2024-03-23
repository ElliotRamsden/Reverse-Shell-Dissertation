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

import threading
import math
import os
import signal
import pyautogui
from src.messages import Messages, clear_terminal


# Clears the terminal and prints the given message to the terminal.

def clear_and_print(message):
    clear_terminal()
    print(message)


# This class is responsible for handling most of the user interaction to the application.

class ServerCommandHandler:
    def __init__(self, connection_manager, server_shutdown, logging):
        self.connection_manager = connection_manager
        self.shutdown_server = server_shutdown
        self.selected_client = None
        self.client_current_directory = None
        self.view_page_amount = 10
        self.messages = Messages()
        self.logging = logging
        self.new_client_connection_wait_interrupted = False
        self.disconnect_shell = False

    # Waits for the next new connection to connect to the server socket, once the client joins the reverse shell is
    # opened straight away which allows the user to start executing commands on the client system. In the event that
    # the server user does not wish to wait for a new client connection then they can press any key and that will
    # terminate the wait and return them to the menu.

    def connect_to_next_new_connection(self):
        clear_and_print(self.messages.display_waiting_for_client_header())
        self.connection_manager.reset_wait_for_new_client()
        self.new_client_connection_wait_interrupted = False
        waiting_for_client_thread = threading.Thread(target=self.break_waiting_for_new_client)
        waiting_for_client_thread.start()
        self.connection_manager.new_connection_event.wait()

        if not self.new_client_connection_wait_interrupted:
            self.selected_client = self.connection_manager.get_last_client()
            if self.selected_client is not None:
                pyautogui.press("enter")
                clear_and_print(f"{self.messages.client_connected_header(self.selected_client)}")
                self.enter_command_mode()
            else:
                clear_and_print(self.messages.clear_and_display_menu("stopped_waiting_for_new_client"))
        else:
            clear_and_print(self.messages.clear_and_display_menu("stopped_waiting_for_new_client"))

    # If the user presses any key the wait will terminate, the flag will be set to true and the thread event will end.

    def break_waiting_for_new_client(self):
        input("Press any key to cancel waiting for new connection > ")
        self.new_client_connection_wait_interrupted = True
        self.connection_manager.new_connection_event.set()

    # Displays the contents of the help message and allows the user to return top the menu.

    def display_help_message(self):
        clear_and_print(self.messages.display_help_message())
        input("Press any key to return to the menu > ")
        clear_and_print(self.messages.clear_and_display_menu())

    # Displays the currently connected clients, allows the user to navigate between pages by using commands such as
    # next, back, and also allows the user to return to the menu by using the menu command.

    def display_connected_clients(self):
        page_number = 1
        current_connections = self.connection_manager.get_total_clients_connected()
        maximum_page = max(1, math.ceil(current_connections / self.view_page_amount))
        clear_and_print(self.connection_manager.list_all_connections(page_number, maximum_page))

        while True:
            user_choice = input("Enter choice (Next, Back, Menu) > ").lower()
            if user_choice in ["menu", "m"]:
                clear_and_print(self.messages.clear_and_display_menu())
                break
            elif user_choice in ["next", "n", "back", "b"]:
                new_page_number = self.adjust_page_number(page_number, maximum_page, user_choice)
                if new_page_number != page_number:
                    page_number = new_page_number
                    clear_and_print(self.connection_manager.list_all_connections(page_number, maximum_page))
                else:
                    error = "maximum_page" if user_choice in ["next", "n"] else "minimum_page"
                    clear_and_print(self.connection_manager.list_all_connections(page_number, maximum_page, error))
            else:
                self.handle_invalid_choice(page_number, maximum_page)
                break

    # If the users input was valid then it will return the page number depending on the choice, either plus or minus
    # one of the original page number. If it was not valid the original page number is returned.

    @staticmethod
    def adjust_page_number(page_number, maximum_page, page_direction):
        if page_direction in ["next", "n"] and page_number < maximum_page:
            return page_number + 1
        elif page_direction in ["back", "b"] and page_number > 1:
            return page_number - 1
        return page_number

    # The user should not be stuck in a loop or being unable to return to the menu, if for some reason they don't know
    # how to get back to the menu and thus keep entering incorrect page numbers then this will only occur three times
    # before giving an error and sending them back to the menu, this amount can be changed but by default it is 3.

    def handle_invalid_choice(self, page_number, maximum_page, attempts=3):
        for _ in range(attempts-1):
            clear_and_print(self.connection_manager.list_all_connections(page_number, maximum_page, "invalid_choice"))
            if input("Enter choice (Next, Back, Menu) > ").lower() in ["menu", "m"]:
                clear_and_print(self.messages.clear_and_display_menu())
                return
        else:
            clear_and_print(self.messages.clear_and_display_menu("multiple_invalid_choices"))
            return

    # Takes a value called client_id then checks to see if it is a number, if it is a number it attempts to find it in
    # the ConnectionManager clients dictionary. If it is not a number or not in the dictionary an error is displayed.

    def select_client(self, client_id):
        try:
            client_id = int(client_id)
            self.selected_client = self.connection_manager.clients.get(client_id)
            if self.selected_client is None:
                clear_and_print(self.messages.display_errors("invalid_client"))
                return False
            clear_and_print(f"{self.messages.client_connected_header(self.selected_client)}")
            return True
        except (ValueError, IndexError):
            clear_and_print(self.messages.display_errors("invalid_client"))
            self.selected_client = None
            return False

    # This allows the user to interact with the program and checks their input, if the input is one of the keywords or
    # numbers then it will be passed to the process_command function or just handled if it is a select (client_id)
    # command, if it is not either of those then an error will be displayed.

    def start_command_interface(self):
        while True:
            server_command = input("Please enter a choice from the menu > ").lower()
            if server_command.startswith("select") and (not server_command == "select"):
                if self.handle_client_selection(server_command):
                    self.enter_command_mode()
                else:
                    print(self.messages.display_server_menu())
            elif server_command in ["1", "2", "help", "4", "list", "3", "shutdown", "5", "select", "exit"]:
                self.process_command(server_command)
            else:
                clear_and_print(self.messages.clear_and_display_menu("invalid_choice"))

    # If the user selects a client from the menu such as select 1 then this function will aim to get the client id on
    # its own and passes it to the select_client function to check if it is a valid client id or not.

    def handle_client_selection(self, command):
        client_id = command.split(" ")[-1]
        return self.select_client(client_id)

    # This handles the user input and depending on their choice calls a function that corresponds to it, there is a
    # default function call too although this is just a backup as this should never be called as it is already handled
    # elsewhere.

    def process_command(self, command):
        match command:
            case "1" | "select":
                self.select_client_menu()
            case "2":
                self.connect_to_next_new_connection()
            case "help" | "4":
                self.display_help_message()
            case "list" | "3":
                self.display_connected_clients()
            case "shutdown" | "5" | "exit":
                self.shutdown_confirmation_check()
            case "":
                clear_and_print(self.messages.clear_and_display_menu("invalid_choice"))

    # When the reverse shell is initiated this is the function that starts it, firstly another check is performed to
    # make sure a valid client is selected, if it is then the clients current directory is displayed as the prompt this
    # is similar to how most CLIs display their prompt, and thus it makes the server user feel as if they are using the
    # client machine as if they are there. Commands are then sent to the client and outputs are received using other
    # functions.

    def enter_command_mode(self):
        if not self.selected_client:
            print("No client is selected.")
            return

        self.client_current_directory = self.selected_client.execute_command(" ")
        print(self.client_current_directory, end="")

        while True:
            if self.disconnect_shell is True:
                clear_and_print(self.messages.clear_and_display_menu("client_disconnected"))
                self.disconnect_shell = False
                break
            else:
                command = input().strip()
                if command.lower() == 'quit':
                    clear_and_print(self.messages.clear_and_display_menu())
                    break
                elif command.lower() == "":
                    if self.client_current_directory[-1] == ">":
                        self.client_current_directory = f"{self.client_current_directory} "
                    print(self.client_current_directory, end="")
                elif command:
                    self.send_command_to_selected_client(command)

    # This is what is responsible for sending the client the commands as well as receiving outputs from the commands
    # given to the client, it is done by sending the command to the ClientHandler execute_command function and this
    # function also sets the current_working directory of the host just in case it needs to be displayed later.

    def send_command_to_selected_client(self, command):
        if self.selected_client:
            output = self.selected_client.execute_command(command)
            if output:
                print(output, end="")
                self.client_current_directory = (output.strip().split('\n'))[-1]
            elif output is False:
                self.disconnect_shell = True
            else:
                print("No output received from client.")
        else:
            print("No client selected.")

    # When a server user types select or 1, they will be taken to the select client menu, this will allow them to enter
    # a client id, it will then pass the client id to another function to check if it is valid or not, if the client id
    # is not valid after 3 attempts then it will break this loop and return them to the main menu.

    def select_client_menu(self):
        clear_terminal()
        for _ in range(3):
            print(self.messages.display_connect_to_client_header())
            user_choice = input("Enter choice (Client ID e.g. 1, Menu) > ").lower()

            if user_choice in ["menu", "m"]:
                clear_and_print(self.messages.clear_and_display_menu())
                break
            elif self.select_client(user_choice):
                self.enter_command_mode()
                break
            else:
                clear_and_print(self.messages.display_errors("invalid_choice"))
        else:
            clear_and_print(self.messages.clear_and_display_menu("multiple_invalid_choices"))

    # This will allow the user to ensure they want to close the program, once the program is closed all connections will
    # have to be re-established, this check allows the user 3 chances to enter y or n, if a valid choice is not made
    # within 3 attempts then the program will return to the menu. This is not displayed when the user presses Ctrl C as
    # when this happens it is assumed the user is doing that for a reason, and thus it just exits. If the user input is
    # Y then the program will cause a signal.SIGINT which is handled elsewhere and means the program will close the same
    # way as if Ctrl C was pressed, thus this also means all threads are properly killed.

    def shutdown_confirmation_check(self):
        print(self.messages.shutdown_confirmation_message())
        for _ in range(3):
            user_quit_program_choice = input("Enter Choice (Y or N) > ").lower()
            if user_quit_program_choice == "y":
                os.kill(os.getpid(), signal.SIGINT)
                break
            elif user_quit_program_choice == "n":
                print(self.messages.clear_and_display_menu("shutdown_cancellation"))
                break
            else:
                print(self.messages.shutdown_confirmation_message())
        else:
            print(self.messages.clear_and_display_menu("multiple_invalid_choices"))
