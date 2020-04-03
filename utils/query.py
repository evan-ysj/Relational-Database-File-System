#--coding:utf-8--
import pymysql
import pandas as pd

class FileSystem(object):
    def __init__(self):
        self.cur_name = '/'
        self.cur_prefix = ''
        self.parent_name = ''
        self.parent_prefix = ''
        self._connection = pymysql.connect('localhost', 'root', 'ece651db', 'filesystem')

    def change_dir(self, target_dir):
        # print("targetdir:",target_dir)
        if target_dir == '/':
            self.cur_name = '/'
            self.cur_prefix = ''
            self.parent_name = ''
            self.parent_prefix = ''
        else:
            target_dir = target_dir.rstrip('/')
            paths = target_dir.split('/')
            cur_name = paths[-1]
            cur_prefix = target_dir[:-len(cur_name)]
            parent_name = paths[-2]
            if not parent_name:
                parent_name = '/'
                parent_prefix = ''
            else:
                parent_prefix = target_dir[:-(len(cur_name)+len(parent_name)+1)]
            cursor = self._connection.cursor()
            try:
                # print("select * from `{}` where name='{}' and prefix='{}'".format(parent_name, cur_name, parent_prefix))
                cursor.execute("select * from `{}` where name='{}' and prefix='{}'".format(parent_name, cur_name, parent_prefix))
            except Exception as e:
                print("Error: Specified directory does not exist!")
                # print(e)
                return
            entry = cursor.fetchone()
            if not entry:
                print("Error: Specified directory does not exist!")
                return
            if entry[3] == 'd':
                self.cur_name = cur_name
                self.cur_prefix = cur_prefix
                self.parent_name = parent_name
                self.parent_prefix = parent_prefix
            elif entry[3] == 'l':
                link = entry[8]
                if link[0] != '/':
                    link_split = link.split('/')
                    link_prefix_split = link.split('/')
                    link_prefix = cur_prefix
                    for i in range(1, len(link_prefix_split) - 1):
                        link_prefix = link_prefix[:-len(link_prefix.split('/')[-1])]
                    link = link_prefix + link.split('../')[-1]
                    if link[0] != '/':
                        link = '/' + link
                cur_name = link_split[-1]
                cur_prefix = link[:-len(cur_name)]
                parent_name = link_split[-2]
                if not parent_name:
                    parent_name = '/'
                    parent_prefix = ''
                else:
                    parent_prefix = link[:-(len(cur_name)+len(parent_name)+1)]
                try:
                    # print("select name from `{}` where name='{}' and prefix='{}' and type='d'".format(parent_name, cur_name, parent_prefix))
                    cursor.execute("select name from `{}` where name='{}' and prefix='{}' and type='d'".format(parent_name, cur_name, parent_prefix))
                except:
                    print("Error: Specified directory does not exist!")
                    return
                if not cursor.fetchall():
                    print("Error: Specified directory does not exist!")
                    return
                self.cur_name = cur_name
                self.cur_prefix = cur_prefix
                self.parent_name = parent_name
                self.parent_prefix = parent_prefix
            cursor.close()

    def list_content(self, args):
        cursor = self._connection.cursor()
        try:
            cursor.execute("select * from `{}` where prefix='{}'".format(self.cur_name, self.cur_prefix))
        except Exception as e:
            print("Error: Can not perform query from database!")
            # print(e)
            return 
        result = []
        for c in cursor.fetchall():           
            row = []
            if args:
                row = [c[3] + c[2], c[5], c[6], c[4], c[7], c[1]]
                if c[8]:
                    row.append('-> ' + c[8])
                else:
                    row.append('')
            else:
                row = [c[1]]
            result.append(row)
        if args:
            self.print_df(result)
        else:
            for r in result:
                print(r[0])
            print("total: ", len(result))
        cursor.close()

    def find(self, target):
        search = target.strip('*')
        cursor = self._connection.cursor()
        try:
            cursor.execute("use information_schema")
            cursor.execute("select table_name from tables where table_schema='filesystem' and table_name like '%{}%'".format(search))
        except Exception as e:
            print("Error: Can not perform query from database!")
            # print(e)
            return []
        tables = cursor.fetchall()
        table_names = []
        for table in tables:
            if target == search and (table[0] == search or table[0] == '[' + search + ']'):
                table_names.append(table)
            elif target == '*' + search and (table[0][-len(search):] == search or table[0][-len(search)-1:] == search + ']'):
                table_names.append(table)
            elif target == search + '*' and (table[0][:len(search)+2] == search or table[0][:len(search)+1] == '[' + search):
                table_names.append(table)
            elif target == '*' + search + '*':
                table_names.append(table)
        if not table_names:
            print("No matched directory or file found!")
        result = []
        try:
            cursor.execute("use filesystem")
            for table_name in table_names:
                name = table_name[0]
                cursor.execute("select distinct prefix from `{}`".format(name))
                prefixs = cursor.fetchall()
                for prefix in prefixs:
                    parent = prefix[0].rstrip('/').split('/')[-1]
                    if not parent:
                        parent = '/'
                    name = name.lstrip('[').rstrip(']')
                    cursor.execute("select * from `{}` where name='{}'".format(parent, name))
                    items = cursor.fetchall()
                    for c in items:
                        row = [c[3] + c[2], c[5], c[6], c[4], c[7], prefix[0] + c[1]]
                        if c[8]:
                            row.append('-> ' + c[8])
                        else:
                            row.append('')
                        if tuple(row) not in result:
                            result.append(tuple(row))
        except Exception as e:
            print("Error: Can not perform query from database!")
            # print(e)
            return []
        cursor.close()
        return result

    def grep(self, args):
        ref = self.find(args[0])
        result = []
        cursor = self._connection.cursor()
        for row in ref:
            if row[0][0] != '-':
                continue
            try:
                cursor.execute("select * from `[{}]`".format(row[5].split('/')[-1]))
            except Exception as e:
                print("Error: Can not perform query from database!")
                return
            files = cursor.fetchall()
            for file in files:
                lines = file[1].split('\n')
                for i, line in enumerate(lines):
                    if args[1].strip('"') in line:
                        result.append((i, line, row[5]))
        if result:
            df = pd.DataFrame(result)
            df.columns = ["Line No.", "Content", "File"]
            print(df.to_string(index=False))
        print("total: ", len(result))
        cursor.close()

    def get_path(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("select * from `$env_path$`")
        except:
            print("Error: Can not get PATH!")
        path = ''
        for p in cursor.fetchall():
            path += p[0] + ':'
        print(path)
        cursor.close()

    def get_executable(self, command):
        if command[0] == '/':
            return [command]
        executable = []
        cursor = self._connection.cursor()
        cursor.execute("select * from `$env_path$`")
        for p in cursor.fetchall():
            executable.append(p[0] + '/' + command)
        cursor.close()
        return executable

    def print_df(self, result):
        if result:
            df = pd.DataFrame(result)
            df.columns = ["Permission", "Owner", "Group", "Size", "Last_update", "Name", "Link"]
            print(df.to_string(index=False))
        print("total: ", len(result))

    def __del__(self):
        self._connection.close()