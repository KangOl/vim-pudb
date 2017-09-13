try:
    import neovim
    import os
    sock = os.environ.get('NVIM_LISTEN_ADDRESS')
    vim = neovim.attach('socket', sock)
except:
    import vim

from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = [bp[:2] for bp in load_breakpoints(*args)]

filename = vim.eval('expand("%:p")')
row, col = vim.current.window.cursor

bp = (filename, row)
if bp in bps:
    bps.pop(bps.index(bp))
else:
    bps.append(bp)


class BP(object):
    def __init__(self, fn, ln):
        self.file = fn
        self.line = ln
        # TODO: Properly handle conditions and allow the user to create them
        # from (neo)vim
        self.cond = None


bp_list = [BP(_bp[0], _bp[1]) for _bp in bps]

save_breakpoints(bp_list)

vim.command('call s:UpdateBreakPoints()')
