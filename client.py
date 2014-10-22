import asyncio

class Client(asyncio.Protocol):

    def __init__(self, bouncer):

        self.bouncer = bouncer
        self.network = None

    def connection_made(self, transport):
        self.transport = transport
        self.bouncer.clients.add(self)
        print("Client Connected to Bouncer")
        self.transport.write(self.bouncer.networks["freenode"].buffer.encode())
        print(self.bouncer.networks["freenode"].buffer)

    def connection_lost(self, exit):
        self.bouncer.clients.remove(self)
        print("Client Disconnected from Bouncer")

    def data_received(self, data):

        command, message = data.decode().rstrip().split(" ", 1)
        print("[D to C]\t", command, message)

        if command == "PING": self.forward(data)
        if command == "USER":

            self.username, self.network = message.split(" ")[0].split("/")
            if not self.network in self.bouncer.networks:
                print("This Network Does Not Exist")
            else: self.network = self.bouncer.networks.get(self.network)

    def send(self, command, *args):

        message = "%s %s\r\n" % (command, " ".join(args))
        self.transport.write(message.encode())
        print("[C to B]\t" + message.rstrip())

    def forward(self, data):
        print("[C to B]\t%s" % data.decode())
        self.bouncer.networks["freenode"].transport.write(data)
