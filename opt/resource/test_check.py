
import unittest
from unittest.mock import patch

import check
from concourse_common import testutil


class TestCheck(unittest.TestCase):
    def test_invalid_json(self):
        testutil.put_stdin(
            """
            {
               "sourcez":{
                  "user": "user",
                  "password": "pw",
                  "host": "hostname"
               },
               "version":{
                  "version": ""
               }
            }
            """)

        self.assertEqual(check.execute(), -1)

    @patch("check.MySQLHandler")
    def test_valid_mysql(self, mock_mysql_handler):
        mock_actual_instance = mock_mysql_handler()
        io = testutil.mock_stdout()
        testutil.put_stdin(
            """
            {
               "source":{
                  "user": "user",
                  "password": "pw",
                  "host": "hostname"
               },
               "version":{
                  "version": "some-version"
               }
            }
            """)
        self.assertEqual(check.execute(), 0)
        mock_actual_instance.close_connection.assert_called_once()
        self.assertEqual(testutil.read_from_io(io), "[{}]")

    @patch("check.MySQLHandler")
    def test_invalid_mysql(self, mock_mysql_handler):
        mock_mysql_handler.return_value = None
        testutil.put_stdin(
            """
            {
               "source":{
                  "user": "user",
                  "password": "pw",
                  "host": "hostname"
               },
               "version":{
                  "version": "some-version"
               }
            }
            """)
        self.assertEqual(check.execute(), -1)

if __name__ == '__main__':
    unittest.main()