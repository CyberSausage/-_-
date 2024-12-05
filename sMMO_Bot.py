import os

from colorama import init, Fore, Back, Style

import requests as rq
import time
import threading

from bs4 import BeautifulSoup
import re
import random

from All_Token import token, api_token
from All_Headers import main_headers, photo_headers, base_headers, base_headers_material

from comparison_model import Similarity_Model

from googletrans import Translator

translator = Translator()

init(autoreset=True)

class Bot_sMMO_cl:

    def __init__(self, self_main_class):

        self.token = token
        self.api_token = api_token

        self.self_main_class = self_main_class

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

        self.sim_model = Similarity_Model()

        self.stop_event = threading.Event()

    def i_am_not_a_bot(self, answer):
        if (str(answer).find("/i-am-not-a-bot?new_page=true") != -1):
            answer = rq.get(self.url_i_am_not_a_bot, headers=self.headers)

            bs = BeautifulSoup(answer.text, 'lxml')
            title_question = bs.find(class_="text-2xl text-gray-800 font-semibold").get_text()

            try:
                result = translator.translate(title_question, src='en', dest='ru')

            except Exception as e:
                print("Ошибка при переводе:", e)

            mass_address_verification = bs.find_all(attrs={":class": "{'opacity-40':loading}"})

            for i in range(0, 4):

                response = rq.get(f"https://web.simple-mmo.com/i-am-not-a-bot/generate_image?uid={i}", headers=photo_headers)

                with open(f'generate_image_uid_{i}.png', 'wb') as file:
                    file.write(response.content)

            if self.count_attempt == 2:
                end_bot = self.people_choose(result, mass_address_verification)

            else:
                end_bot = self.model_choose(result, mass_address_verification)

            not_bot_responce = rq.post("https://web.simple-mmo.com/api/bot-verification", headers=self.headers, data={"data": end_bot, "valid": "false", "x": self.get_rand(400, 700), "y": self.get_rand(350, 410)})

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
        return end_bot


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
        answer = rq.post(self.url_steps, headers=base_headers, data={"_token": self.token, "api_token": self.api_token, "d_1": self.get_rand(446, 687), "d_2": self.get_rand(394, 423), "s": "false", "travel_id": 0})
        if answer.status_code == 200:
            try:
                answer = answer.json()
                if self.i_am_not_a_bot(answer['text']):
                    return None

                if (answer['heading'] == "Hold your horses!"):
                    return None


                if (answer['step_type'] == 'text'):
                    self.count_exp_amount += int(answer['exp_amount'])
                    self.count_gold_amount += int(answer['gold_amount'])
                    print(Fore.MAGENTA + f"Опыт: {self.count_exp_amount:<6}  |  Золото: {self.count_gold_amount:<6}  |  NPC: {self.count_kill_npc:<6}")


                elif (answer['step_type'] == 'npc'):
                    rq.get(self.url.replace("api/", "").replace("api", "web") + answer['text'].split("href='")[1].split("'")[0], headers=base_headers)
                    type_attack = self.attack_npc(answer['text'].split("href='")[1].split("?")[0].replace("/n", "n"))
                    self.count_kill_npc += 1
                    print(Fore.RED + f"{type_attack}:  {answer['text'].split('>')[3].split('<')[0]}  |  {answer['heading']}")

                elif (answer['step_type'] == 'item'):
                    print(Fore.YELLOW + "You have found the item")

                elif (answer['step_type'] == 'material'):
                    if answer['text'].find("Your skill level isn't high enough") != -1:
                        print(Fore.BLUE + "Your skill level isn't high enough")


                    else:
                        url_material_gather = rq.get(self.url.replace("api/", "").replace("api", "web") + answer['text'].split("location='")[1].split("'")[0], headers=base_headers).text
                        url_material_gather = url_material_gather.split('game_data.push')[1].split('"')[3]

                        id_room = answer['text'].split("location='")[1].split("/")[4].split("?")[0]

                        type_work = self.materials(self.normalize_url(url_material_gather), id_room, answer["text"].split(">")[3].split("<")[0])
                        print(Fore.CYAN + f"{type_work}:  {answer['heading']}   material  х{self.count_materials}   {answer['text'].split('>')[3].split('<')[0]}")
                        self.count_materials = 0

                elif (answer['step_type'] == 'player'):
                    print(f"Опыт: {self.count_exp_amount:<6}  |  Золото: {self.count_gold_amount:<6}  |  NPC: {self.count_kill_npc:<6}")

                time.sleep(self.get_rand(6.00001, 8))

            except Exception as e:
                print(e, "req_step")
                return None

    def attack_npc(self, number_npc):
        try:
            attack_npc = rq.post(self.url + number_npc + self.url_attack_npc, headers=base_headers, data={"_token": self.token, "api_token": self.api_token, "special_attack": "false"}).json()
            if (attack_npc['type'] == "error"):
                self.i_am_not_a_bot(attack_npc['result'])
                attack_npc = rq.post(self.url + number_npc + self.url_attack_npc, headers=self.headers,
                                     data={"_token": self.token, "api_token": self.api_token,
                                           "special_attack": "false"}).json()

            if (attack_npc['opponent_hp'] == 0):
                rq.get("https://web.simple-mmo.com/travel", headers=base_headers)
                return attack_npc['type']

            else:
                return self.attack_npc(number_npc=number_npc)

        except:
            return self.attack_npc(number_npc)

    def materials(self, url_gather, id_room, rare):
        request = ""
        request = rq.post(url_gather, headers=base_headers_material, data={"id": int(id_room), "quantity": 1})
        time.sleep(0.9)

        try:
            self.count_materials += 1
            self.count_materials_output[rare] += 1
            if not request.json()['is_end']:
                return self.materials(url_gather, id_room, rare)

            else:
                rq.get("https://web.simple-mmo.com/travel", headers=base_headers)
                return request.json()['type']

        except Exception as e:
            print(e, "materials")
            return "Error"

    def quests(self):
        answer = rq.get(self.url_quest, headers=self.headers)

        bs = BeautifulSoup(answer.text, 'lxml')
        link = bs.find_all(attrs={"onclick": re.compile(r"window\.location='/quests/view/")})

        number_quest = ""
        for li in link:
            span = li.find('span', class_=re.compile(r'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs'))
            if span:
                number_quest = li.get('onclick').split("='")[1].split("/")[3].split("?")[0]

        request = rq.post(f"{self.url}/quest/{number_quest}/gj83h", headers=self.headers, data={"api_token": self.api_token, "x": self.get_rand(432, 542), "y": self.get_rand(787, 817),"s": 0}).json()

        if (request['status'] == "error" and request["resultText"].find("Please verify that you are a human") != -1):
            self.i_am_not_a_bot(request['resultText'])

    def bank_dep(self, count):
        answer = rq.post(self.url_bank_dep, headers=self.headers, data={"_token": self.token, "GoldAmount": count}).json()

    def get_rand(self, min_value, max_value):
        if isinstance(min_value, float) or isinstance(max_value, float):
            return random.uniform(min_value, max_value)
        else:
            return random.randint(min_value, max_value)