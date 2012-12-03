vim-pudb
========

simple plugin allowing you to manage pudb breakpoint directly into vim.

This plugin need vim to be compiled with +python

Installation
============

The recommended way of installing is to use `vim-pathogen`_


Utilisation
===========
To add/remove a breakpoint, you just need to call the command ``:TogglePudbBreakPoint``

For easy access, you can bind it to the F7 key.


    ``nnoremap <F7> :TogglePudbBreakPoint<CR>``

    ``inoremap <F7> <ESC>:TogglePudbBreakPoint<CR>a``

.. _vim-pathogen: https://github.com/tpope/vim-pathogen#readme

Know problems
=============
Currently, the list of breakpoints is not releaded automatically. 

There is also room for speed optimisations.
