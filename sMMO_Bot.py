import os

from colorama import init, Fore, Back, Style

import requests as rq
import time
import threading

from bs4 import BeautifulSoup
import re
import random

#from All_Token import token, api_token
from All_Headers import main_headers, photo_headers, base_headers, base_headers_material, base_headers_material_travel

from comparison_model import Similarity_Model

from googletrans import Translator

translator = Translator()

init(autoreset=True)


class Bot_sMMO_cl:


    def __init__(self, self_main_class, token, api_token):

        self.token = token
        self.api_token = api_token

        self.session = rq.Session()

        self.session.cookies.update({"cookie": self_main_class.connDB.select(nameTable='Cookie')[0][0]})

        self.self_main_class = self_main_class
        self.index_log_message = 0

        self.headers = main_headers

        self.url = "https://api.simple-mmo.com/api/"

        self.url_i_am_not_a_bot = f"https://web.simple-mmo.com/i-am-not-a-bot?new_page=true"

        self.url_steps = "https://api.simple-mmo.com/api/action/travel/4"
        self.url_attack_npc = "/434g3s"
        self.url_materials = "https://web.simple-mmo.com/api"
        self.url_quest = "https://web.simple-mmo.com/quests/viewall"
        self.url_bank_dep = "https://web.simple-mmo.com/bank/deposit/submit"

        self.count_exp_amount = 0
        self.count_gold_amount = 0
        self.count_kill_npc = 0
        self.count_materials = 0
        self.count_materials_output = {"Common": 0, "Uncommon": 0, "Rare": 0, "Elite": 0, "Epic": 0, "Legendary": 0, "Celestial": 0}

        self.count_attempt = 0

        self.path_image = ["generate_image_uid_0.png", "generate_image_uid_1.png", "generate_image_uid_2.png", "generate_image_uid_3.png"]

        self.sim_model = Similarity_Model()

        self.stop_event = threading.Event()


    def i_am_not_a_bot(self, answer):
        if (str(answer).find("/i-am-not-a-bot?new_page=true") != -1):
            answer = self.session.get(self.url_i_am_not_a_bot, headers=self.headers)

            bs = BeautifulSoup(answer.text, 'lxml')
            title_question = bs.find(class_="text-2xl text-gray-800 font-semibold").get_text()

            try:
                result = translator.translate(title_question, src='en', dest='ru')

            except Exception as e:
                print("Ошибка при переводе:", e)

            mass_address_verification = bs.find_all(attrs={":class": "{'opacity-40':loading}"})

            for i in range(0, 4):

                response = self.session.get(f"https://web.simple-mmo.com/i-am-not-a-bot/generate_image?uid={i}", headers=photo_headers)

                with open(f'generate_image_uid_{i}.png', 'wb') as file:
                    file.write(response.content)
            answer_for_log = 0
            if self.count_attempt == 2:
                end_bot = self.people_choose(result, mass_address_verification)

            else:
                end_bot, answer_for_log = self.model_choose(result, mass_address_verification)

            not_bot_responce = self.session.post("https://web.simple-mmo.com/api/bot-verification", headers=self.headers, data={"data": end_bot, "valid": "false", "x": self.get_rand(400, 700), "y": self.get_rand(350, 410)})

            self.self_main_class.log_menu.add_right_part_log_kaptcha(self.index_log_message, self.path_image[0], self.path_image[1], self.path_image[2], self.path_image[3], f"{result.text}: {answer_for_log + 1}", "#FF00FF")

            print(Fore.GREEN + not_bot_responce.json()['title'])

            if not_bot_responce.json()['title'].find("woops") == -1:
                self.count_attempt = 0
            else:
                self.count_attempt += 1

            return True

        return False


    def model_choose(self, result, mass_addr_ver):
        name_dir = f"photo captch test2/{result.text}"
        list_photo = os.listdir(name_dir)
        list_similarity = {0: [], 1: [], 2: [], 3: []}

        for i in range(0, 4):

            for img in list_photo:
                print(img)
                list_similarity[i].append(self.sim_model.compare(f"{name_dir}/{img}", f"generate_image_uid_{i}.png"))

            medium_sim = sum(sorted(list_similarity[i], reverse=True)[:10]) / 10
            list_similarity[i].clear()
            list_similarity[i] = medium_sim

        end_bot = mass_addr_ver[int(max(list_similarity, key=list_similarity.get))].get('x-on:click').split("'")[1]
        print(result.text, max(list_similarity, key=list_similarity.get))
        return end_bot, max(list_similarity, key=list_similarity.get)


    def people_choose(self, result, mass_addr_ver):
        self.self_main_class.send_photos(result.text)

        for i in list(self.count_materials_output.keys()):
            self.count_materials_output[i] = 0

        while self.self_main_class.kapcha_number is None:
            time.sleep(5)

        end_bot = mass_addr_ver[int(self.self_main_class.kapcha_number) - 1].get('x-on:click').split("'")[1]

        self.self_main_class.kapcha_number = None

        return end_bot


    def main_run(self):
        while not self.stop_event.is_set():
            self.req_step()


    def stop(self):
        self.stop_event.set()


    def normalize_url(self, raw_url):
        cleaned_url = raw_url.replace("\\", "").replace("u0026", "&")

        return cleaned_url


    def req_step(self):
        answer = self.session.post(self.url_steps, headers=base_headers, data={"_token": self.token, "api_token": self.api_token, "d_1": self.get_rand(446, 687), "d_2": self.get_rand(394, 423), "s": "false", "travel_id": 0})
        if answer.status_code == 200:
            #try:
                answer = answer.json()
                if self.i_am_not_a_bot(answer['text']):
                    return None

                if (answer['heading'] == "Hold your horses!"):
                    return None

                if (answer['step_type'] == 'text'):
                    self.count_exp_amount += int(answer['exp_amount'])
                    self.count_gold_amount += int(answer['gold_amount'])
                    text = f"Опыт: {self.count_exp_amount:<6}  |  Золото: {self.count_gold_amount:<6}  |  NPC: {self.count_kill_npc:<6}"

                    print(Fore.MAGENTA + text)
                    self.self_main_class.log_menu.add_right_part_log(self.index_log_message, text, "#7f03fc")


                elif (answer['step_type'] == 'npc'):
                    self.session.get(self.url.replace("api/", "").replace("api", "web") + answer['text'].split("href='")[1].split("'")[0], headers=base_headers)
                    type_attack = self.attack_npc(answer['text'].split("href='")[1].split("?")[0].replace("/n", "n"))
                    self.count_kill_npc += 1
                    text = f"{type_attack}:  {answer['text'].split('>')[3].split('<')[0]}  |  {answer['heading']}"

                    print(Fore.RED + text)
                    self.self_main_class.log_menu.add_right_part_log(self.index_log_message, text, "#FF0000")

                elif (answer['step_type'] == 'item'):
                    text = "You have found the item"
                    print(Fore.YELLOW + text)
                    self.self_main_class.log_menu.add_right_part_log(self.index_log_message, text, "#FFD700")

                elif (answer['step_type'] == 'material'):
                    if answer['text'].find("Your skill level isn't high enough") != -1:
                        print(Fore.BLUE + "Your skill level isn't high enough")


                    else:
                        url_material_gather = self.session.get(self.url.replace("api/", "").replace("api", "web") + answer['text'].split("location='")[1].split("'")[0].replace("/crafting", "crafting"), headers=base_headers_material_travel)

                        url_material_gather = url_material_gather.text.split('game_data.push')[1].split('"')[3]

                        id_room = answer['text'].split("location='")[1].split("/")[4].split("?")[0]

                        type_work = self.materials(self.normalize_url(url_material_gather), id_room, answer["text"].split(">")[3].split("<")[0])

                        text = f"{type_work}:  {answer['heading']}   material  х{self.count_materials}   {answer['text'].split('>')[3].split('<')[0]}"
                        print(Fore.CYAN + text)
                        self.self_main_class.log_menu.add_right_part_log(self.index_log_message, text, "#00FFFF")

                        self.count_materials = 0

                elif (answer['step_type'] == 'player'):
                    text = f"Опыт: {self.count_exp_amount:<6}  |  Золото: {self.count_gold_amount:<6}  |  NPC: {self.count_kill_npc:<6}"
                    print(text)
                    self.self_main_class.log_menu.add_right_part_log(self.index_log_message, text, "#E0FFFF")

                time.sleep(self.get_rand(6.00001, 8))

            #except Exception as e:
            #    print(e, "req_step")
            #    return None


    def attack_npc(self, number_npc):
        try:
            attack_npc = self.session.post(self.url + number_npc + self.url_attack_npc, headers=base_headers, data={"_token": self.token, "api_token": self.api_token, "special_attack": "false"}).json()
            if (attack_npc['type'] == "error"):
                self.i_am_not_a_bot(attack_npc['result'])
                attack_npc = self.session.post(self.url + number_npc + self.url_attack_npc, headers=self.headers,
                                     data={"_token": self.token, "api_token": self.api_token,
                                           "special_attack": "false"}).json()

            if (attack_npc['opponent_hp'] == 0):
                self.session.get("https://web.simple-mmo.com/travel", headers=base_headers)
                return attack_npc['type']

            else:
                return self.attack_npc(number_npc=number_npc)

        except:
            return self.attack_npc(number_npc)


    def materials(self, url_gather, id_room, rare):
        request = ""
        request = self.session.post(url_gather, headers=base_headers_material, data={"id": int(id_room), "quantity": 1})
        time.sleep(0.9)

        try:
            self.count_materials += 1
            self.count_materials_output[rare] += 1
            if not request.json()['is_end']:
                return self.materials(url_gather, id_room, rare)

            else:
                self.session.get("https://web.simple-mmo.com/travel", headers=base_headers)
                return request.json()['type']

        except Exception as e:
            print(e, "materials")
            return "Error"


    def quests(self):
        answer = self.session.get(self.url_quest, headers=self.headers)

        bs = BeautifulSoup(answer.text, 'lxml')
        link = bs.find_all(attrs={"onclick": re.compile(r"window\.location='/quests/view/")})

        number_quest = ""
        for li in link:
            span = li.find('span', class_=re.compile(r'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs'))
            if span:
                number_quest = li.get('onclick').split("='")[1].split("/")[3].split("?")[0]

        request = self.session.post(f"{self.url}/quest/{number_quest}/gj83h", headers=self.headers, data={"api_token": self.api_token, "x": self.get_rand(432, 542), "y": self.get_rand(787, 817),"s": 0}).json()

        if (request['status'] == "error" and request["resultText"].find("Please verify that you are a human") != -1):
            self.i_am_not_a_bot(request['resultText'])


    def bank_dep(self, count):
        answer = self.session.post(self.url_bank_dep, headers=self.headers, data={"_token": self.token, "GoldAmount": count}).json()


    def get_rand(self, min_value, max_value):
        if isinstance(min_value, float) or isinstance(max_value, float):
            return random.uniform(min_value, max_value)
        else:
            return random.randint(min_value, max_value)