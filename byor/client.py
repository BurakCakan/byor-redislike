
import sys
import socket
from byor.protocol import RedisProtocol


class RedisClient:

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
    

    def connect(self):
        self.client_socket.connect(self.server_address)

    def receive_message(self):
        data = self.client_socket.recv(1024).decode().strip()
        protocolInstance = RedisProtocol()
        return protocolInstance.decode(data)
    
    def send_message(self,request):
        self.client_socket.sendall(str(request).encode())
        
    def close(self):
        self.client_socket.close()

if __name__ == "__main__":

    if len(sys.argv) < 1:
        print("Please type like `python3 client.py <command> <value>`")
        sys.exit(1)

    procedure = sys.argv[1]
    print(procedure)
    key = sys.argv[2]
    print(key)
    if str(procedure) == "SET":
        value = sys.argv[3]
    else:
        value = "none"

    print(value)

    client = RedisClient('127.0.0.1', 65432)
    client.connect()
    
    message = 55 # added new
    protocolInstance = RedisProtocol()

    request = f"{procedure}:{key}:{value}"
    client.send_message(protocolInstance.encode(request))

    response = client.receive_message()
    print("Server Response->", response)

    client.close()