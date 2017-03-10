#! /usr/bin/env python3

from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from model import *

import yaml

from parser import Parser
from dbexecutor import Executor
from dbhandler import DBHandler


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.OUT)
    if not valid:
        return -1

    config_file_path = join_paths(directory, get_params_value(payload, CONFIG_FILE_KEY))

    if not validate_path(config_file_path):
        log_error("Config file not found")
        return -1

    user = get_source_value(payload, USER_KEY)
    password = get_source_value(payload, PASSWORD_KEY)
    host = get_source_value(payload, HOST_KEY)

    with open(config_file_path, 'r') as stream:
        yaml_dict = yaml.load(stream)
        with DBHandler(user, password, host) as db_handler:
            parser = Parser(yaml_dict)
            db_executor = Executor(db_handler, parser)
            db_executor.execute()

    print(get_version_output("no-version",VERSION_KEY_NAME))

    return 0


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
