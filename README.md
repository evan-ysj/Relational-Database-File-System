# ECE656 Project

Unix file_directory system realized by SQL.

## Source File ##

- treefile  
- create_fs.py  

The directories and files are collected from real Un*x system by the following command:
```bash
tree -pinsugfDN -L 4 --charset utf-8 --timefmt "%F %T" -o treefile /
```
This treefile contains all the paths of directories and files within a depth of 4 from the root directory. 
We use the util module "create_fs.py" to create related database and tables in MySQL. All the directories and files are presented as tables in database. We also copy the file contents into corresponding file tables under "/etc". 

## Query Module ##

- query.py


## Input Parsing ##

- parse_input.py

