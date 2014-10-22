import asyncio

class Network(asyncio.Protocol):

    def __init__(self, bouncer, network, nickname, username, realname,
                 password=None, usermode=0):

        self.usermode = str(usermode)
        self.username = username
        self.nickname = nickname
        self.password = password
        self.realname = ":%s" % realname

        self.bouncer, self.network = bouncer, network
        if self.network in self.bouncer.networks:
            self.bouncer.networks[self.network].transport.close()
        self.bouncer.networks[self.network] = self

        self.buffer = ""

    def connection_made(self, transport):
        self.transport = transport
        self.send("PASS", self.password) if self.password else None
        self.send("NICK", self.nickname)
        self.send("USER", self.username, self.usermode, "*", self.realname)
        print("Bouncer Connected to Network %s" % self.network)

    def connection_lost(self, exit):
        print("Bouncer Disconnected from Network %s" % self.network)

    def data_received(self, data):

        command, message = data.decode().rstrip().split(" ", 1)
        print("[N to B]\t%s" % command, message)

        if   command == "PING": self.send("PONG", message)
        elif command == "PONG": self.forward(data) # no this isn't quite right
        else: self.buffer += data.decode()

    def send(self, command, *args):

        message = "%s %s\r\n" % (command, " ".join(args))
        self.transport.write(message.encode())
        print("[B to N]\t" + message.rstrip())

    def forward(self, data):

        print("[B to C]\t%s" % data.decode())
        for client in self.bouncer.clients:
            if client.network == self:
                client.transport.write(data)
