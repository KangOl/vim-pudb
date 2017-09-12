try:
    import neovim
    import os
    sock = os.environ.get('NVIM_LISTEN_ADDRESS')
    vim = neovim.attach('socket', sock)
except:
    import vim

from pudb.settings import load_breakpoints
from pudb import NUM_VERSION

filename = vim.eval('expand("%:p")')

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = load_breakpoints(*args)

for bp in bps:
    if bp[0] != filename:
        continue

    sign_id = vim.eval("s:next_sign_id")
    vim.command("sign place %s line=%s name=PudbBreakPoint file=%s"
                % (sign_id, bp[1], filename))
    vim.eval("add(b:pudb_sign_ids, s:next_sign_id)")
    vim.command("let s:next_sign_id += 1")
