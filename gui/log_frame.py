from doctest import master

import customtkinter as ctk
from PIL import Image

class LogFrame:


    def __init__(self, master_frame, owner_object):

        self.owner_object = owner_object

        master_frame.grid_rowconfigure(0, weight=1)
        master_frame.grid_columnconfigure(0, weight=1)

        self.main_log_frame = ctk.CTkFrame(master=master_frame,
                                                    height=400,
                                                    width=550,
                                                    fg_color="transparent")

        self.main_log_frame.grid(row=0, column=0, sticky="nsew")

        self.left_scroll_log_frame = ctk.CTkFrame(master=self.main_log_frame, fg_color="transparent", width=110, height=400)
        self.left_scroll_log_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=20)

        self.log_separator = ctk.CTkFrame(self.main_log_frame, width=2, height=450, fg_color=self.owner_object.theme.theme_content['fg_table_separator'])
        self.log_separator.grid(row=0, column=1, sticky="ew")

        self.right_scroll_log_frame = ctk.CTkScrollableFrame(master=self.main_log_frame, fg_color="transparent", width=410, height=400)
        self.right_scroll_log_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=20)

        self.main_log_frame.grid_columnconfigure(0, weight=0, minsize=110)
        self.main_log_frame.grid_columnconfigure(1, weight=0, minsize=2)
        self.main_log_frame.grid_columnconfigure(2, weight=0, minsize=410)
        self.main_log_frame.grid_rowconfigure(0, weight=1)
           
           
    def add_left_part_log(self, index, text):

        self.label_count_afk = ctk.CTkLabel(master=self.left_scroll_log_frame,
                                            text=text,
                                            text_color="#",
                                            width=110,
                                            height=20)

        self.label_count_afk.grid(row=index, column=0, sticky="ew")


    def add_right_part_log(self, index, text, text_color):

        self.label_count_step = ctk.CTkLabel(master=self.right_scroll_log_frame,
                                            text=text,
                                            text_color=text_color,
                                            width=400,
                                            height=20,
                                            anchor="w")

        self.label_count_step.grid(row=index, column=0,  sticky="ew")

        self.owner_object.smmo_bot.index_log_message += 1

        self.right_scroll_log_frame._parent_canvas.yview_moveto(1)


    def add_right_part_log_kaptcha(self, index, path0, path1, path2, path3, text_answer, text_color):

        self.frame_last_kaptcha = ctk.CTkFrame(master=self.right_scroll_log_frame,
                                               width=400,
                                               height=25,
                                               fg_color="transparent")

        self.frame_last_kaptcha.grid(row=index, column=0, sticky="ew")

        self.frame_last_kaptcha.grid_columnconfigure(0, weight=0, minsize=70)
        self.frame_last_kaptcha.grid_columnconfigure(1, weight=0, minsize=70)
        self.frame_last_kaptcha.grid_columnconfigure(2, weight=0, minsize=70)
        self.frame_last_kaptcha.grid_columnconfigure(3, weight=0, minsize=70)
        self.frame_last_kaptcha.grid_columnconfigure(4, weight=0, minsize=120)

        image_convert = [Image.open(path0),
                        Image.open(path1),
                        Image.open(path2),
                        Image.open(path3)]

        for i in range(4):

            self.lable_photo = ctk.CTkLabel(master=self.frame_last_kaptcha,
                                            text="",
                                            image=ctk.CTkImage(dark_image=image_convert[i], light_image=image_convert[i]),
                                            width=60,
                                            height=25,
                                            fg_color="transparent")

            self.lable_photo.grid(row=0, column=i, sticky="ew")

        self.lable_text = ctk.CTkLabel(master=self.frame_last_kaptcha,
                                       text=text_answer,
                                       text_color=text_color,
                                       width=120,
                                       height=25,
                                       fg_color="transparent",
                                       anchor="w")

        self.lable_text.grid(row=0, column=4, sticky="ew")

        self.owner_object.smmo_bot.index_log_message += 1
        self.right_scroll_log_frame._parent_canvas.yview_moveto(1)