from PIL import Image

import customtkinter as ctk

class KaptchaFrame:


    def __init__(self, master_frame, owner_object):

        self.owner_object = owner_object

        self.title_kaptcha_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=110, height=400)
        self.title_kaptcha_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        self.get_rowconfigure(self.title_kaptcha_frame)

        self.photo1_kaptcha_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=90, height=400)
        self.photo1_kaptcha_frame.grid(row=0, column=1, sticky="nsew", pady=5)
        self.get_rowconfigure(self.photo1_kaptcha_frame)

        self.photo2_kaptcha_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=90, height=400)
        self.photo2_kaptcha_frame.grid(row=0, column=2, sticky="nsew", pady=5)
        self.get_rowconfigure(self.photo2_kaptcha_frame)

        self.photo3_kaptcha_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=90, height=400)
        self.photo3_kaptcha_frame.grid(row=0, column=3, sticky="nsew", pady=5)
        self.get_rowconfigure(self.photo3_kaptcha_frame)

        self.photo4_kaptcha_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=90, height=400)
        self.photo4_kaptcha_frame.grid(row=0, column=4, sticky="nsew", pady=5)
        self.get_rowconfigure(self.photo4_kaptcha_frame)

        self.answer_kaptcha_frame = ctk.CTkFrame(master=master_frame, fg_color="transparent", width=100, height=400)
        self.answer_kaptcha_frame.grid(row=0, column=5, sticky="nsew", pady=5)
        self.get_rowconfigure(self.answer_kaptcha_frame)

        master_frame.grid_columnconfigure(0, weight=0, minsize=110)
        master_frame.grid_columnconfigure(1, weight=0, minsize=90)
        master_frame.grid_columnconfigure(2, weight=0, minsize=90)
        master_frame.grid_columnconfigure(3, weight=0, minsize=90)
        master_frame.grid_columnconfigure(4, weight=0, minsize=90)
        master_frame.grid_columnconfigure(5, weight=0, minsize=100)
        master_frame.grid_rowconfigure(0, weight=1)

        for i in range(0, 15):
            self.add_new_string("Пример", "generate_image_uid_0.png", "generate_image_uid_0.png", 'generate_image_uid_0.png', "generate_image_uid_0.png", "ответ 1")
        self.add_new_string("Пример", "generate_image_uid_0.png", "generate_image_uid_0.png",
                            'generate_image_uid_0.png', "generate_image_uid_0.png", "ответ 1")

    def get_rowconfigure(self, parent):
        for i in range(16):
            parent.grid_rowconfigure(i, weight=1)


    def add_new_string(self, title, path1, path2, path3, path4, answer):

        list_title_frame_children = self.title_kaptcha_frame.winfo_children()
        count_frame_children = len(list_title_frame_children)

        if count_frame_children == 16:
            list_title_frame_children[0].destroy()

            for index, child in enumerate(list_title_frame_children):
                child.grid(row=index, column=0, sticky="nsew", padx=5, pady=5)

            self.add_constructor(15, title, path1, path2, path3, path4, answer)

        else:
            self.add_constructor(count_frame_children, title, path1, path2, path3, path4, answer)


    def add_constructor(self, row, title, path1, path2, path3, path4, answer):
        self.add_title_kaptcha(title_text=title, row=row)
        self.add_photo_kaptcha(row=row, frame_parent=self.photo1_kaptcha_frame, path=path1)
        self.add_photo_kaptcha(row=row, frame_parent=self.photo2_kaptcha_frame, path=path2)
        self.add_photo_kaptcha(row=row, frame_parent=self.photo3_kaptcha_frame, path=path3)
        self.add_photo_kaptcha(row=row, frame_parent=self.photo4_kaptcha_frame, path=path4)
        self.add_answer_kaptcha(answer_text=answer, row=row)


    def add_title_kaptcha(self, title_text, row):
        self.title_kaptcha_label = ctk.CTkLabel(master=self.title_kaptcha_frame,
                                                text=title_text,
                                                text_color=self.owner_object.theme.theme_content['text_color'],
                                                width=100,
                                                height=20)

        self.title_kaptcha_label.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)


    def add_photo_kaptcha(self, row, frame_parent, path="generate_image_uid_1.png"):
        image_kaptcha_ex = Image.open(path)
        self.photo_kaptcha = ctk.CTkLabel(master=frame_parent,
                                                text="",
                                                image=ctk.CTkImage(dark_image=image_kaptcha_ex, light_image=image_kaptcha_ex),
                                                width=80,
                                                height=30)
        self.photo_kaptcha.grid(row=row, column=0, sticky="nsew", padx=5)


    def add_answer_kaptcha(self, answer_text, row):
        self.title_kaptcha_label = ctk.CTkLabel(master=self.answer_kaptcha_frame,
                                                text=answer_text,
                                                text_color=self.owner_object.theme.theme_content['text_color'],
                                                width=100,
                                                height=20)

        self.title_kaptcha_label.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)