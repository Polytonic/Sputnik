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

    def connection_made(self, transport):
        self.transport = transport

        if self.password: self.send("PASS", self.password)
        self.send("NICK", self.nickname)
        self.send("USER", self.username, self.usermode, "*", self.realname)

        self.send("JOIN", "#testing12345")

    def connection_lost(self, exit):
        print("Network Disconnected")

    def data_received(self, data):

        command, message = data.decode().rstrip().split(" ", 1)
        print(command, message)
        if command == "PING": self.send("PONG", message)
        for client in self.bouncer.clients:
            client.transport.write(data)

    def send(self, command, *args):

        message = "%s %s\r\n" % (command, " ".join(args))
        self.transport.write(message.encode())
        print("Wrote: " + message.rstrip())
