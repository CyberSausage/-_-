import telebot
from telebot.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InputMediaPhoto, CallbackQuery

import threading

from All_Token import token_tg_bot
from sMMO_Bot import Bot_sMMO_cl

class Tg_Bot(telebot.TeleBot):

    def __init__(self, token):
        super().__init__(token)

        self.message_handler(commands=['start'])(self.send_welcome)
        self.message_handler(func=lambda message : message.text == "Старт sMMO")(self.start_sMMO)
        self.message_handler(func=lambda message : message.text == "Стоп sMMO")(self.stop_sMMO)
        self.message_handler(func=lambda message : message.text == "Стата")(self.get_stat)

        self.message_handler(func=lambda message : message.text == "1" or message.text == "2" or
                             message.text == "3" or message.text == "4")(self.callback_query)

        self.bot_sMMO = Bot_sMMO_cl(self)
        self.bot_sMMO_thread = None
        self.chat_id = None
        self.kapcha_number = None


    def send_welcome(self, message:Message):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Старт sMMO"),
                     KeyboardButton("Стоп sMMO"),
                     KeyboardButton("Стата"))

        self.reply_to(message, "Работаю...")
        self.send_message(message.chat.id, text="Жмай чё-то ._.", reply_markup=keyboard)


    def get_stat(self, message):
        self.reply_to(message, message.text)


    def run_bot(self):
        self.polling(none_stop=True)
        print(self.event_handler)


    def start_sMMO(self, message: Message):

        self.bot_sMMO_thread = threading.Thread(target=self.bot_sMMO.main_run)
        self.bot_sMMO_thread.start()

        self.chat_id = message.chat.id
        self.reply_to(message, "sMMO запущен.")

    def stop_sMMO(self, message):

        self.bot_sMMO.stop()
        self.bot_sMMO_thread.join()

        self.bot_sMMO.stop_event.clear()

        self.reply_to(message, "sMMO остановлен.")


    def send_photos(self, title):

        media_group = [
            InputMediaPhoto(open("/home/stanislav/PycharmProjects/SimpleMMObot/generate_image_uid_0.png", 'rb')),
            InputMediaPhoto(open("/home/stanislav/PycharmProjects/SimpleMMObot/generate_image_uid_1.png", 'rb')),
            InputMediaPhoto(open("/home/stanislav/PycharmProjects/SimpleMMObot/generate_image_uid_2.png", 'rb')),
            InputMediaPhoto(open('/home/stanislav/PycharmProjects/SimpleMMObot/generate_image_uid_3.png', 'rb'))
        ]

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        keyboard.add(KeyboardButton("1"),
                     KeyboardButton("2"),
                     KeyboardButton("3"),
                     KeyboardButton("4"))

        self.send_media_group(self.chat_id, media_group)
        self.send_message(self.chat_id, text=title, reply_markup=keyboard)

    def callback_query(self, message):
        print("work")
        self.kapcha_number = message.text

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Старт sMMO"),
                     KeyboardButton("Стоп sMMO"),
                     KeyboardButton("Стата"))

        self.reply_to(message, "Работаю...")
        self.send_message(message.chat.id, text="Повезло-повезло", reply_markup=keyboard)

if __name__ == "__main__":
    bot = Tg_Bot(token_tg_bot)

    bot.run_bot()