""" 
Usage: load_breakpoints.py <filename>

Print breakpoints in <filename>

Example usage:

    $ ./load_breakpoints.py foo.py
    3
    50
    57

"""

import sys

from pudb.settings import load_breakpoints
from pudb import NUM_VERSION

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = load_breakpoints(*args)

filename = sys.argv[1]

bps = [bp[1] for bp in bps if bp[0] == filename]

for bp in bps:
    print(bp)
