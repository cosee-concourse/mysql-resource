#! /usr/bin/env python3

import yaml
from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
import statement_executor
from config_executor import ConfigExecutor
from config_parser import ConfigParser
from mysql_handler import MySQLHandler
from model import *


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.OUT)
    if not valid:
        return -1

    user = get_source_value(payload, USER_KEY)
    password = get_source_value(payload, PASSWORD_KEY)
    host = get_source_value(payload, HOST_KEY)

    sql_file = get_params_value(payload, SQL_FILE_KEY)
    config_file = get_params_value(payload, CONFIG_FILE_KEY)
    command = get_params_value(payload, COMMAND_KEY)

    operation_list = []

    if sql_file is not None:
        operation_list.append((execute_sql_file, [directory, sql_file]))

    if config_file is not None:
        operation_list.append((execute_configuration_file, [directory, config_file]))

    if command is not None:
        operation_list.append((execute_sql_command, [command]))

    if len(operation_list) is 0:
        log_error("No operation specified")
        return -1

    return_value = execute_operations(operation_list, user, password, host)

    if return_value is 0:
        print(get_version_output("no-version", VERSION_KEY_NAME))
        return 0
    else:
        return return_value


def execute_operations(operation_list, user, password, host):
    for operation in operation_list:
        with MySQLHandler(user, password, host) as db_handler:
            method = operation[0]
            return_value = method(*operation[1], db_handler)
        if return_value is not 0:
            return return_value
    return 0


def execute_configuration_file(directory, config_file, db_handler):
    config_file_path = join_paths(directory, config_file)

    if not validate_path(config_file_path):
        log_error("Config file not found")
        return -1

    with open(config_file_path, 'r') as stream:
        yaml_dict = yaml.load(stream)
        parser = ConfigParser(yaml_dict)
        db_executor = ConfigExecutor(db_handler, parser)
        db_executor.execute()

    return 0


def execute_sql_file(directory, sql_file, db_handler):
    sql_file_path = join_paths(directory, sql_file)

    if not validate_path(sql_file_path):
        log_error("SQL script file not found")
        return -1

    return_value = statement_executor.execute_sql_file(sql_file_path, db_handler)
    return return_value


def execute_sql_command(command, db_handler):
    return_value = statement_executor.execute_transaction(db_handler, command)
    return return_value


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
