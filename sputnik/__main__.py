#! /usr/bin/env python3
from bouncer import Bouncer

bnc = Bouncer()
# bnc.add_network("Decepticon1337/freenode", "irc.freenode.net", 6667,
#                 nickname="Decepticon1337",
#                 username="Decepticon1337",
#                 realname="Decepticon1337")
bnc.start()
