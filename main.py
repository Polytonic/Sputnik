#! /usr/bin/env python3
from bouncer import Bouncer

sputnik = Bouncer()
sputnik.add_network("irc.freenode.net", 6667)
sputnik.add_network("irc.quakenet.org", 6667)
# sputnik.start() # this is a blocking call

sputnik.add_network("irc.efnet.org", 6667)
