vim-pudb-and-jam
================

A simple plugin allowing you to manage pudb breakpoints directly from vim.
Forked from `vim-pudb`_ and given some jammy features such as setting and
editing breakpoint conditions, customization options, improved persistence
of breakpoints, and the ability to list active breakpoints either as a
printed message or in a quickfix list.

.. _vim-pudb: https://github.com/KangOl/vim-pudb


Installation
============

Similar to any other vim plugin, use your preferred method. If you're new, check
out
`vim-pathogen <https://github.com/tpope/vim-pathogen#readme>`_ or
`vim-plug <https://github.com/junegunn/vim-plug>`_ or
`:help packages <https://vimhelp.org/repeat.txt.html#packages>`_


Requirements
------------

This plugin needs vim to be compiled with ``+python`` or ``+python3`` as well as
``+signs`` and is intended for vim 8.2 or later, though I'm not sure exactly
which patch is the earliest that is supported.

You will also need to have `pudb`_ installed, obviously.

.. _pudb: https://pypi.org/project/pudb/


Commands
========

``:PudbToggle``
    Add / remove a breakpoint at the current line.

``:PudbEdit``
    Edit the condition of a breakpoint on the current line. Creates a
    breakpoint if one doesn't already exist.

``:PudbClearAll``
    Remove all breakpoints from every file.

``:PudbList``
    Show a list of the full file paths, line numbers, and conditions of all
    breakpoints.

``:PudbLocList``
    Load all breakpoints into the location list. Does not jump to the first
    entry. Breakpoints into buffers that are not loaded will be in the list, but
    with the text '<buffer not loaded>'. Lines containing only whitespace
    will appear with the text '<blank line>'

``:PudbQfList``
    Load all breakpoints into the quickfix list. Does not jump to the first
    entry. Breakpoints into buffers that are not loaded will be in the list, but
    with the text '<buffer not loaded>'. Lines containing only whitespace
    will appear with the text '<blank line>'

``:PudbPopulateList <arg>``
    Supply a list of all breakpoints, in quickfix format, to the Ex command
    given by <arg>. This is a generic form of PudbLocList and PudbQfList,
    allowing you to customise the operation for any precise need you may have.

``:PudbUpdate``
    Sometimes the breakpoint signs can get out of date. The above commands will
    all trigger an update, but this command lets you trigger an update without
    doing anything else.


Mappings
========

There are no mappings set up by default, so you don't have to worry about
conflicts with other plugins. Here's what I use:

::

    nnoremap <leader>bc :<C-U>PudbClearAll<CR>
    nnoremap <leader>be :<C-U>PudbEdit<CR>
    nnoremap <leader>bl :<C-U>PudbList<CR>
    nnoremap <leader>bq :<C-U>PudbQfList<CR>
    nnoremap <leader>bp :<C-U>PudbToggle<CR>
    nnoremap <leader>bu :<C-U>PudbUpdate<CR>


Configuration
=============

The text of the sign can be defined with ``g:pudb_sign`` (default ``'B>'``):

``let g:pudb_sign = 'B>'``

The highlight group of the sign in the sign colum can be defined with
``g:pudb_highlight`` (default ``'error'``):

``let g:pudb_highlight = 'error'``

The priority of the breakpoint signs can be defined with ``g:pudb_priority``
(default ``100``):

``let g:pudb_priority = 100``

This plugin uses sign groups. You can change the name of the sign group using
``g:pudb_sign_group`` (default ``pudb_sign_group``):

``let g:pudb_sign_group = 'pudb_sign_group'``


Known problems
==============

- Currently, the list of breakpoints is not reloaded automatically. Signs are
  only updated when a python buffer is first read, or when one of the above
  commands is called.
- There may be room for speed optimisations.
- There is currently no way to specify which breakpoint file to use.
