import customtkinter as ctk

from gui.setting_functions import SettingFunctions

class SettingFrame:


    def __init__(self, master_frame, owner_object):

        self.functions = SettingFunctions(self, owner_object.connDB, owner_object.theme)

        self.owner_object = owner_object

        self.left_setting_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=120, height=400)
        self.left_setting_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=20)

        self.separator = ctk.CTkFrame(master_frame, width=2, height=450, fg_color=self.owner_object.theme.theme_content['fg_table_separator'])
        self.separator.grid(row=0, column=1, padx=5)

        self.right_setting_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=480, height=400)
        self.right_setting_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=20)

        master_frame.grid_columnconfigure(0, weight=0, minsize=120)
        master_frame.grid_columnconfigure(1, weight=0, minsize=2)
        master_frame.grid_columnconfigure(2, weight=0, minsize=480)
        master_frame.grid_rowconfigure(0, weight=1)

        self.setting_menu_setup()
        self.show_setting_params()


    def setting_menu_setup(self):
        # left_setting_frame

        self.left_setting_frame.grid_columnconfigure(0, weight=1)

        self.btn_setting_params = ctk.CTkButton(master=self.left_setting_frame,
                                                text="Параметры",
                                                text_color=self.owner_object.theme.theme_content['text_color'],
                                                width=110,
                                                command=self.show_setting_params,
                                                fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                                hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
        self.btn_setting_params.grid(row=0, column=1, pady=(0, 5), sticky="ew")

        self.btn_setting_token = ctk.CTkButton(master=self.left_setting_frame,
                                               text="Токены",
                                               text_color=self.owner_object.theme.theme_content['text_color'],
                                               width=110,
                                               command=self.show_setting_token,
                                               fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                               hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
        self.btn_setting_token.grid(row=1, column=1, pady=(0, 5), sticky="ew")

        self.btn_setting_themes = ctk.CTkButton(master=self.left_setting_frame,
                                                text="Темы",
                                                text_color=self.owner_object.theme.theme_content['text_color'],
                                                width=110,
                                                command=self.show_setting_themes,
                                                fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                                hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
        self.btn_setting_themes.grid(row=2, column=1, pady=(0, 5), sticky="ew")


    def clear_and_added_right_settings_frame(self, fg_color=""):
        self.owner_object.clear_frame(self.right_setting_frame)

        right_sett_frame = ctk.CTkFrame(master=self.right_setting_frame, fg_color=f"{'transparent' if fg_color == '' else fg_color}",
                                                        width=480, height=400)
        right_sett_frame.grid(row=0, column=0, sticky="nsew")

        return right_sett_frame


    # right_setting_frame

    def show_setting_params(self):
        data_checkbox = self.functions.select_params()

        self.right_params_setting_frame = self.clear_and_added_right_settings_frame()

        self.right_params_setting_frame.grid_columnconfigure(0, weight=1)
        self.right_params_setting_frame.grid_columnconfigure(1, weight=1)
        self.right_params_setting_frame.grid_rowconfigure(0, weight=1)
        self.right_params_setting_frame.grid_rowconfigure(1, weight=6)

        self.check_telegram = ctk.CTkCheckBox(master=self.right_params_setting_frame,
                                              text="Телеграмм бот",
                                              text_color=self.owner_object.theme.theme_content['text_color'],
                                              width=150,
                                              command=self.functions.update_params,
                                              variable=ctk.IntVar(value=data_checkbox[0]),
                                              fg_color=self.owner_object.theme.theme_content['fg_checkbox'],
                                              border_color=self.owner_object.theme.theme_content['border_color_checkbox'],
                                              hover_color=self.owner_object.theme.theme_content['hover_color_checkbox'])
        self.check_telegram.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.check_desktop = ctk.CTkCheckBox(master=self.right_params_setting_frame,
                                             text="Локально",
                                             text_color=self.owner_object.theme.theme_content['text_color'],
                                             width=150,
                                             command=self.functions.update_params,
                                             variable=ctk.IntVar(value=data_checkbox[1]),
                                             fg_color=self.owner_object.theme.theme_content['fg_checkbox'],
                                             border_color=self.owner_object.theme.theme_content['border_color_checkbox'],
                                             hover_color=self.owner_object.theme.theme_content['hover_color_checkbox'])
        self.check_desktop.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="nsew")


    def show_setting_token(self):

        self.right_token_setting_frame = self.clear_and_added_right_settings_frame()

        self.right_token_setting_frame.grid_columnconfigure(0, weight=0, minsize=300)
        self.right_token_setting_frame.grid_columnconfigure(1, weight=0, minsize=100)
        self.right_token_setting_frame.grid_rowconfigure(0, weight=1)
        self.right_token_setting_frame.grid_rowconfigure(1, weight=1)
        self.right_token_setting_frame.grid_rowconfigure(2, weight=25)

        self.input_token = ctk.CTkEntry(master=self.right_token_setting_frame,
                                        placeholder_text="Token",
                                        placeholder_text_color=self.owner_object.theme.theme_content['placeholder_color_input'],
                                        text_color=self.owner_object.theme.theme_content['text_color'],
                                        width=150,
                                        height=20,
                                        fg_color=self.owner_object.theme.theme_content['fg_color_input'],
                                        border_color=self.owner_object.theme.theme_content['border_color_input'])

        self.input_token.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.btn_token_change = ctk.CTkButton(master=self.right_token_setting_frame, text="Записать",
                                              text_color=self.owner_object.theme.theme_content['text_color'], width=100, height=20,
                                              command=self.show_setting_params,
                                              fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                              hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
        self.btn_token_change.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.input_api_token = ctk.CTkEntry(master=self.right_token_setting_frame,
                                            placeholder_text="Api Token",
                                            placeholder_text_color=self.owner_object.theme.theme_content['placeholder_color_input'],
                                            text_color=self.owner_object.theme.theme_content['text_color'],
                                            width=150,
                                            height=20,
                                            fg_color=self.owner_object.theme.theme_content['fg_color_input'],
                                            border_color=self.owner_object.theme.theme_content['border_color_input'])

        self.input_api_token.grid(row=1, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.btn_api_token_change = ctk.CTkButton(master=self.right_token_setting_frame, text="Записать",
                                                  text_color=self.owner_object.theme.theme_content['text_color'], width=100, height=20,
                                                  command=self.show_setting_params,
                                                  fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                                  hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
        self.btn_api_token_change.grid(row=1, column=1, padx=(0, 5), pady=(0, 5), sticky="nsew")

        data_checkbox = self.functions.select_params()[0]

        if data_checkbox:
            self.input_id_tg_bot = ctk.CTkEntry(master=self.right_token_setting_frame,
                                                placeholder_text="Bot ID with https://my.telegram.org/apps",
                                                placeholder_text_color=self.owner_object.theme.theme_content['placeholder_color_input'],
                                                text_color=self.owner_object.theme.theme_content['text_color'],
                                                width=150,
                                                height=20,
                                                fg_color=self.owner_object.theme.theme_content['fg_color_input'],
                                                border_color=self.owner_object.theme.theme_content['border_color_input'])

            self.input_id_tg_bot.grid(row=3, column=0, padx=(0, 5), pady=(25, 5), sticky="nsew")

            self.btn_api_token_change = ctk.CTkButton(master=self.right_token_setting_frame, text="Записать",
                                                      text_color=self.owner_object.theme.theme_content['text_color'], width=100, height=20,
                                                      command=self.show_setting_params,
                                                      fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                                      hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
            self.btn_api_token_change.grid(row=3, column=1, padx=(0, 5), pady=(25, 5), sticky="nsew")

            self.input_id_tg_bot = ctk.CTkEntry(master=self.right_token_setting_frame,
                                                placeholder_text="Bot hash with https://my.telegram.org/apps",
                                                placeholder_text_color=self.owner_object.theme.theme_content['placeholder_color_input'],
                                                text_color=self.owner_object.theme.theme_content['text_color'],
                                                width=150,
                                                height=20,
                                                fg_color=self.owner_object.theme.theme_content['fg_color_input'],
                                                border_color=self.owner_object.theme.theme_content['border_color_input'])

            self.input_id_tg_bot.grid(row=4, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

            self.btn_api_token_change = ctk.CTkButton(master=self.right_token_setting_frame, text="Записать",
                                                      text_color=self.owner_object.theme.theme_content['text_color'], width=100, height=20,
                                                      command=self.show_setting_params,
                                                      fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                                      hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
            self.btn_api_token_change.grid(row=4, column=1, padx=(0, 5), pady=(0, 5), sticky="nsew")

            self.input_token_tg_bot = ctk.CTkEntry(master=self.right_token_setting_frame,
                                                   placeholder_text="Tg bot Token",
                                                   placeholder_text_color=self.owner_object.theme.theme_content['placeholder_color_input'],
                                                   text_color=self.owner_object.theme.theme_content['text_color'],
                                                   width=150,
                                                   height=20,
                                                   fg_color=self.owner_object.theme.theme_content['fg_color_input'],
                                                   border_color=self.owner_object.theme.theme_content['border_color_input'])

            self.input_token_tg_bot.grid(row=5, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

            self.btn_api_token_change = ctk.CTkButton(master=self.right_token_setting_frame, text="Записать",
                                                      text_color=self.owner_object.theme.theme_content['text_color'], width=100, height=20,
                                                      command=self.show_setting_params,
                                                      fg_color=self.owner_object.theme.theme_content['fg_btn_table'],
                                                      hover_color=self.owner_object.theme.theme_content['fg_hover_btn_table'])
            self.btn_api_token_change.grid(row=5, column=1, padx=(0, 5), pady=(0, 5), sticky="nsew")


    def show_setting_themes(self):
        self.owner_object.clear_frame(self.right_setting_frame)

        self.right_themes_setting_frame = self.clear_and_added_right_settings_frame(fg_color="#303030")

        self.right_themes_setting_frame.grid_columnconfigure(0, weight=0, minsize=200)
        self.right_themes_setting_frame.grid_columnconfigure(1, weight=0, minsize=200)
        self.right_themes_setting_frame.grid_rowconfigure(0, weight=0, minsize=90)
        self.right_themes_setting_frame.grid_rowconfigure(1, weight=0, minsize=90)
        self.right_themes_setting_frame.grid_rowconfigure(2, weight=0, minsize=90)
        self.right_themes_setting_frame.grid_rowconfigure(3, weight=0, minsize=90)

        dict_themes_content = self.functions.get_all_themes()
        list_names = str(dict_themes_content.keys()).split("['")[1].replace("', '", ",").replace("'])", "").split(",")
        number = 0
        self.list_btn = []

        for column in range(2):

            for row in range(4):

                text = list_names[number]
                text_color = dict_themes_content[text]['text_color']
                fg_color_label = dict_themes_content[text]['fg_color_input']
                fg_checkbox = dict_themes_content[text]['fg_checkbox']
                border_color_checkbox = dict_themes_content[text]['border_color_checkbox']
                hover_color_checkbox = dict_themes_content[text]['hover_color_checkbox']
                fg_btn_table = dict_themes_content[text]['fg_btn_table']
                fg_hover_btn_table = dict_themes_content[text]['fg_hover_btn_table']
                border_btn_table = dict_themes_content[text]['border_color_input']


                self.theme_frame = ctk.CTkFrame(master=self.right_themes_setting_frame,
                                                    fg_color="#121212",
                                                    width=200, height=90)
                self.theme_frame.grid(row=row, column=column, padx=(5, 5), pady=5, sticky="nsew")

                self.theme_frame.grid_columnconfigure(0, weight=0, minsize=100)
                self.theme_frame.grid_columnconfigure(1, weight=0, minsize=70)
                self.theme_frame.grid_rowconfigure(0, weight=0, minsize=45)
                self.theme_frame.grid_rowconfigure(1, weight=1, minsize=45)

                self.title_theme = ctk.CTkLabel(master=self.theme_frame,
                                                text=text,
                                                text_color=text_color,
                                                fg_color=fg_color_label,
                                                height=25)
                self.title_theme.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="nsew")

                self.check_theme = ctk.CTkCheckBox(master=self.theme_frame,
                                                      text="Тыкни",
                                                      text_color=text_color,
                                                      fg_color=fg_checkbox,
                                                      border_color=border_color_checkbox,
                                                      hover_color=hover_color_checkbox)
                self.check_theme.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

                self.btn_theme_agree = ctk.CTkButton(master=self.theme_frame,
                                                     text="Применить",
                                                     text_color=text_color,
                                                     fg_color=fg_btn_table,
                                                     hover_color=fg_hover_btn_table,
                                                     border_color=border_btn_table,
                                                     border_width=1,
                                                     command=lambda col=column, rw=row: self.new_theme(col * 4 + rw),
                                                     height=20,
                                                     width=60)
                self.btn_theme_agree.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

                number += 1
                self.list_btn.append(self.btn_theme_agree)


    def new_theme(self, number_btn=0):

        parent_name = self.list_btn[number_btn].winfo_parent()
        parent = self.owner_object.nametowidget(parent_name)

        title_theme_object = parent.winfo_children()[0]
        title_theme_info = title_theme_object.cget("text")

        print(title_theme_info)

        self.functions.update_theme(new_theme=title_theme_info)

        self.owner_object.get_and_update_theme()

        self.owner_object.show_settings()