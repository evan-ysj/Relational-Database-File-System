# ECE656 Project

Unix file_directory system realized by SQL.

## Source File ##

- treefile  
- create_fs_linux.py  

The directories and files are collected from real Linux system by the following command:
```bash
tree -pinsugfDN --charset utf-8 --timefmt "%F %T" -o treefile /
```
This treefile contains all the paths of directories and files from the root directory. 
We use the file "create_fs.py" to create related database and tables in MySQL. All the directories and files are presented as tables in database. We also copy the file contents into corresponding file tables under "/etc". 

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
Name of the current path.
```python
self.cur_name
```
The prefix of current path (path - cur_name).
```python
self.cur_prefix
```
Name of the parent directory.
```python
self.parent_name
```
The prefix of parent path (parent_path - parent_name).
```python
self.parent_prefix
```
The connection object used to communicate with database.
```python
self._connection
```

**Functions**  
Change current directory to "target_dir".
```python
def change_dir(self, target_dir):
```
List all the child directories and files of current directory.
```python
def list_content(self, args):
```
Find the directories and files that match the target name or pattern.
```python
def find(self, target):
```
Find the lines and files that match the target string pattern.
```python
def grep(self, args):
```
Get the PATH variables in the system.
```python
def get_path(self):
```
Get the executable command with full path by concatenating "command" with PATH variables.
```python
def get_executable(self, command):
```
Convert the query results to pandas dataframes and print to terminal.
```python
def print_df(self, result):
```

## Datebase Structure ##
The season why we didn’t put everything into one table:  
We considered about expansion of filesystem. Theoretically, each directory in the linux system can hold up to 32000 entries for each level. The total amount of directories and files can be as many as 1 billion. Usually, the system will encounter performance issues when a table contains over 5 million lines because the system has to load the whole table into memory. So we split it up and create a table for each distinct directory and file name.

The structure of database tables are as follow:
1. Tables for directories

| Field       | Type         | Null | Key | Default           | Extra                       |
|-------------|--------------|------|-----|-------------------|-----------------------------|
| prefix      | varchar(500) | NO   | PRI | NULL              |                             |
| name        | varchar(100) | NO   | PRI | NULL              |                             |
| permission  | varchar(30)  | NO   |     | rwxr-xr-x         |                             |
| type        | varchar(5)   | NO   | PRI | d                 |                             |
| size        | bigint(20)   | NO   |     | 0                 |                             |
| owner       | varchar(30)  | NO   |     | root              |                             |
| group       | varchar(30)  | NO   |     | root              |                             |
| update_time | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| link        | varchar(500) | YES  |     | NULL              |                             |


2. Tables for files

| Field   | Type         | Null | Key | Default | Extra |
|---------|--------------|------|-----|---------|-------|
| prefix  | varchar(500) | NO   | PRI | NULL    |       |
| content | text         | YES  |     | NULL    |       |


3. Table for PATH variables

| Field | Type         | Null | Key | Default | Extra |
|-------|--------------|------|-----|---------|-------|
| path  | varchar(500) | NO   | PRI | NULL    |       |

