# coding=utf-8
try:
    import IPython
except ImportError:
    print('IPython not installed!')
    exit(1)

def drop_shell():
    import os
    a = 1
    IPython.embed()


if __name__ == '__main__':
    drop_shell()