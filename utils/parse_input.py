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
        print(fs.cur_path)
    elif command == 'cd':
        pass
    elif command == 'ls':
        pass
    elif command == 'find':
        pass
    elif command == 'grep':
        pass
    elif command == 'exit':
        return True
    else:
        print("Invalid command")
    return False
            