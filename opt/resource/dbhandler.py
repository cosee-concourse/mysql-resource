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
        self.execute_db_command("CREATE DATABASE IF NOT EXISTS `" + db_name + "`;")

    def drop_db(self, db_name):
        self.execute_db_command("DROP DATABASE IF EXISTS `" + db_name + "`;")

    def create_user(self, user_name, user_pw):
        if self.user_exists(user_name):
            log_warning("Ignored operation CREATE USER: User {} already exists.".format(user_name))
            return
        self.execute_db_command("CREATE USER `" + user_name + "`@`%` IDENTIFIED BY \'" + user_pw + "\';")

    def drop_user(self, user_name):
        if not self.user_exists(user_name):
            log_warning("Ignored operation DROP USER: User {} does not exist.".format(user_name))
            return
        self.execute_db_command("DROP USER `" + user_name + "`;")

    def grant_all_user_on_db(self, user_name, db_name):
        if not self.user_exists(user_name):
            log_warning("WARNING: User {} was created implicitly by GRANT command because it did not exist.".format(user_name))
        self.execute_db_command("GRANT ALL ON `" + db_name + "`.* TO `" + user_name + "`@`%`;")

    def grant_select_user_on_db(self, user_name, db_name):
        if not self.user_exists(user_name):
            log_warning("WARNING: User {} was created implicitly by GRANT command because it did not exist.".format(user_name))
        self.execute_db_command("GRANT SELECT ON `" + db_name + "`.* TO `" + user_name + "`@`%`;")

    def grant_select_user_on_table(self, user_name, db_name, table_name):
        if not self.table_exists(db_name, table_name):
            log_warning("Ignored operation GRANT SELECT-TABLE: Table {} does not exist".format(table_name))
            return
        if not self.user_exists(user_name):
            log_warning("WARNING: User {} was created implicitly by GRANT command because it did not exist.".format(user_name))
        self.execute_db_command("GRANT SELECT ON `" + db_name + "`.`" + table_name + "` TO `" + user_name + "`@`%`;")

    def user_exists(self, username):
        self.execute_db_command("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{}');".format(username))
        if self.cursor.fetchall() == (1,):
            return True
        else:
            return False

    def table_exists(self, database, table):
        self.execute_db_command("""
            SELECT count(*)
            FROM information_schema.TABLES
            WHERE (TABLE_SCHEMA = '{}') AND (TABLE_NAME = '{}');""".format(database, table))
        if self.cursor.fetchall() == (1,):
            return True
        else:
            return False

    def execute_db_command(self, command):
        self.cursor.execute(command)

    def execute_multiple_db_commands(self, command):
        self.cursor.execute(command, multi=True)

    def close_connection(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

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
