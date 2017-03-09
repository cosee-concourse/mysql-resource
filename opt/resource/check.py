#! /usr/bin/env python3
from concourse_common.jsonutil import *
import schemas
from dbhandler import DBHandler
from model import *


def execute():
    valid, payload = load_and_validate_payload(schemas, Request.CHECK)
    if not valid:
        return -1

    db_handler = DBHandler(get_source_value(payload, USER_KEY), get_source_value(payload, PASSWORD_KEY), get_source_value(payload, HOST_KEY))

    if db_handler is None:
        return -1
    else:
        db_handler.close_connection()

    print([{}])

    return 0

if __name__ == '__main__':
    exit(execute())
