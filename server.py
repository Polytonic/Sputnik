import asyncio
from network import Network

class Server(asyncio.Protocol):

    def __init__(self):

        self.credentials = {}

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write("Connection Made".encode())

    def data_received(self, data):
        data = data.decode().rstrip()
        print(data)
        # data = iter(data.split())
        # # k, *v = data.split()
        # self.credentials.update(zip(data, data))
        # from pprint import pprint
        # pprint(self.credentials)
        # print()
        # self.transport.write(str(self.credentials).encode())

    def connection_lost(self, exit):
        print("Client Disconnected")
