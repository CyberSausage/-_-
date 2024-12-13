
import json


class ParserTheme:


    def __init__(self, name_theme):

        self.name = name_theme
        self.dictionary = {}

        self.get_theme()

        self.theme_name = self.dictionary['theme_name']
        self.theme_content = self.dictionary['app_color']


    def get_theme(self):

        with open(f"themes/{self.name.replace(' ', '_')}_theme.json", "r", encoding='utf-8') as file:

            theme_content = json.loads(file.read())
            self.dictionary = theme_content


    def return_theme_content(self, name):

        with open(f"themes/{name}", "r", encoding="utf-8") as file:
            theme_content = json.loads(file.read())

            return theme_content


if __name__ == "__main__":

    pars_ex = ParserTheme("violet")
    pars_ex.get_theme()