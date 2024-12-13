
import sqlite3


class DataBase:


    def __init__(self):
        super().__init__()

        self.connect = sqlite3.connect("smmo_DB.db")
        self.cursor = self.connect.cursor()


    def select(self, columns="*", nameTable="", condition_select=""):
        self.cursor.execute(f'''select {columns} from {nameTable}{condition_select if condition_select == "" else f" where {condition_select}"}''')
        resoult = self.cursor.fetchall()

        return resoult


    def update(self, nameTable="", columns_val="", condition_update=""):
        self.cursor.execute(f'''update {nameTable} set {columns_val} {condition_update if condition_update == "" else f" where {condition_update}"}''')
        self.connect.commit()


    def insert(self, nameTable="", nameColumn="", valueColumn=""):
        self.cursor.execute(f'''insert into {nameTable} ({nameColumn}) values ({valueColumn})''')
        self.connect.commit()


    def delete(self, nameTable="", condition_delete=""):
        self.cursor.execute(f'''delete from {nameTable} where {condition_delete}''')
        self.connect.commit()