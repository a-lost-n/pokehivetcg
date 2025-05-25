import requests
import json
from bs4 import BeautifulSoup
from variables import LIMITLESS_BASE_ENDPOINT, LIMITLESS_DECKS_ENDPOINT

card_dict = {}
arch_dict = {}

def pull_decks(endpoint):
    global card_dict, arch_dict
    with requests.get(endpoint) as deck_table_page:
        soup = BeautifulSoup(deck_table_page.text, 'html.parser')
        table = soup.find('table', {'class': 'data-table striped'})
        for tr in table.find_all("tr"):
            a_tag = tr.find("a")
            if not a_tag: continue
            deck_name = a_tag.contents[0].strip()
            if deck_name in arch_dict: continue
            ref = a_tag['href'] 
            if 'variant=' not in ref: ref += '?variant=0'
            with requests.get(LIMITLESS_BASE_ENDPOINT + ref) as deck_page:
                deck_soup = BeautifulSoup(deck_page.text, 'html.parser')
                core_cards = deck_soup.find_all('div', {'class': 'core-card'})
                if not core_cards:
                    print(deck_name)
                    continue
                arch_dict[deck_name] = {"ref": ref, 'key_cards': {}}
                for core_card in core_cards:
                    img_tag = core_card.find("img")
                    data_set = img_tag['data-set']
                    data_number = img_tag['data-number']
                    set_number = "{}-{}".format(data_set, data_number)
                    if set_number not in card_dict:
                        with requests.get(LIMITLESS_BASE_ENDPOINT + core_card.find("a")['href']) as card_page:
                            card_soup = BeautifulSoup(card_page.text, 'html.parser')
                            card_name = card_soup.find('span', {'class': 'card-text-name'}).find("a").contents[0]
                            card_dict[set_number] = card_name
                    else:
                        card_name = card_dict[set_number]
                    card_name = card_name.replace('é', 'e')
                    arch_dict[deck_name]['key_cards'][card_name] = int(core_card.find('span').contents[0].strip()[0])


pull_decks(LIMITLESS_DECKS_ENDPOINT)

with open('archetypes.json', 'w') as file:
    json.dump(arch_dict, file, ensure_ascii=False)
