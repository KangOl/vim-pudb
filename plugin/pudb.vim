" File: pudb.vim
" Author: Christophe Simonis, Michael van der Kamp
" Description: Manage pudb breakpoints directly into vim
" Last Modified: March 01, 2020

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
    autocmd BufReadPost *.py call s:UpdateBreakpoints()
augroup end

let s:pudb_sign_group = 'pudb_sign_group_'

function! s:UpdateBreakpoints()

" first remove existing signs
call sign_unplace(s:pudb_sign_group .. expand('%:p'))

pythonx << EOF
import vim
from pudb.settings import load_breakpoints
from pudb import NUM_VERSION

args = () if NUM_VERSION >= (2013, 1) else (None,)

for bp_file, bp_lnum, temp, cond, funcname in load_breakpoints(*args):
    try:
        opts = '{"lnum": %d, "priority": %d}' % (bp_lnum, vim.vars['pudb_breakpoint_priority'])
        vim.eval('sign_place(0, "%s", "PudbBreakPoint", "%s", %s)'
                 '' % (vim.eval('s:pudb_sign_group .. "%s"' % bp_file), bp_file, opts))
    except vim.error:
        # Buffer for the given file isn't loaded.
        continue
EOF

endfunction

function! s:ToggleBreakpoint()
pythonx << EOF
import vim
from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION
from bdb import Breakpoint

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = {(bp.file, bp.line): bp
       for bp in map(lambda values: Breakpoint(*values), load_breakpoints(*args))}

filename = vim.eval('expand("%:p")')
row, col = vim.current.window.cursor

bp_key = (filename, row)
if bp_key in bps:
    bps.pop(bp_key)
else:
    bps[bp_key] = Breakpoint(filename, row)

save_breakpoints(bps.values())
EOF

call s:UpdateBreakpoints()
endfunction

function! s:EditBreakPoint()
pythonx << EOF
import vim
from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION
from bdb import Breakpoint

args = () if NUM_VERSION >= (2013, 1) else (None,)
bps = {(bp.file, bp.line): bp
       for bp in map(lambda values: Breakpoint(*values), load_breakpoints(*args))}

filename = vim.eval('expand("%:p")')
row, col = vim.current.window.cursor

bp_key = (filename, row)
if bp_key not in bps:
    bps[bp_key] = Breakpoint(filename, row)
bp = bps[bp_key]

old_cond = '' if bp.cond is None else bp.cond
vim.command('echo "Current condition: %s"' % old_cond)
vim.command('echohl Question')
vim.eval('inputsave()')
bp.cond = vim.eval('input("New Condition: ", "%s")' % old_cond)
vim.eval('inputrestore()')
vim.command('echohl None')

save_breakpoints(bps.values())
EOF

call s:UpdateBreakpoints()
endfunction

function! s:ClearAllBreakpoints()
pythonx << EOF
from pudb.settings import save_breakpoints
save_breakpoints([])
EOF

call s:UpdateBreakpoints()
endfunction

function! s:ListBreakpoints()
pythonx << EOF
import vim
from pudb.settings import load_breakpoints
from pudb import NUM_VERSION

vim.command('echomsg "Listing all pudb breakpoints:"')

args = () if NUM_VERSION >= (2013, 1) else (None,)
for bp_file, bp_lnum, temp, cond, funcname in load_breakpoints(*args):
    vim.command('echomsg "%s:%d:%s"' % (
        bp_file, bp_lnum, '' if not bool(cond) else ' %s' % cond
    ))
EOF
endfunction

command! PudbToggleBreakpoint call s:ToggleBreakpoint()
command! PudbUpdateBreakpoints call s:UpdateBreakpoints()
command! PudbClearAllBreakpoints call s:ClearAllBreakpoints()
command! PudbEditBreakpoint call s:EditBreakPoint()
command! PudbListBreakpoints call s:ListBreakpoints()

if &filetype == 'python'
    call s:UpdateBreakpoints()
endif
