import typer
from byor.client import RedisClient
from byor.server import RedisServer
from byor.protocol import RedisProtocol
import time

app = typer.Typer()


@app.command()
def run_server(host: str = "127.0.0.1", port: int = 65432):
    server = RedisServer(host, port)
    server.initialize_server()
    server.start_client_threads()

@app.command()
def GET(key:str):
    client = RedisClient('127.0.0.1', 65432)
    client.connect()

    action = "GET"

    value = "none"
    request = f"{action}:{key}:{value}"

    protocolInstance = RedisProtocol()
    client.send_message(protocolInstance.encode(request))

    response = client.receive_message()
    print("Server Response:", response)
    
    client.close()

@app.command()
def SET(key:str, value:str):
    client = RedisClient('127.0.0.1', 65432)
    client.connect()

    action = "SET"

    request = f"{action}:{key}:{value}"
    protocolInstance = RedisProtocol()
    client.send_message(protocolInstance.encode(request))

    response = client.receive_message()
    print("Server Response:", response)
    
    #time.sleep(50)
    client.close()

if __name__ == "__main__":
    app()

