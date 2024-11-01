
import asyncio

from pars_photo import Client

from skimage.metrics import structural_similarity as ssim
import cv2

import os, shutil

class Train(Client):

    def __init__(self):

        super().__init__()

        self.offset_id = None

        self.name_main_folder = "photo captch"
        self.contents = os.listdir(self.name_main_folder)

        self.list_value = {}


    async def learning(self):
        await self.session.start()

        try:
            list_mess = await self.session.get_messages(self.chat_id, limit=1)
            self.offset_id = list_mess[-1].id

        except:
            list_mess = await self.session.get_messages(self.chat_id, limit=2)
            self.offset_id = list_mess[-1].id

        for count in range(0, 10000, 500):
            self.messages = await self.session.get_messages(self.chat_id, limit=500, offset_id=self.offset_id)

            self.offset_id = self.messages[-1].id

            for mes in self.messages:

                #try:
                    if mes.photo:
                        path = f"{self.name_main_folder} test/карантин/{mes.id}.png"
                        await self.session.download_media(mes, file=path)

                        self.list_value = {}

                        for folder in self.contents:

                            path_folder = f"{self.name_main_folder}/{folder}"
                            images = os.listdir(path_folder)

                            summ = 0

                            for img in images:

                                summ += self.compare(f"{path_folder}/{img}", path)


                            self.list_value[folder] = summ / len(images)

                        print(self.list_value)

                        max_key = max(self.list_value, key=self.list_value.get)

                        destination_folder = f"{self.name_main_folder} test/{max_key}"
                        print(destination_folder)
                        os.makedirs(destination_folder, exist_ok=True)

                        destination = os.path.join(destination_folder, os.path.basename(path))
                        shutil.move(path, destination)

                #except Exception as exc:
                #    print(exc)


    def compare(self, path_img1, path_img2):

        print(f"{path_img1}  ||  {path_img2}")

        img1 = cv2.imread(path_img1)
        img2 = cv2.imread(path_img2)

        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_img2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

        similarity, _ = ssim(gray_img1, gray_img2, full=True)

        return similarity if similarity > 0 else 0


if __name__ == "__main__":

    train_ex = Train()

    asyncio.run(train_ex.learning())