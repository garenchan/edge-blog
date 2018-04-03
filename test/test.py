# coding=utf-8
from utils.cli import CLI

cli = CLI('blog', version='1.0.0')


@cli.option('-a', '--ar', type=int, default=1)
@cli.option('-l', '--log', default='debug')
def test(ar, log):
    print('hello world', type(ar), log)
    
if __name__ == '__main__':
    cli.run()