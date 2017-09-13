" File: pudb.vim
" Author: Christophe Simonis
" Description: Manage pudb breakpoints directly into (neo)vim
" Last Modified: 2017-09-13

if exists('g:loaded_pudb_plugin') || &cp
    finish
endif

let g:loaded_pudb_plugin = 1
let g:plugin_path = expand('<sfile>:p:h')
let s:toggle_path = g:plugin_path . '/toggle.py'
let s:update_path = g:plugin_path . '/update.py'

if !has("python") && !has("python3")
    echo "Error: Required (neo)vim compiled with +python"
    finish
endif

sign define PudbBreakPoint text=Ø) texthl=error

let s:first_sign_id = 10000
let s:next_sign_id = s:first_sign_id

augroup pudb
    autocmd BufReadPost *.py call s:UpdateBreakPoints()
augroup end

command! TogglePudbBreakPoint call s:ToggleBreakPoint()

function! s:UpdateBreakPoints()
    " first remove existing signs
    if !exists("b:pudb_sign_ids")
        let b:pudb_sign_ids = []
    endif

    for i in b:pudb_sign_ids
        exec "sign unplace " . i
    endfor

    let b:pudb_sign_ids = []
    execute 'pyfile ' . s:update_path
endfunction

function! s:ToggleBreakPoint()
    execute 'pyfile ' . s:toggle_path
endfunction
