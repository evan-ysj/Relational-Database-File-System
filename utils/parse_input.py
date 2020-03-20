#--coding:utf-8--
import re
from utils import query

def parse(fs, input_string):
    input_string_split = re.split(r"\s+", input_string)
    command = input_string_split[0]
    args = []
    if len(input_string_split) > 1:
        args = input_string_split[1:]
    if command == 'pwd':
        print(fs.cur_prefix + fs.cur_name)
    elif command == 'cd':
        if len(args) > 1 or (len(args) == 1 and len(args[0]) < 1):
            print("Error: Please check the format of target path!")
            return False
        if not args:
            args = ['/']
        path = args[0]
        if args[0] == '.':
            return False
        elif args[0] == '..':
            path = fs.parent_prefix + fs.parent_name
        elif path[0] != '/':
            if fs.cur_name == '/':
                path = '/' + path
            else:
                path = fs.cur_prefix + fs.cur_name + '/' + path
        fs.change_dir(path)
    elif command == 'ls':
        if len(args) > 1 or (len(args) == 1 and args[0] != '-l'):
            print("Error: Please check the format of target path!")
            return False
        fs.list_content(args)
    elif command == 'find':
        if len(args) != 1:
            print("Error: Please check the format of target path!")
            return False
        res = fs.find(args[0])
        fs.print_df(res)
    elif command == 'grep':
        if len(args) != 2:
            print("Error: Please check the format of target path!")
            return False
        fs.grep(args)
    elif command == 'exit':
        return True
    elif command == '':
        return False
    else:
        print("Invalid command")
    return False
            