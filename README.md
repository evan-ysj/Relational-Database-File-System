# ECE656 Project

Unix file_directory system realized by SQL.

## Source File ##

- treefile  
- create_fs_linux.py  

The directories and files are collected from real Un*x system by the following command:
```bash
tree -pinsugfDN --charset utf-8 --timefmt "%F %T" -o treefile /
```
This treefile contains all the paths of directories and files within a depth of 4 from the root directory. 
We use the util module "create_fs.py" to create related database and tables in MySQL. All the directories and files are presented as tables in database. We also copy the file contents into corresponding file tables under "/etc". 

## Program Entrance ##

- rdbsh.py

This file is the entrance of the whole program. It simulates a terminal interface to accept commands from user.

## Input Parsing ##

- parse_input.py

This file is responsible for parsing user's input strings and process some simple logic to pass parameters to the query module.

## Query Module ##

- query.py

This module defines a filesystem class that contains some basic attributes and all the core functions. The attributes and functions are described as below.  
**Attributes**
```python
self.cur_name
self.cur_prefix
self.parent_name
self.parent_prefix
self._connection
```
**Functions**
```python
def change_dir(self, target_dir):
def list_content(self, args):
def find(self, target):
def grep(self, args):
def get_path(self):
def get_executable(self, command):
def print_df(self, result):
```


