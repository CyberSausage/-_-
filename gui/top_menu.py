import customtkinter as ctk

from PIL import Image

class TopMenu:


    def __init__(self, master_frame, owner_object):

        self.btn_start = ctk.CTkButton(master=master_frame,
                                       text="Старт",
                                       width=100,
                                       command=owner_object.start_smmo,
                                       fg_color="#008000",
                                       hover_color="#016301")
        self.btn_start.grid(row=1, column=0, padx=(0, 15))

        self.btn_stop = ctk.CTkButton(master=master_frame,
                                      text="Стоп",
                                      width=100,
                                      command=owner_object.stop_smmo,
                                      fg_color="#8B0000",
                                      hover_color="#6e0202")
        self.btn_stop.grid(row=1, column=1, padx=(0, 15))

        log_image = Image.open("log.png")

        self.btn_log = ctk.CTkButton(master=master_frame,
                                     text="Лог",
                                     text_color="#4f9521",
                                     width=100,
                                     command=owner_object.show_log,
                                     fg_color="#000000",
                                     hover_color="#1f1e1e",
                                     image=ctk.CTkImage(dark_image=log_image, size=log_image.size))
        self.btn_log.grid(row=1, column=2, padx=(0, 15))

        self.btn_captch = ctk.CTkButton(master=master_frame, text="Капча", width=100, command=owner_object.show_kaptcha)
        self.btn_captch.grid(row=1, column=3, padx=(0, 15))

        self.btn_setting = ctk.CTkButton(master=master_frame,
                                         text="Настройки",
                                         width=100,
                                         command=owner_object.show_settings,
                                         fg_color="#2F4F4F",
                                         hover_color="#203636")
        self.btn_setting.grid(row=1, column=4, padx=(0, 15))