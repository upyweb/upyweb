#!/usr/bin/env python
# encoding: utf-8

import sys


def check_is_system_module(path):
    import os
    for i in sys.path[1:]:
        if os.path.dirname(path).startswith(i):
            return True

    return False

def trace_calls_and_returns(frame, event, arg, stack={}, depth=[0]):
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    line_no = frame.f_lineno
    filename = co.co_filename

    key = '{2}L{1}{0}'.format(func_name, line_no, filename, '\t' * depth[0])

    if check_is_system_module(filename):
        return
    if event == 'call':
        print '{3}{2} L{1}: {0}'.format(func_name, line_no, filename, '\t' * depth[0], co.co_names)
        depth[0] += 1
        return trace_calls_and_returns
    elif event == 'return':
        depth[0] -= 1
        print '{3}{2} L{1}: {0}, {4}'.format(func_name, line_no, filename, '\t' * depth[0], arg)
    return

sys.settrace(trace_calls_and_returns)


from bottle import route, run, template

@route('/hello/<name>')
def index(name):
        return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)

