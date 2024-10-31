from telethon import TelegramClient
import asyncio
import re

from All_Token import api_tg_id, api_tg_hash


class Client:

    def __init__(self):

        self.api_id = api_tg_id
        self.api_hash = api_tg_hash

        self.chat_id = '' # id чата или @ тег

        self.session = TelegramClient('my_session', self.api_id, self.api_hash)

        self.messages = []

        self.index_mes = 0
        self.index_photo = {}


    async def run(self):
        await self.session.start()

        last_mes_id = None

        for count in range(0, 10000, 500):

            if last_mes_id is not None:
                self.messages = await self.session.get_messages(self.chat_id, limit=500, offset_id=last_mes_id)
            else:
                self.messages = await self.session.get_messages(self.chat_id, limit=500)

            last_mes_id = self.messages[-1].id

            for mes in self.messages:
                if re.match(r'^[1-4]$', mes.message):
                    self.index_mes = self.messages.index(mes)

                    self.index_photo = {
                        "1": self.index_mes + 5, "2": self.index_mes + 4,
                        "3": self.index_mes + 3, "4": self.index_mes + 2,

                        "-1": mes.id - 5, "-2": mes.id - 4,
                        "-3": mes.id - 3, "-4": mes.id - 2,
                    }

                    try:
                        title = self.messages[self.index_mes + 1].message
                        mess_photo = self.messages[self.index_photo[mes.message]]

                    except:
                        title = self.session.get_messages(self.chat_id, limit=1, offset_id=mes.id - 1)
                        mess_photo = self.session.get_messages(self.chat_id, limit=1, offset_id=self.index_photo[f"-{mes.message}"])

                    if asyncio.iscoroutine(mess_photo):
                        print(mess_photo)

                    else:
                        if mess_photo.photo:
                            await self.session.download_media(mess_photo, file=f"{title}/{mess_photo.id}.png")


            await asyncio.sleep(3)


if __name__ == "__main__":

    cli = Client()
    asyncio.run(cli.run())