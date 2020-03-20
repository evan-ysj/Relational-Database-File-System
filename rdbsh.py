#--coding:utf-8--
import sys
from utils import parse_input, query

def header():
    print('*' * 60)
    print('*', ' ' * 56, '*')
    print('*', ' ' * 6, "Welcome to Relational Database Filesystem!", ' ' * 6, '*')
    print('*', ' ' * 15, "Version released: 1.0.0 ", ' ' * 15, '*')
    print('*', ' ' * 56, '*')
    print('*' * 60)

def main():
    header()
    fs = query.FileSystem()
    while True:
        try:
            input_string = input('RDBSH {}> '.format(fs.cur_name))
            terminate = parse_input.parse(fs, input_string)
            if terminate:
                break
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt) or isinstance(e, EOFError):
                break
            
    del fs
    print('Application terminated')
    sys.exit(0)


if __name__ == '__main__':
    main()