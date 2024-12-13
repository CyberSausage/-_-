
import customtkinter as ctk

from sMMO_Bot import Bot_sMMO_cl
from main import Tg_Bot

from gui.top_menu import TopMenu
from gui.setting_frame import SettingFrame
from gui.kaptcha_frame import KaptchaFrame
from gui.log_frame import LogFrame

from parse_theme import ParserTheme
from connect_to_db import DataBase

import threading


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.connDB = DataBase()

        self.theme = None

        self.get_and_update_theme()

        self.tg_bot = None
        self.smmo_bot = None
        self.smmo_bot_thread = None

        self.geometry("610x650")
        self.title("simple ботик")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)

        self.appearance_mode = ctk.set_appearance_mode("dark")
        self.default_color_theme = ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(master=self, text="")
        self.label.grid(row=0, column=0)

        self.top_menu_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.top_menu_frame.grid(row=1, column=0, padx=(20, 30), sticky="nsew")

        self.labelTopMenu = ctk.CTkLabel(master=self.top_menu_frame, text="")
        self.labelTopMenu.grid(row=0, column=0)

        self.add_top_menu()

        self.label.grid(row=2, column=0)

        self.add_table_frame()

        self.label_border = ctk.CTkLabel(master=self, text="", height=50)
        self.label_border.grid(row=4, column=0)

        self.grid_rowconfigure(3, weight=1)

        self.create_bot_and_tg_bot()


    def create_bot_and_tg_bot(self):
        status_tg_bot_and_local = self.connDB.select(nameTable="Params")[0]

        token = self.connDB.select(columns='token', nameTable='All_Token')
        api_token = self.connDB.select(columns='api_token', nameTable="All_Token")
        cookie = self.connDB.select(nameTable="Cookie")

        if not token or not api_token or not cookie:

            self.show_settings()
            self.settings_menu.show_setting_token()

        else:
            self.smmo_bot = Bot_sMMO_cl(self, token[0][0], api_token[0][0])

        if status_tg_bot_and_local[0] == 1:
            token_tg_bot = self.connDB.select(columns='token_tg_bot', nameTable="All_Token")

            if not token_tg_bot[0][0]:
                self.show_settings()
                self.settings_menu.show_setting_token()

            else:
                token_tg_bot = token_tg_bot[0][0]

                self.tg_bot = Tg_Bot(token_tg_bot)


    def get_and_update_theme(self):

        self.theme = ParserTheme(self.connDB.select(nameTable="All_Theme")[0][0])


    def add_top_menu(self):
        self.top_menu = TopMenu(self.top_menu_frame, self)


    def add_table_frame(self):
        self.table_frame = ctk.CTkFrame(master=self, height=400, width=550, fg_color=self.theme.theme_content['fg_table_frame'])
        self.table_frame.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")


    def start_smmo(self):
        token = self.connDB.select(columns='token', nameTable='All_Token')
        api_token = self.connDB.select(columns='api_token', nameTable="All_Token")
        api_tg_id = self.connDB.select(columns='api_tg_id', nameTable="All_Token")
        api_tg_hash = self.connDB.select(columns='api_tg_hash', nameTable="All_Token")
        cookie = self.connDB.select(nameTable="Cookie")

        if self.smmo_bot is None:
            self.create_bot_and_tg_bot()

            return None

        if not token or not api_token or not cookie:

            self.show_settings()
            self.settings_menu.show_setting_token()

        else:
            self.bot_sMMO_thread = threading.Thread(target=self.smmo_bot.main_run)

            self.show_log()
            self.log_menu.add_right_part_log(self.smmo_bot.index_log_message, "Старт.", "#7FFF00")

            self.bot_sMMO_thread.start()


    def stop_smmo(self):
        self.smmo_bot.stop()
        self.bot_sMMO_thread.join()

        self.smmo_bot.stop_event.clear()

        self.log_menu.add_right_part_log(self.smmo_bot.index_log_message, "Стоп.", "#B22222")


    def show_log(self):
        self.table_frame.destroy()
        self.add_table_frame()

        self.log_menu = LogFrame(self.table_frame, self)


    def show_kaptcha(self):
        self.table_frame.destroy()
        self.add_table_frame()

        self.kaptcha_menu = KaptchaFrame(self.table_frame, self)


    def show_settings(self):
        self.table_frame.destroy()
        self.add_table_frame()

        self.settings_menu = SettingFrame(self.table_frame, self)


    def clear_frame(self, frame):

        for widget in frame.winfo_children():
            widget.grid_forget()


if __name__ == '__main__':
    app = App()
    app.mainloop()
