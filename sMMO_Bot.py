from colorama import init, Fore, Back, Style

import requests as rq
import time
import threading

from bs4 import BeautifulSoup
import re
import random

from All_Token import token, api_token
from All_Headers import main_headers, photo_headers, base_headers

from googletrans import Translator

translator = Translator()

init(autoreset=True)

class Bot_sMMO_cl:

    def __init__(self, self_main_class):

        self.token = token
        self.api_token = api_token

        self.self_main_class = self_main_class

        self.headers = main_headers

        self.url = "https://api.simple-mmo.com/api"

        self.url_i_am_not_a_bot = f"https://web.simple-mmo.com/i-am-not-a-bot?new_page=true"

        self.url_steps = "https://api.simple-mmo.com/api/action/travel/4"
        self.url_attack_npc = "/434g3s"
        self.url_materials = "https://web.simple-mmo.com/api" # /crafting/material/gather/151468913?new_page=true
        self.url_quest = "https://web.simple-mmo.com/quests/viewall"
        self.url_bank_dep = "https://web.simple-mmo.com/bank/deposit/submit"

        self.count_exp_amount = 0
        self.count_gold_amount = 0
        self.count_kill_npc = 0
        self.count_materials = 0
        self.count_materials_output = {"Common": 0, "Uncommon": 0, "Rare": 0, "Elite": 0, "Epic": 0, "Legendary": 0, "Celestial": 0}

        self.stop_event = threading.Event()

    def i_am_not_a_bot(self, answer):
        if (str(answer).find("/i-am-not-a-bot?new_page=true") != -1):
            answer = rq.get(self.url_i_am_not_a_bot, headers=self.headers)

            bs = BeautifulSoup(answer.text, 'lxml')
            title_question = bs.find(class_="text-2xl text-gray-800 font-semibold").get_text()

            result = translator.translate(title_question, src='en', dest='ru')

            mass_address_verification = bs.find_all(attrs={":class": "{'opacity-40':loading}"})

            for i in range(0, 4):

                response = rq.get(f"https://web.simple-mmo.com/i-am-not-a-bot/generate_image?uid={i}", headers=photo_headers)

                with open(f'generate_image_uid_{i}.png', 'wb') as file:
                    file.write(response.content)



            self.self_main_class.send_photos(result.text)

            for i in list(self.count_materials_output.keys()):
                self.count_materials_output[i] = 0

            while self.self_main_class.kapcha_number is None:
                time.sleep(5)

            end_bot = mass_address_verification[int(self.self_main_class.kapcha_number) - 1].get('x-on:click').split("'")[1]
            not_bot_responce = rq.post("https://web.simple-mmo.com/api/bot-verification", headers=self.headers, data={"data": end_bot, "valid": "false", "x": self.get_rand(400, 700), "y": self.get_rand(350, 410)})

            self.self_main_class.kapcha_number = None

            print(Fore.GREEN + not_bot_responce.json()['title'])

            return True

        return False

    def main_run(self):
        while not self.stop_event.is_set():
            self.req_step()

    def stop(self):
        self.stop_event.set()

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
                    type_attack = self.attack_npc(answer['text'].split("href='")[1].split("?")[0])
                    self.count_kill_npc += 1
                    print(Fore.RED + f"{type_attack}:  {answer['text'].split('>')[3].split('<')[0]}  |  {answer['heading']}")

                elif (answer['step_type'] == 'item'):
                    print(Fore.YELLOW + "You have found the item")

                elif (answer['step_type'] == 'material'):
                    if answer['text'].find("Your skill level isn't high enough") != -1:
                        print(Fore.BLUE + "Your skill level isn't high enough")


                    else:
                        rq.get(self.url.replace("api/", "").replace("api", "web") + answer['text'].split("location='")[1].split("'")[0], headers=base_headers)
                        type_work = self.materials(answer['text'].split("location='")[1].split("?")[0], answer["text"].split(">")[3].split("<")[0])
                        print(Fore.CYAN + f"{type_work}:  {answer['heading']}   material  х{self.count_materials}   {answer['text'].split('>')[3].split('<')[0]}")
                        self.count_materials = 0

                elif (answer['step_type'] == 'player'):
                    print(f"Опыт: {self.count_exp_amount:<6}  |  Золото: {self.count_gold_amount:<6}  |  NPC: {self.count_kill_npc:<6}")

                time.sleep(self.get_rand(5.00001, 5.25))

            except Exception as e:
                print(e)
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

    def materials(self, number_material, rare):
        requerst = ""
        requerst = rq.post(f"{self.url_materials}{number_material}", headers=base_headers, data={"_token": self.token})
        time.sleep(0.5)

        try:
            self.count_materials += 1
            self.count_materials_output[rare] += 1
            if not requerst.json()['gatherEnd']:
                return self.materials(number_material, rare)

            else:
                rq.get("https://web.simple-mmo.com/travel", headers=base_headers)
                return requerst.json()['type']

        except Exception as e:
            print(e)
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