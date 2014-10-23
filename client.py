from connection import Connection

class Client(Connection):

    def __init__(self, bouncer):

        self.bouncer = bouncer
        self.network = None

        self.connected = False

    def connection_made(self, transport):
        self.transport = transport
        self.bouncer.clients.add(self)

        print("Client Connected to Bouncer")


    def connection_lost(self, exit):
        self.bouncer.clients.remove(self)
        print("Client Disconnected from Bouncer")

    def data_received(self, data):

        command, message = data.decode().rstrip().split(" ", 1)
        print("[D to C]\t%s %s" %(command, message))

        if command == "PING": self.forward(data)
        if command == "USER":

            self.username, self.network = message.split(" ")[0].split("/")
            if not self.network in self.bouncer.networks:
                self.send("This Network Does Not Exist")
            else: print("\n\tUsing Network: %s\n" % self.network)

        # this prints the server connection log
        # there is a race condition here
        if self.network and not self.connected:
            for line in self.bouncer.networks["freenode"].chatbuffer:
                self.send(line)
            self.connected = True

        if self.network:

            self.forward(data.decode())


    def send(self, *args):

        message = self.normalize(" ".join(args))
        self.transport.write(message.encode())
        print("[C to D]\t%s" % message, end="")

    def forward(self, *args):

        message = self.normalize(" ".join(args))
        self.bouncer.networks[self.network].transport.write(message.encode())
        print("[C to B]\t%s" % message, end="")
