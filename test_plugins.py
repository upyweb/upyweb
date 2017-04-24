import os
import stat


def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except OSError:
        return False
    return True

def isdir(s):
    """Return true if the pathname refers to an existing directory."""
    try:
        st = os.stat(s)
    except OSError:
        return False
    return stat.S_ISDIR(st[0]) # unix/modos.c

base_path = os.curdir + '/plugins'


for folder in os.listdir(base_path):
    module_path = base_path + '/' + folder
    if exists(module_path + '/__init__.py'):
        print(module_path)
