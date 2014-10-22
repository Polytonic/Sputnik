import asyncio

class Client(asyncio.Protocol):

    def __init__(self, bouncer):

        print(bouncer.networks)
        self.bouncer = bouncer
        self.bouncer.clients.append(self)
        # bouncer.networks["freenode"].transport.close()

    def connection_made(self, transport):
        self.transport = transport
        print("Connection Made")

    def connection_lost(self, exit):
        print("ASDF Client Disconnected")

    def data_received(self, data):
        command, message = data.decode().rstrip().split(" ", 1)
        print(command, message)

        if command == "USER":
            print()
            print(message.split(" "))
            print()
