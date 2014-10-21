import asyncio

class Network(asyncio.Protocol):

    def __init__(self, nickname, ident, realname, password=None, usermode=0):

        self.ident = ident
        self.usermode = str(usermode)
        self.nickname = nickname
        self.password = password
        self.realname = ":%s" % realname

    def connection_made(self, transport):
        self.transport = transport

        if self.password: self.send("PASS", self.password)
        self.send("NICK", self.nickname)
        self.send("USER", self.ident, self.usermode, "*", self.realname)



        self.send("JOIN", "#testing12345")
        print("Connected to Network")

    def data_received(self, data):

        command, message = data.decode().rstrip().split(" ", 1)
        if command == "PING": self.send("PONG", message)
        print(command, message)

    def connection_lost(self, exit):
        print("Client Disconnected")

    def send(self, command, *args):

        message = "%s %s\r\n" % (command, " ".join(args))
        self.transport.write(message.encode())
        print("Wrote: " + message.rstrip())
