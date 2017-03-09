class Executor:
    def __init__(self, db_handler, parser):
        self.db_handler = db_handler
        self.parser = parser

    def execute(self):
        self.database_operations()
        self.user_operations()
        self.grant_operations()

    def database_operations(self):
        for db in self.parser.db_create_list():
            self.db_handler.create_db(db)

        for db in self.parser.db_remove_list():
            self.db_handler.drop_db(db)

    def user_operations(self):
        for user in self.parser.user_create_list():
            user_name = user['USERNAME']
            password = user['PASSWORD']
            self.db_handler.create_user(user_name, password)

        for user in self.parser.user_remove_list():
            self.db_handler.drop_user(user)

    def grant_operations(self):
        for grant in self.parser.grant_all_list():
            user = grant['USER']
            db = grant['DATABASE']
            self.db_handler.grant_all_user_on_db(user, db)

        for grant in self.parser.grant_select_list():
            user = grant['USER']
            db = grant['DATABASE']
            self.db_handler.grant_select_user_on_db(user, db)

        for grant in self.parser.grant_select_table_list():
            user = grant['USER']
            db = grant['DATABASE']
            table = grant['TABLE']
            self.db_handler.grant_select_user_on_table(user, db, table)
