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

import select
import socket
import threading
import time
from src.client_handler import ClientHandler
from src.messages import Messages
from datetime import datetime as dt


# This is where all clients are managed, a dictionary of clients is where ClientHandler instances are stored.
# A new thread that is responsible for checking that clients that are within the dictionary are still connected to the
# server is also created in the initializer.

class ConnectionManager:
    def __init__(self, logging):
        self.clients = {}
        self.view_page_amount = 10
        self.next_client_id = 1
        self.messages = Messages()
        self.logging = logging
        self.new_connection_event = threading.Event()
        self.check_client_connections_thread = threading.Thread(target=self.check_client_connections)
        self.check_client_connections_thread.daemon = True
        self.check_client_connections_thread.start()

    # This is used in a thread in the Server class, this is responsible for accepting all new connections to the server
    # and then stores those connections as ClientHandler instances within the self.clients dictionary where the key is
    # the unique client id and the value is the ClientHandler instance.

    def accept_connections(self, server_socket):
        while True:
            try:
                connection, address = server_socket.accept()
                connection.setblocking(True)
                client_hostname = connection.recv(1024).decode("utf-8")
                new_client_id = self.get_next_client_id()
                new_client = ClientHandler(connection, address[0], address[1], client_hostname,
                                   new_client_id, dt.now(), self.logging)
                self.clients[new_client.client_id] = new_client
                self.new_connection_event.set()
                #  print(f"\nA new connection has been established: {address[2]} @ ({address[0]}:{address[1]})")
            except OSError as error:
                print(f"\n{self.messages.display_errors('client_connection_error')}")
                self.logging.add_error_to_log(error)
                continue

    # This is used in a thread to check if clients are still connected to the server, if they are not then they are
    # removed from the dictionary, this check is performed every second.

    def check_client_connections(self):
        while True:
            time.sleep(1)
            for client_id, client in list(self.clients.items()):
                if not client.send_ping_and_wait_for_pong():
                    self.close_single_connection(client_id)
                    del self.clients[client_id]

    # Checks if a client is connected, requires a ClientHandler instance so that it can access its attributes such as
    # the .connection attribute which is its socket.

    @staticmethod
    def is_client_connected(client):
        client.connection.setblocking(False)
        try:
            client_alive_data = client.connection.recv(16)
            if not client_alive_data:
                return False
            return True
        except BlockingIOError:
            return True
        except (ConnectionResetError, OSError):
            return False
        finally:
            client.connection.setblocking(True)

    # Closes all connections to the server, this is only used within the shutdown function located in Server class.

    def close_all_connections(self):
        for client_id, client in self.clients.items():
            self.close_single_connection(client_id)

    # Closes a single connections and requires the client id, this can pull the ClientHandler instance from the
    # self.clients dictionary as the client_id is unique.

    def close_single_connection(self, client_id):
        if client_id in self.clients:
            self.clients[client_id].connection.close()

    # Calculates which clients should be displayed on the given page, then displays those clients in a formatted manner,
    # each client is displayed on a separate line, if there are no clients connected then a message is displayed to
    # let the user know that no one is connected.

    def list_all_connections(self, page_number, maximum_page, error=None):
        client_list_message = ""
        if error is not None:
            client_list_message += f"{self.messages.display_errors(error)}\n"
        client_list_message += f"{self.messages.connected_clients_header(len(self.clients))}"

        if len(self.clients) > 0:
            start_index = (page_number - 1) * self.view_page_amount
            end_index = start_index + self.view_page_amount
            clients_items = list(self.clients.items())[start_index:end_index]

            for client_id, client in clients_items:
                client_list_message += f"\n{client_id}: {client.hostname} | {client.client_socket} - " \
                                       f"{client.date_joined.strftime('%d/%m/%Y @ %H:%M')}"
        else:
            client_list_message += "\nThere are currently no clients connected."
        client_list_message += f"\n{self.messages.total_pages_footer(page_number, maximum_page)}"
        return client_list_message

    # Returns the last client in the list, or None if there is no one in the list. This is used when waiting for a
    # client to join the server in option 2 of the menu.

    def get_last_client(self):
        if len(self.clients) > 0:
            last_key = next(reversed(self.clients))
            return self.clients[last_key]
        else:
            return None
        
    # Gets the id of the next client, using length of list as client id can lead to errors.

    def get_next_client_id(self):
        current_id = self.next_client_id
        self.next_client_id += 1
        return current_id

    # Returns the length of the clients dictionary and thus how many clients are connected.

    def get_total_clients_connected(self):
        return len(self.clients)

    # Resets the wait for new client Event, this is needed so that the server user can wait for another new client in
    # the future.

    def reset_wait_for_new_client(self):
        self.new_connection_event.clear()
