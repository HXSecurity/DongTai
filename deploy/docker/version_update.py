######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : version_update
# @created     : 星期四 1月 20, 2022 15:42:27 CST
#
# @description :
######################################################################


from configparser import ConfigParser
import os
import MySQLdb
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser()
status = config.read(os.path.join(BASE_DIR, "../dongtai_conf/conf/config.ini"))
if len(status) == 0:
    print("config file not exist. stop running")
    sys.exit(0)
DBCONFIG = {
    "user": config.get("mysql", "user"),
    "db": config.get("mysql", "name"),
    "passwd": config.get("mysql", "password"),
    "host": config.get("mysql", "host"),
    "port": int(config.get("mysql", "port")),
}
db = MySQLdb.connect(**DBCONFIG, use_unicode=True, charset="utf8mb4")
cursor = db.cursor()
with open(os.path.join(BASE_DIR, "docker/version.sql"), encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        cursor.execute(line)
cursor.close()
db.commit()
