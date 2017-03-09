import unittest

from concourse_common import testutil

import parser

import yaml


class TestParser(unittest.TestCase):
    yaml_string = \
        """
        DATABASES:
            CREATE:
                - database-name1
                - database-name2
            REMOVE:
                - database-name3
                - database-name4
        USERS:
            CREATE:
                - USERNAME: username1
                  PASSWORD: password1
                - USERNAME: username2
                  PASSWORD: password2
            REMOVE:
                - username3
                - username4
            GRANT-ALL:
                - USER: username1
                  DATABASE: database-name1
                - USER: username1
                  DATABASE: database-name2
            GRANT-SELECT:
                - USER: username2
                  DATABASE: database-name1
                - USER: username2
                  DATABASE: database-name2
            GRANT-SELECT-TABLE:
                - USER: username1
                  DATABASE: database-name1
                  TABLE: table-name
                - USER: username2
                  DATABASE: database-name1
                  TABLE: table-name
        """

    def setUp(self):
        self.uut = parser.Parser(yaml.load(self.yaml_string))

    def test_db_create_list(self):
        expected = ['database-name1', 'database-name2']
        self.assertEqual(self.uut.db_create_list(), expected)

    def test_db_remove_list(self):
        expected = ['database-name3', 'database-name4']
        self.assertEqual(self.uut.db_remove_list(), expected)

    def test_user_create_list(self):
        expected = [
            {'USERNAME': 'username1',
             'PASSWORD': 'password1'},
            {'USERNAME': 'username2',
             'PASSWORD': 'password2'}
        ]
        self.assertEqual(self.uut.user_create_list(), expected)

    def test_user_remove_list(self):
        expected = ['username3', 'username4']
        self.assertEqual(self.uut.user_remove_list(), expected)

    def test_grant_all_list(self):
        expected = [
            {'USER': 'username1',
             'DATABASE': 'database-name1'},
            {'USER': 'username1',
             'DATABASE': 'database-name2'}
        ]
        self.assertEqual(self.uut.grant_all_list(), expected)

    def test_grant_select_list(self):
        expected = [
            {'USER': 'username2',
             'DATABASE': 'database-name1'},
            {'USER': 'username2',
             'DATABASE': 'database-name2'}
        ]
        self.assertEqual(self.uut.grant_select_list(), expected)

    def test_grant_select_table_list(self):
        expected = [
            {'USER': 'username1',
             'DATABASE': 'database-name1',
             'TABLE': 'table-name'},
            {'USER': 'username2',
             'DATABASE': 'database-name1',
             'TABLE': 'table-name'}
        ]
        self.assertEqual(self.uut.grant_select_table_list(), expected)