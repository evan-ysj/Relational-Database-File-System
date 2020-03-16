#--coding:utf-8--
import re
import pymysql
from warnings import filterwarnings

filterwarnings('ignore', category=pymysql.Warning)

connection = pymysql.connect('localhost', 'root', 'ece651db')
cursor = connection.cursor()
cursor.execute("drop database if exists filesystem")
cursor.execute("create database filesystem")
cursor.execute("use filesystem")
cursor.execute("""create table if not exists `/`(
                    `prefix` varchar(500),
                    `name` varchar(50) not null,
                    `permission` varchar(30) not null default 'rwxr-xr-x',
                    `type` varchar(5) not null default 'd',
                    `size` int default 0 not null,
                    `owner` varchar(30) not null default 'root',
                    `group` varchar(30) not null default 'root',
                    `update_time` TIMESTAMP,
                    `link` varchar(500),
                    primary key (`prefix`, `name`)) engine=InnoDB""")

count = 0
with open('treefile', 'r') as f:
    for line in f.readlines():
        count += 1
        if count == 1:
            continue
        line = line.replace('\ ', '_').strip().strip('\n')
        if not line:
            break 
        attr = line.split('[')[1].split(']')[0]
        attrs = re.split(r"\s+", attr)
        type_ = attrs[0][0]
        permission = attrs[0][1:]
        owner = attrs[1]
        group = attrs[2]
        size = int(attrs[3])
        update_time = attrs[4] + ' ' + attrs[5]
        paths = line.split('[')[1].split(']')[1].strip().split(' -> ')
        path = paths[0]
        link = ''
        if len(paths) > 1:
            link = paths[1]
        path_split = path.split('/')
        name = path_split[len(path_split)-1]
        prefix = path[:-len(name)]
        parent = path_split[len(path_split)-2]
        prefix_parent = prefix[:-(len(parent)+1)]
        if len(name) > 50 or len(parent) > 50:
            continue
        if not parent:
            parent = '/'
            prefix_parent = ''
        try:
            try:
                connection.ping()
            except:
                print("reconnect to db")
                cursor = connection.cursor()
                cursor.execute("use filesystem")
            insert_parent = "insert into `{}` values ('{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}')"
            cursor.execute(insert_parent.format(parent, prefix_parent, name, permission, type_, size, owner, group, update_time, link))
            if type_ == 'd':
                create_dir = """create table if not exists `{}`(
                        `prefix` varchar(500),
                        `name` varchar(100) not null,
                        `permission` varchar(30) not null default 'rwxr-xr-x',
                        `type` varchar(5) not null default 'd',
                        `size` bigint default 0 not null,
                        `owner` varchar(30) not null default 'root',
                        `group` varchar(30) not null default 'root',
                        `update_time` TIMESTAMP,
                        `link` varchar(500),
                        primary key (`prefix`, `name`, `type`)) engine=InnoDB"""
                cursor.execute(create_dir.format(name))
            else:
                create_file = """create table if not exists `[{}]`(
                        `prefix` varchar(500),
                        `content` text,
                        primary key (`prefix`)) engine=InnoDB"""
                cursor.execute(create_file.format(name))
                content = ''
                
                if '/etc/' in prefix:
                    try:
                        with open(prefix + name, 'r') as file:
                            for l in file.readlines():
                                content += l
                    except FileNotFoundError as x:
                        print(x)
                
                insert_cur = "insert into `[{}]` (prefix, content) values ('{}', '{}')"
                cursor.execute(insert_cur.format(name, prefix, content))     
        except Exception as e:
            print(path, e)

            
connection.commit()
connection.close()
print(count)