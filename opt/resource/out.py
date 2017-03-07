#! /usr/bin/env python3

from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from model import *

import yaml


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.OUT)
    if not valid:
        return -1

    config_file_path = join_paths(directory, get_params_value(payload, CONFIG_FILE_KEY))

    if not validate_path(config_file_path):
        log_error("Config file not found")
        return -1

    with open(config_file_path, 'r') as stream:
        yaml_dict = yaml.load(stream)
        # TODO: parse yaml here and execute commands

    print([{}])

    return 0


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
