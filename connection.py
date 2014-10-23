import asyncio

class Connection(asyncio.Protocol):

    def normalize(self, line, ending="\r\n"):

        if not line.endswith(ending):
            line += ending
        return line

    def send(self, *args):

        message = self.normalize(" ".join(args))
        self.transport.write(message.encode())
        print("[B to N]\t%s" % message, end="")

    def forward(self, *args):

        message = self.normalize(" ".join(args))
        for client in self.bouncer.clients:
            if client.broker == self:
                client.transport.write(message.encode())
                print("[B to C]\t%s" % message, end="")
