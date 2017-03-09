import mysql.connector
from mysql.connector import errorcode
from concourse_common.common import *


class DBHandler:
    def __init__(self, user,password,host):
        self.connection = self.connect_internal(user, password, host)

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor = self.cursor.close()
        self.close_connection()

    def create_db(self, db_name):
        self.execute_db_command("CREATE DATABASE IF NOT  EXISTS `" + db_name + "`;")
        # cursor.execute("USE `" + db_name + "`;")
        # cursor.execute("CREATE TABLE t (c CHAR(20) CHARACTER SET utf8 COLLATE utf8_bin);")

    def drop_db(self, db_name):
        self.execute_db_command("DROP DATABASE `" + db_name + "`;")

    def create_user(self, user_name, user_pw):
        self.execute_db_command("CREATE USER `" + user_name + "`@`%` IDENTIFIED BY \'" + user_pw + "\';")

    def drop_user(self, user_name):
        self.execute_db_command("DROP USER `" + user_name + "`;")

    def grant_all_user_on_db(self, user_name, db_name):
        self.execute_db_command("GRANT ALL ON `" + db_name + "`.* TO `" + user_name + "`@`%`;")

    def grant_select_user_on_db(self, user_name, db_name):
        self.execute_db_command("GRANT SELECT ON `" + db_name + "`.* TO `" + user_name + "`@`%`;")

    def grant_select_user_on_table(self, user_name, db_name, table_name):
        self.execute_db_command("GRANT SELECT ON `" + db_name + "`.`" + table_name + "` TO `" + user_name + "`@`%`;")

    def execute_db_command(self, command):
        self.cursor.execute(command)

    def close_connection(self):
        self.connection.close()

    @staticmethod
    def connect_internal(user,password,host):
        config = {
            'user': user,
            'password': password,
            'host': host
        }
        try:
            connection = mysql.connector.connect(**config)
            return connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log_error('Something is wrong with your user name or password')
            else:
                log_error(err)
            return None
