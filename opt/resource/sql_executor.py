import io

import re
from concourse_common.common import *


def execute_sql_file(sql_file_path, db_handler):
    try:
        sql_contents = io.open(sql_file_path, "r", encoding='utf-8').readlines()
    except UnicodeDecodeError:
        try:
            sql_contents = io.open(sql_file_path, "r", encoding='latin1').readlines()
        except UnicodeDecodeError:
            log_error("SQL file needs to be encoded in either utf-8 or latin1")
            return -1

    try:
        statement = ""
        for line in sql_contents:
            line = line.strip()
            if line.startswith('--'):  # ignore sql comment lines
                continue

            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement += line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement += line
                log_info("Executing statement: {}".format(statement))
                db_handler.execute_multiple_db_commands(statement)
                statement = ""
    except Exception as e:
        db_handler.rollback()
        log_error(e)
        return -1
    db_handler.commit()
    return 0


def execute_sql_command(command, db_handler):
    try:
        log_info("Executing statement: {}".format(command))
        db_handler.execute_multiple_db_commands(command)
    except Exception as e:
        db_handler.rollback()
        log_error(e)
        return -1
    db_handler.commit()
    return 0
