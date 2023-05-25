import argparse
import json
import socket
from threading import Thread
import threading


global rows_generator
lock = threading.Lock()


def read_row(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


class Client(Thread):
    def __init__(self, generator, server_host, server_port):
        super().__init__()
        self.generator = generator
        self.server_host = server_host
        self.server_port = server_port

    def run(self):
        while True:
            lock.acquire()
            row = next(self.generator, None)
            lock.release()
            if row is None:
                break

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_host, self.server_port))
            client_socket.send(row.encode())
            data = client_socket.recv(1024).decode()
            while not data:
                data = client_socket.recv(1024).decode()
            result = json.loads(data)
            print(f"{row}: {result}")
            client_socket.close()


def main(arguments):
    rows_generator = read_row(arguments.file)

    threads = []
    for _ in range(arguments.threads):
        thread = Client(rows_generator, 'localhost', 5000)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('threads', type=int)
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    main(args)
