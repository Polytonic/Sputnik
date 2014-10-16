import asyncio
from network import Network

class Bouncer(object):

    @asyncio.coroutine
    def add_network(self, hostname, port):

        loop = asyncio.get_event_loop()
        yield from loop.create_connection(Network, hostname, port)
        # yieldloop.run_until_complete(coro)

    @asyncio.coroutine
    def create_component(self, name, bin):

        yield from asyncio.create_subprocess_exec(bin, name)
        print("Spawned Process %s" % name)

    def register_component(self, name, bin="python3"):

        # if length == 1, tokenize
        # otherwise pass args
        coroutine = self.create_component(name, bin)
        self.loop.run_until_complete(coroutine)
        print("Registered Component %s" % name)
