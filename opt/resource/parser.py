
class Parser:
    def __init__(self, yaml):
        self.yaml = yaml

    def db_create_list(self):
        return self.yaml['DATABASES']['CREATE']

    def db_remove_list(self):
        return self.yaml['DATABASES']['REMOVE']

    def user_create_list(self):
        return self.yaml['USERS']['CREATE']

    def user_remove_list(self):
        return self.yaml['USERS']['REMOVE']

    def grant_all_list(self):
        return self.yaml['USERS']['GRANT-ALL']

    def grant_select_list(self):
        return self.yaml['USERS']['GRANT-SELECT']

    def grant_select_table_list(self):
        return self.yaml['USERS']['GRANT-SELECT-TABLE']
