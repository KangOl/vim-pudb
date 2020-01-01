vim-pudb
========

Simple plugin allowing you to manage pudb breakpoints directly from vim.

This plugin needs vim to be compiled with +python or +python3

Installation
============
The recommended way of installing is to use `vim-pathogen`_ or `vim-plug`_

.. _vim-pathogen: https://github.com/tpope/vim-pathogen#readme
.. _vim-plug: https://github.com/junegunn/vim-plug

How to use
==========
To add/remove a breakpoint, you just need to call the command ``:TogglePudbBreakPoint``

For easy access, use a mapping:

    ``nnoremap <F8> :TogglePudbBreakPoint<CR>``

    ``inoremap <F8> <ESC>:TogglePudbBreakPoint<CR>a``
   
In case the breakpoints get out of sync after a debugging session, there is also a command
``:UpdatePudbBreakPoints`` which refreshes the breakpoint signs.

To edit the condition of a breakpoint on the current line, use the command
``:EditPudbBreakPoint``

To clear all pudb breakpoints, use the command ``:ClearAllPudbBreakPoints``

Configuration
=============
The text of the sign can be defined with ``g:pudb_breakpoint_sign`` (default
``'>>'``):

    ``let g:pudb_breakpoint_sign = '>>'``

The highlight group of the sign in the sign colum can be defined with
``g:pudb_breakpoint_highlight`` (default ``'error'``):

    ``let g:pudb_breakpoint_highlight = 'error'``

The priority of the breakpoint signs can be defined with
``g:pudb_breakpoint_priority`` (default ``100``):

    ``let g:pudb_breakpoint_priority = 100``
Known problems
=============
Currently, the list of breakpoints is not reloaded automatically.

There is also room for speed optimisations.
