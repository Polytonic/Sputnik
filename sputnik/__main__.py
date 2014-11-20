#! /usr/bin/env python3
"""Sputnik Main Runtime

This implements the Sputnik main file, allowing users to run the Sputnik
bouncer from the project root as a folder. e.g. `python3 sputnik`.
"""

from bouncer import Bouncer
Bouncer().start()
