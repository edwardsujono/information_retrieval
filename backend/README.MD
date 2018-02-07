# Information Retrieval Backend

### Note
1. This project use Django 2.* which is only support Python 3
2. This project is assumed to be deployed in Ubuntu 14.0 or 16.0
3. This project use MySQL as DBMS

### Installation
1. Install libmysqlclient-dev as library for mysql driver with command
```
sudo apt-get install python3-dev libmysqlclient-dev
``` 
2. Install python packages by invoking
```
pip install -r requirements.txt
```
3. Add MySQL database configuration file in /etc/mysql/my_backend.cnf with content
```
[client]
database = [database_name]
user = [database_user]
password = [database password]
host = [host IP address]
default-character-set = utf8
```


