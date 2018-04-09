# coding=utf-8
import code


def drop_shell():
    vars = globals()
    vars.update(locals())
    vars['a'] = 1
    vars['b'] = 2
    code.interact(local=vars)


if __name__ == '__main__':
    drop_shell()