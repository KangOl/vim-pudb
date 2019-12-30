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

for bp_file, bp_lnum, temp, cond, funcname in load_breakpoints(*args):
    if bp_file != filename:
        continue

    opts = '{"lnum": %d, "priority": %d}' % (bp_lnum, vim.vars['pudb_breakpoint_priority'])
    vim.eval('sign_place(0, "%s", "PudbBreakPoint", "%s", %s)'
             '' % (vim.eval('s:pudb_sign_group .. "%s"' % filename), filename, opts))
EOF

endfunction

function! s:ToggleBreakPoint()
pythonx << EOF
import vim
from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION
from bdb import Breakpoint

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = {(bp.file, bp.line): bp
       for bp in map(lambda args: Breakpoint(*args), load_breakpoints(*args))}

filename = vim.eval('expand("%:p")')
row, col = vim.current.window.cursor

bp_key = (filename, row)
if bp_key in bps:
    bps.pop(bp_key)
else:
    bps[bp_key] = Breakpoint(filename, row)

save_breakpoints(bps.values())

vim.command('call s:UpdateBreakPoints()')
EOF
endfunction

command! TogglePudbBreakPoint call s:ToggleBreakPoint()
command! UpdatePudbBreakPoints call s:UpdateBreakPoints()

if &filetype == 'python'
    call s:UpdateBreakPoints()
endif
