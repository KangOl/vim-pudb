# vim: tw=79
import vim

from bdb import Breakpoint
from itertools import starmap
from linecache import checkcache
from pudb.settings import (
    load_breakpoints, save_breakpoints, get_breakpoints_file_name)
from pudb import NUM_VERSION

LOAD_ARGS = () if NUM_VERSION >= (2013, 1) else (None,)


def breakpoints():
    """
    :return: An iterator over the saved breakpoints.
    :rtype: starmap(Breakpoint)
    """
    return starmap(Breakpoint, load_breakpoints(*LOAD_ARGS))


def breakpoint_dict():
    """
    :return: The saved breakpoints, as a dict with (filename, line number) keys
    :rtype: dict(tuple(str, int), Breakpoint)
    """
    return {(bp.file, bp.line): bp for bp in breakpoints()}


def breakpoint_strings(empty_cond_str='<condition not set>'):
    """
    :return: A generator over the saved breakpoints as strings in the format:
        "filename:linenr:condition"
    :rtype: generator(str)
    """
    return (
        '{file}:{line:d}:{cond}'.format(
            file=bp.file,
            line=bp.line,
            cond=bp.cond if bp.cond else empty_cond_str)
        for bp in breakpoints()
    )


def update_breakpoints():
    vim.eval('sign_unplace(g:pudb_sign_group)')
    for bp in breakpoints():
        try:
            options = '{{"lnum": {line:d}, "priority": {prio:d}}}'.format(
                line=bp.line,
                prio=vim.vars['pudb_priority'],
            )

            # Critical to use vim.eval here instead of vim.vars[] to get sign
            # group, since vim.vars[] will render the string as
            # "b'pudb_sign_group'" instead of "pudb_sign_group"
            vim.eval(
                'sign_place(0, "{group}", "PudbBreakPoint", "{file}", {opts})'
                .format(
                    group=vim.eval('g:pudb_sign_group'),
                    file=bp.file,
                    opts=options,
                ))
        except vim.error:
            # Buffer for the given file isn't loaded.
            continue


def current_position():
    """
    :return: a filename, line number pair, to be used as a key for a
        breakpoint.
    :rtype: tuple(str, int)
    """
    filename = vim.current.buffer.name
    row, _ = vim.current.window.cursor
    return (filename, row)


def toggle_breakpoint():
    """
    Toggles a breakpoint on the current line.
    """
    bps = breakpoint_dict()
    bp_key = current_position()

    if bp_key in bps:
        bps.pop(bp_key)
    else:
        bps[bp_key] = Breakpoint(*bp_key)

    save_breakpoints(bps.values())
    update_breakpoints()


def edit_condition():
    """
    Edit the condition of a breakpoint on the current line.
    If no such breakpoint exists, creates one.
    """
    bps = breakpoint_dict()
    bp_key = current_position()

    if bp_key not in bps:
        bps[bp_key] = Breakpoint(*bp_key)
    bp = bps[bp_key]

    old_cond = '' if bp.cond is None else bp.cond
    vim.command('echo "Current condition: {}"'.format(old_cond))
    vim.command('echohl Question')
    vim.eval('inputsave()')
    bp.cond = vim.eval('input("New Condition: ", "{}")'.format(old_cond))
    vim.eval('inputrestore()')
    vim.command('echohl None')

    save_breakpoints(bps.values())
    update_breakpoints()


def move_breakpoint():
    """
    Move the breakpoint to a different line, preserving the condition.
    """
    bps = breakpoint_dict()
    bp_key = current_position()

    if bp_key not in bps:
        vim.command('echo "No breakpoint at current position"')
        return

    bp = bps[bp_key]
    old_line = bp.line
    vim.command('echo "Current line: {}"'.format(old_line))
    vim.command('echohl Question')
    vim.eval('inputsave()')
    new_line = (vim.eval('input("New line: ", "{}")'.format(old_line)))
    vim.eval('inputrestore()')
    vim.command('echohl None')

    try:
        bp.line = int(new_line)
    except ValueError:
        vim.command('echo "Invalid line number: {}"'.format(new_line))
        return

    save_breakpoints(bps.values())
    update_breakpoints()


def edit_breakpoint_file():
    """
    Open the breakpoint file in a buffer for direct editing.
    """
    vim.command('edit {}'.format(get_breakpoints_file_name()))


def clear_all_breakpoints():
    """
    Clears all pudb breakpoints from all files.
    """
    save_breakpoints([])
    update_breakpoints()


def list_breakpoints():
    """
    Prints a list of all the breakpoints in all files.
    Shows the full file path, line number, and condition of each breakpoint.
    """
    update_breakpoints()
    vim.command('echomsg "Listing all pudb breakpoints:"')
    for bp_string in breakpoint_strings():
        vim.command('echomsg "{}"'.format(bp_string))


def populate_list(list_command):
    """
    Calls the given vim command with a list of the breakpoints as strings in
    quickfix format.
    """
    update_breakpoints()
    bps = list(breakpoint_strings())
    vim.command('{command} {breakpoints}'.format(
        command=list_command,
        breakpoints=bps,
    ))


def quickfix_list_arg():
    """
    :return: The list of dicts to provide as the first argument to setqflist()
    :rtype: list[dict]
    """
    return [
        {
            'filename': bp.file,
            'lnum': bp.line,
            'text': bp.cond if bp.cond else '',
        }
        for bp in breakpoints()
    ]


def quickfix_list():
    """
    Populate the quickfix list with the breakpoint locations.
    """
    setqflist = vim.Function('setqflist')
    entries = quickfix_list_arg()
    setqflist(entries)
    height = min(10, len(entries))
    vim.command('cwindow {}'.format(height))


def location_list():
    """
    Populate the location list with the breakpoint locations.
    """
    setloclist = vim.Function('setloclist')
    entries = quickfix_list_arg()
    setloclist(entries)
    height = min(10, len(entries))
    vim.command('cwindow {}'.format(height))


def clear_linecache():
    """
    Clear the python line cache for the given file if it has changed
    """
    filename = vim.current.buffer.name
    checkcache(filename)
    update_breakpoints()
