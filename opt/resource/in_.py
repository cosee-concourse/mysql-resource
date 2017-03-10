#! /usr/bin/env python3

from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from model import *


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.IN)
    if not valid:
        return -1

    version = get_version(payload, VERSION_KEY_NAME)
    if version is None:
        print({})
    else:
        print(get_version_output(version, VERSION_KEY_NAME))

    return 0

if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
