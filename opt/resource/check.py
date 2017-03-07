#! /usr/bin/env python3
from concourse_common.jsonutil import *
import schemas
import dbhandler
from model import *


def execute():
    valid, payload = load_and_validate_payload(schemas, Request.CHECK)
    if not valid:
        return -1

    dbhandler.connect(get_source_value(payload, USER_KEY), get_source_value(payload, PASSWORD_KEY), get_source_value(payload, HOST_KEY))

    print([{}])

    return 0

if __name__ == '__main__':
    exit(execute())
