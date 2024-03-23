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

import struct
from src.messages import Messages


# Each new connection is stored as an object of ClientHandler, this object holds important information such as the
# date the client joined the server, its socket, hostname, ip address, and port number.

class ClientHandler:
    def __init__(self, connection, ip_address, port_number, hostname, client_id, current_date, logging):
        self.connection = connection
        self.address = ip_address
        self.hostname = hostname
        self.port_number = port_number
        self.client_socket = f"{ip_address}:{port_number}"
        self.client_id = client_id
        self.date_joined = current_date
        self.messages = Messages()
        self.logging = logging

    # Sends a command to the client

    def execute_command(self, command):
        try:
            self.connection.send(command.encode('utf-8'))
            encoded_message_length = self.receive_amount_of_data(4)
            if not encoded_message_length:
                return None
            message_length = struct.unpack('>I', encoded_message_length)[0]
            return self.receive_amount_of_data(message_length).decode('utf-8')
        except OSError as error:
            print(self.messages.display_errors("command_send_error"))
            self.logging.add_error_to_log(error)
            return False

    # Receives a response from the client

    def receive_amount_of_data(self, amount_of_data):
        received_data = b''
        while len(received_data) < amount_of_data:
            received_packet = self.connection.recv(amount_of_data - len(received_data))
            if not received_packet:
                return None
            received_data += received_packet
        return received_data
