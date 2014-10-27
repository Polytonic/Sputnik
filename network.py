from connection import Connection

class Network(Connection):

    def __init__(self, bouncer, network, nickname, username, realname,
                 password=None, usermode=0):

        self.usermode = str(usermode)
        self.username = username
        self.nickname = nickname
        self.password = password
        self.realname = ":%s" % realname

        self.bouncer = bouncer
        self.network = network

    def connection_made(self, transport):

        if self.network in self.bouncer.networks:
            self.bouncer.networks[self.network].transport.close()
        self.bouncer.networks[self.network] = self

        self.transport  = transport
        self.linebuffer = ""
        self.chatbuffer = []

        print("Bouncer Connected to Network")

        self.send("PASS", self.password) if self.password else None
        self.send("NICK", self.nickname)
        self.send("USER", self.username, self.usermode, "*", self.realname)

        # self.send("JOIN", "#testing12345")

    def connection_lost(self, exit):

        self.bouncer.networks.pop(self.network)
        print("Bouncer Disconnected from Network")

    def data_received(self, data):

        data = data.decode()
        if not data.endswith("\r\n"):
            self.linebuffer += data
            return

        for line in (self.linebuffer + data).rstrip().split("\r\n"):

            print("[N to B]\t%s" % line)

            l = line.split(" ", 2)
            if   l[0] == "PING": self.send("PONG", l[1])
            elif l[1] == "PONG": self.forward("PONG", l[2])

            # breaks because it can't check for integers because 353 and 366
            # are related to channel joining and responses etc.

            elif l[1] == "NOTICE": self.chatbuffer.append(line)
            elif l[1] == "MODE": self.chatbuffer.append(line)
            elif l[1].isdigit(): self.chatbuffer.append(line)
            else: self.forward(line)


        else: self.linebuffer = ""

        # only reset the linebuffer if the chatbuffer is successfully replayed to a client
        # need to periodically PING the client to check if it's still active
        # need to intercept QUIT message
        # quit -> AWAY?
        # load plugins
