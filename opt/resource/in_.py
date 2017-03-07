#! /usr/bin/env python3

from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from model import *


def execute(directory):
    print([{}])

    return 0

if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
