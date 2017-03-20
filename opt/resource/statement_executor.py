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

    statement_list = parse_statements(sql_contents)
    return execute_transaction(db_handler, statement_list)


def parse_statements(sql_file_contents):
    statement_list = []
    statement = ""
    for line in sql_file_contents:
        line = line.strip()
        if line.startswith('--'):  # ignore sql comment lines
            continue

        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement += line
        else:  # when you get a line ending in ';' then add statement to list and reset for next statement
            statement += line
            statement_list.append(statement)
            statement = ""
    return statement_list


def execute_transaction(db_handler, *statements):
    try:
        for statement in statements:
            execute_statement(statement, db_handler)
    except Exception as e:
        db_handler.rollback()
        log_error(e)
        return -1
    db_handler.commit()
    return 0


def execute_statement(statement, db_handler):
    log_info("Executing statement: {}".format(statement))
    db_handler.execute_multiple_db_commands(statement)
