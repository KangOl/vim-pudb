" File: pudb.vim
" Author: Christophe Simonis
" Description: Manage pudb breakpoints directly into vim
" Last Modified: March 02, 2018
"
" TODO: handle conditions in breakpoints (at least do not loose them when saving breakpoints)

if exists('g:loaded_pudb_plugin') || &cp
    finish
endif
let g:loaded_pudb_plugin = 1

if !has("pythonx")
    echo "Error: Required vim compiled with +python and/or +python3"
    finish
endif

if !exists('g:pudb_breakpoint_sign')
    let g:pudb_breakpoint_sign = '>>'
endif

if !exists('g:pudb_breakpoint_highlight')
    let g:pudb_breakpoint_highlight = 'error'
endif

if !exists('g:pudb_breakpoint_priority')
    let g:pudb_breakpoint_priority = 100
endif

call sign_define('PudbBreakPoint', {
            \   'text': g:pudb_breakpoint_sign,
            \   'texthl': g:pudb_breakpoint_highlight
            \ })

augroup pudb
    autocmd BufReadPost *.py call s:UpdateBreakPoints()
augroup end

let s:pudb_sign_group = 'pudb_sign_group_'

function! s:UpdateBreakPoints()

" first remove existing signs
call sign_unplace(s:pudb_sign_group .. expand('%:p'))

pythonx << EOF
import vim
from pudb.settings import load_breakpoints
from pudb import NUM_VERSION

filename = vim.eval('expand("%:p")')

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = [bp[:2] for bp in load_breakpoints(*args)]

for bp_file, bp_lnum in bps:
    if bp_file != filename:
        continue

    opts = '{"lnum": %d, "priority": %d}' % (bp_lnum, vim.vars['pudb_breakpoint_priority'])
    vim.eval('sign_place(0, "%s", "PudbBreakPoint", "%s", %s)'
             '' % (vim.eval('s:pudb_sign_group .. expand("%:p")'), filename, opts))
EOF

endfunction

function! s:ToggleBreakPoint()
pythonx << EOF
import vim
from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION
from bdb import Breakpoint

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = {tuple(bp[:2]) for bp in load_breakpoints(*args)}

filename = vim.eval('expand("%:p")')
row, col = vim.current.window.cursor

bp = (filename, row)
if bp in bps:
    bps.remove(bp)
else:
    bps.add(bp)

bp_list = [Breakpoint(bp[0], bp[1]) for bp in bps]

save_breakpoints(bp_list)

vim.command('call s:UpdateBreakPoints()')
EOF
endfunction

command! TogglePudbBreakPoint call s:ToggleBreakPoint()
command! UpdatePudbBreakPoints call s:UpdateBreakPoints()
