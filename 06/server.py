import argparse
import json
import queue
import socket
from collections import Counter
from threading import Thread
import threading
from bs4 import BeautifulSoup
import requests


class Worker(Thread):
    def __init__(self, worker_id, top_k):
        super().__init__()
        self.worker_id = worker_id
        self.top_k = top_k

    def run(self):
        while True:
            conn, addr = que.get()

            if conn == 'stop':
                break

            with conn:
                data = conn.recv(1024).decode()
                url = data.strip()
                result = self.process_url(url)
                conn.send(json.dumps(result).encode())
                count[self.worker_id - 1] += 1
                print(f"{sum(count)} URLs processed")

    def process_url(self, url):
        response = requests.get(url)
        html_content = response.content
        root = BeautifulSoup(html_content, 'html.parser')
        words = root.get_text().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').split(' ')
        words = [word for word in words if (word != '') and (word.isalpha())]
        counter = Counter(words)
        return dict(counter.most_common(self.top_k))


class Master:
    def __init__(self, host, port, num_workers, top_k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()

        for i in range(self.num_workers):
            worker = Worker(i + 1, self.top_k)
            count.append(0)
            worker.start()

        while True:
            try:
                server_socket.settimeout(15)
                conn, addr = server_socket.accept()
                que.put((conn, addr))
            except socket.timeout:
                for _ in range(self.num_workers):
                    que.put(('stop', None))
                server_socket.close()
                break


que = queue.Queue()
count = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='num_workers', type=int)
    parser.add_argument('-k', dest='top_k', type=int)
    args = parser.parse_args()

    master = Master('localhost', 5000, args.num_workers, args.top_k)
    master.start()
