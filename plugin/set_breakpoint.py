""" 
Usage: set_breakpoint.py <filename> <lineno>

Set a breakpoint in <filename> at <lineno>

Example usage:

    $ ./load_breakpoints.py foo.py
    12
    $ ./set_breakpoint.py foo.py 11
    $ ./load_breakpoints.py foo.py
    12
    11
"""

import sys

from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = [bp[:2] for bp in load_breakpoints(*args)]

filename = sys.argv[1]
row = int(sys.argv[2])

bp = (filename, row)
if bp in bps:
    bps.pop(bps.index(bp))
else:
    bps.append(bp)

class BP(object):
    def __init__(self, fn, ln):
        self.file = fn
        self.line = ln
        self.cond = None

bp_list = [BP(bp[0], bp[1]) for bp in bps]

save_breakpoints(bp_list)
