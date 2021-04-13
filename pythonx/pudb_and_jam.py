# vim: tw=79
import linecache
import vim

from bdb import Breakpoint
from pudb.settings import load_breakpoints, save_breakpoints
from pudb import NUM_VERSION

LOAD_ARGS = () if NUM_VERSION >= (2013, 1) else (None,)


def update():
    vim.command('call sign_unplace(g:pudb_sign_group)')
    for bp_file, bp_lnum, temp, cond, funcname in load_breakpoints(*LOAD_ARGS):
        try:
            opts = ('{"lnum": %d, "priority": %d}'
                    % (bp_lnum, vim.vars['pudb_priority']))

            # Critical to use vim.eval here instead of vim.vars[] to get sign
            # group, since vim.vars[] will render the string as
            # "b'pudb_sign_group'" instead of "pudb_sign_group"
            vim.eval('sign_place(0, "%s", "PudbBreakPoint", "%s", %s)'
                     '' % (vim.eval('g:pudb_sign_group'), bp_file, opts))
        except vim.error:
            # Buffer for the given file isn't loaded.
            continue


def toggle():
    """
    Toggles a breakpoint on the current line.
    """
    bps = {(bp.file, bp.line): bp
           for bp in map(lambda values: Breakpoint(*values),
                         load_breakpoints(*LOAD_ARGS))}

    filename = vim.eval('expand("%:p")')
    row, col = vim.current.window.cursor

    bp_key = (filename, row)
    if bp_key in bps:
        bps.pop(bp_key)
    else:
        bps[bp_key] = Breakpoint(filename, row)

    save_breakpoints(bps.values())
    update()


def edit():
    """
    Edit the condition of a breakpoint on the current line.
    If no such breakpoint exists, creates one.
    """
    bps = {(bp.file, bp.line): bp
           for bp in map(lambda values: Breakpoint(*values),
                         load_breakpoints(*LOAD_ARGS))}

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
    update()


def clearAll():
    """
    Clears all pudb breakpoints from all files.
    """
    save_breakpoints([])
    update()


def list():
    """
    Prints a list of all the breakpoints in all files.
    Shows the full file path, line number, and condition of each breakpoint.
    """
    update()
    vim.command('echomsg "Listing all pudb breakpoints:"')
    for bp_file, bp_lnum, temp, cond, funcname in load_breakpoints(*LOAD_ARGS):
        vim.command('echomsg "%s:%d:%s"' % (
            bp_file, bp_lnum, '' if not bool(cond) else ' %s' % cond
        ))


def populateList(list_command):
    """
    Calls the given vim command with a list of the breakpoints as strings in
    quickfix format.
    """
    update()
    qflist = []
    for bp_file, bp_lnum, temp, cond, funcname in load_breakpoints(*LOAD_ARGS):
        try:
            line = vim.eval('getbufline(bufname("%s"), %s)'
                            % (bp_file, bp_lnum))[0]
            if line.strip() == '':
                line = '<blank line>'
        except LookupError:
            line = '<buffer not loaded>'
        qflist.append(':'.join(map(str, [bp_file, bp_lnum, line])))
    vim.command('%s %s' % (list_command, qflist))


def quickfixList():
    """
    Populate the quickfix list with the breakpoint locations.
    """
    populateList('cgetexpr')


def locationList():
    """
    Populate the location list with the breakpoint locations.
    """
    populateList('lgetexpr')


def clearLineCache():
    """
    Clear the python line cache for the given file if it has changed
    """
    filename = vim.eval('expand("%:p")')
    linecache.checkcache(filename)
    update()
