
import os


class SettingFunctions:

    def __init__(self, owner_object, connDB, theme):

        self.owner_object = owner_object
        self.theme = theme
        self.connDB = connDB


    def select_params(self):
        try:
            data_checkbox = self.connDB.select(nameTable="Params")[0]

            return data_checkbox

        except:

            return [0, 0]


    def update_params(self):

        data_now = self.connDB.select(nameTable="Params")

        if not data_now:
            self.connDB.insert(nameTable="Params", nameColumn="telegram, desktop", valueColumn=f"{self.owner_object.check_telegram.get()}, {self.owner_object.check_desktop.get()}")

        else:
            self.connDB.update(nameTable="Params", columns_val=f"telegram={self.owner_object.check_telegram.get()}, desktop={self.owner_object.check_desktop.get()}")


    def select_tokens(self):
        pass


    def get_all_themes(self):

        list_name_theme = os.listdir("themes")
        dict_content_theme = {}

        for name in list_name_theme:

            content = self.theme.return_theme_content(name)

            dict_content_theme[content['theme_name']] = content['app_color']

        return dict_content_theme


    def update_theme(self, new_theme="Violet Dark"):

        self.connDB.update(nameTable="All_Theme", columns_val=f"theme_now='{new_theme}'", )