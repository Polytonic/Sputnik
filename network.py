import asyncio

class Network(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        print("Client Connected")

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exit):
        print("Client Disconnected")
