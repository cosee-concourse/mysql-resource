import unittest
from io import TextIOWrapper
from unittest.mock import MagicMock, patch

import in_
from concourse_common import testutil


class TestInput(unittest.TestCase):

    def test_returns_valid_json(self):
        testutil.put_stdin(
            """
            {
              "source": {
                "user": "user",
                "password": "pw",
                "host": "hostname"
              },
              "version": {
                "version": "some-version"
              }
            }
            """)
        io = testutil.mock_stdout()
        self.assertEqual(in_.execute('/'), 0)
        self.assertEqual(testutil.read_from_io(io), "[{}]")
