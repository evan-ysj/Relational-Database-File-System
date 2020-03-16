#--coding:utf-8--
import pymysql

class FileSystem(object):
    def __init__(self):
        self.cur_name = '/'
        self.cur_path = '/'
        self.parent_name = ''
        self.parent_path = ''
        self._connection = pymysql.connect('localhost', 'root', 'ece651db', 'filesystem')
        self._cursor = self._connection.cursor()

    def change_dir(self, target_dir):
        pass

    def list_content(self, args):
        pass

    def find(self, target_file):
        pass

    def grep(self, target_pattern):
        pass

    def _print_query(self):
        pass

    def __del__(self):
        self._connection.close()