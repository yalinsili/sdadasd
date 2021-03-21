import pymysql
import json
from config import db_host, db_user, db_password, db_name, db_charset


def baglanti():
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 db=db_name,
                                 charset=db_charset,
                                 cursorclass=pymysql.cursors.DictCursor)
    connection.autocommit(True)
    cursor = connection.cursor()
    return cursor, connection
