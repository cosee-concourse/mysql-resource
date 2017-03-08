import mysql.connector
from mysql.connector import errorcode
from concourse_common.common import *


def create_db(db_name, cursor):
    cursor.execute("CREATE DATABASE IF NOT  EXISTS `" + db_name + "`;")
    # cursor.execute("USE `" + db_name + "`;")
    # cursor.execute("CREATE TABLE t (c CHAR(20) CHARACTER SET utf8 COLLATE utf8_bin);")


def drop_db(db_name, cursor):
    cursor.execute("DROP DATABASE `" + db_name + "`;")


def create_user(user_name, user_pw, cursor):
    cursor.execute("CREATE USER `" + user_name + "`@`%` IDENTIFIED BY \'" + user_pw + "\';")


def grant_all_user_on_db(user_name, db_name, cursor):
    cursor.execute("GRANT ALL ON `" + db_name + "`.* TO `" + user_name + "`@`%`;")


def grant_select_user_on_db(user_name, db_name, cursor):
    cursor.execute("GRANT SELECT ON `" + db_name + "`.* TO `" + user_name + "`@`%`;")


def grant_select_user_on_table(user_name, db_name, table_name, cursor):
    cursor.execute("GRANT SELECT ON `" + db_name + "`.`" + table_name + "` TO `" + user_name + "`@`%`;")


def connect(user, password, host):
    config = {
        'user': user,
        'password': password,
        'host': host
    }
    connect_internal(**config)


def connect_database(user, password, host, database):
    config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database
    }
    return connect_internal(**config)


def connect_internal(**config):
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log_error('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            log_error("Database does not exist")
        else:
            log_error(err)
        return None


def close(connection):
    connection.close()


def cursor(connection):
    return connection.cursor()
