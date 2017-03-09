import unittest

from concourse_common import testutil

import out


class TestOut(unittest.TestCase):
    def test_invalid_json(self):
        testutil.put_stdin(
            """
            {
              "source": {
                "user": "user",
                "password": "password",
                "host": "hostname"
              },
              "params": {
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    def test_params_required_json(self):
        testutil.put_stdin(
            """
            {
              "source": {
                "user": "user",
                "password": "password",
                "host": "hostname"
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

