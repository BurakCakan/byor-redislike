
import socket
from byor.protocol import RedisProtocol
from _thread import *
import threading
import time
from queue import Queue


class RedisServer:

    def __init__(self, host: str, port: int) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.bcdb = {}
        self.client_threads = []
        self.print_lock = threading.Lock()

    def initialize_server(self):
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)

        print("Server is listening for connections")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Connection from:", client_address)

            client_thread = threading.Thread(target=self.handler, args=(client_socket,))
            client_thread.start()
            self.client_threads.append(client_thread)
    
    def handler(self, client_socket):
            try:
                self.print_lock.acquire()
                data = self.receive_message(client_socket)
                time.sleep(5)
                response = self.process_request(data)
                #self.send_message(client_socket, response)
                
                action, key, value = data.split(":")

                if action=="SET":
                    self.add_record(key,value)
                    print("Record insertd to BC DB")
                    self.send_message(client_socket,"Record added: {}".format(self.bcdb[key]))
                elif action=="GET":
                    print("BC DB records are listed in the client")
                    self.send_message(client_socket,self.bcdb[key])
                else:
                    print("No action")
                    self.print_lock.release()

            finally:
                self.print_lock.release()
                client_socket.close()

    def receive_message(self,client_socket):
        data = client_socket.recv(1024)
        received_data = data.decode().strip()
        protocolInstance = RedisProtocol()
        return protocolInstance.decode(received_data)
    
    def process_request(self, request):
        return f"Received: {request}"


    def send_message(self, socket, data):
        protocolInstance = RedisProtocol()
        response = protocolInstance.encode(data)
        socket.sendall(response.encode())

    def add_record(self,key,record):
        self.bcdb[key] = record

    def stop_server(self,server_socket):
        for thread in self.client_threads:
            thread.join()
        self.server_socket.close()


if __name__ == "__main__":
    server = RedisServer('127.0.0.1', 65432)
    server.initialize_server()



    