import threading
from enum import Enum, auto
from queue import Queue


class JobType(Enum):
    ACCEPT_CONNECTIONS = auto()
    PROCESS_COMMANDS = auto()


class ThreadHandler:
    def __init__(self, server):
        self.number_of_threads = 2
        self.task_queue = Queue()
        self.threads = []
        self.server = server

    def initialize_threads(self):
        for _ in range(self.number_of_threads):
            thread = threading.Thread(target=self.process_task_from_queue)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def process_task_from_queue(self):
        while True:
            task_type = self.task_queue.get()
            if task_type == JobType.ACCEPT_CONNECTIONS:
                self.server.connection_manager.accept_connections(self.server.socket)
            elif task_type == JobType.PROCESS_COMMANDS:
                self.server.command_handler.start_command_interface()
            self.task_queue.task_done()

    def enqueue_tasks(self):
        for task_type in [JobType.ACCEPT_CONNECTIONS, JobType.PROCESS_COMMANDS]:
            self.task_queue.put(task_type)
        self.task_queue.join()
