import sqlite3

from connect_to_db import DataBase

class crerate_BataDase:


    def __init__(self):
        super().__init__()

        self.connect = sqlite3.connect("smmo_DB.db")
        self.cursor = self.connect.cursor()


    def create_table_params(self):
        self.cursor.execute('''create table Params
        (telegram bool,
        desktop bool)''')


    def create_themes(self):
        self.cursor.execute('''create table All_Theme
        (theme_now text)''')


    def create_table_token(self):
        self.cursor.execute('''create table All_Token
        (token_tg_bot text primary key,
        token text,
        api_token text,
        api_tg_id text,
        api_tg_hash text)''')


    def create_table_cookie(self):
        self.cursor.execute('''create table Cookie
        (cookie text)''')


    def create_full(self):
        self.create_table_params()
        self.create_themes()
        self.create_table_token()
        self.create_table_cookie()


if __name__ == "__main__":
    obj_DB = crerate_BataDase()
    obj_DB.create_full()

    ob_DB = DataBase()
    print(ob_DB.select(nameTable="All_Theme"))
    ob_DB.insert(nameTable="All_Theme", nameColumn="theme_now", valueColumn="'Violet Dark'")