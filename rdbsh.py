#--coding:utf-8--
import sys
from utils import parse_input, query

def main():
    fs = query.FileSystem()
    while True:
        try:
            input_string = input('DBFS > ')
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