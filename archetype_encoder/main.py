import pandas as pd
import re
import math
import requests
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from archetype_encoder.endpoints import LIMITLESS_LABS_MAIN_PAGE, LIMITLESS_LABS_STANDINGS_ENDPOINT, LIMITLESS_LABS_PAIRINGS_ENDPOINT

CATEGORY = 'MA'

base_dir = os.path.dirname(os.path.abspath(__file__))

def clean_name(input_string):
    result = re.sub(r'\s*\[.*?\]\s*', '', input_string)
    result = re.sub(r'STATIC SEATING \(\d+\)\s*', '', result)
    result = re.sub(r'>.*?>', '', result)
    result = re.sub(r'>TABLE \d+ ', '', result)
    return result


def get_standings(id):
    response = requests.get(LIMITLESS_LABS_STANDINGS_ENDPOINT.format(id, CATEGORY))
    standings_df = pd.DataFrame(response.json()['message'])

    archetype_dict = json.load(open(os.path.join(base_dir, "archetype.json")))

    standings_df = pd.DataFrame({
        'Placement': standings_df['placement'],
        'Player': standings_df['name'],
        'Player ID': standings_df['tp_id'],
        'Country': standings_df['country'],
        'Day 2': standings_df['day2'],
        'Deck': standings_df['deck_name'],
        'Variant': 'Standard'  # Set a constant value
    })
    standings_df = standings_df.dropna(subset=['Placement'])
    standings_df['Placement'] = standings_df['Placement'].apply(lambda x: "Top {}".format(pow(2, math.ceil(math.log(x, 2)))))
    standings_df['Deck'] = standings_df['Deck'].map(archetype_dict).fillna(standings_df['Deck'])

    return standings_df


def get_pairings(id):
    player1_list = []
    player2_list = []
    player1_id_list = []
    player2_id_list = []
    table_list = []
    round_list = []
    result_list = []
    round_iterator = 1
    while True:
        response = requests.get(LIMITLESS_LABS_PAIRINGS_ENDPOINT.format(id, CATEGORY, round_iterator))
        for pairing in response.json()['message']:
            if pairing['table'] and pairing['winner'] != -1:
                player1_list.append(clean_name(pairing['p1_name']))
                player1_list.append(clean_name(pairing['p2_name']))
                player2_list.append(clean_name(pairing['p2_name']))
                player2_list.append(clean_name(pairing['p1_name']))
                player1_id_list.append(pairing['player1'])
                player1_id_list.append(pairing['player2'])
                player2_id_list.append(pairing['player2'])
                player2_id_list.append(pairing['player1'])
                table_list.append(pairing['table'])
                table_list.append(pairing['table'])
                round_list.append(round_iterator)
                round_list.append(round_iterator)
                if pairing['winner'] == pairing['player1']:
                    result_list.append('W')
                    result_list.append('L')
                elif pairing['winner'] == pairing['player2']:
                    result_list.append('L')
                    result_list.append('W')
                elif pairing['winner'] == 0:
                    result_list.append('T')
                    result_list.append('T')
                else:
                    print(f"Unexpected winner value: {pairing['winner']} for round {round_iterator} at table {pairing['table']}.")

        round_iterator += 1

        if not response.json()['message']:
            break

    pairings_df = pd.DataFrame({
        'Player 1': player1_list,
        'Player 2': player2_list,
        'Player 1 ID': player1_id_list,
        'Player 2 ID': player2_id_list,
        'Table': table_list,
        'Round': round_list,
        'Result': result_list
    })

    return pairings_df

def save_to_excel(pairings_df, standings_df, name):
    with pd.ExcelWriter(f'{base_dir}/datasets/{name}.xlsx') as writer:
        pairings_df.to_excel(writer, sheet_name='pairings', index=False)
        standings_df.to_excel(writer, sheet_name='standings', index=False)


def get_tournaments():

    response = requests.get(LIMITLESS_LABS_MAIN_PAGE)

    if response.status_code != 200:
        print(f"Failed to fetch tournaments. Status code: {response.status_code}")
        return [], [], []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    tour_ids = []
    tour_names = []
    tour_dates = []

    for li in soup.find_all('ul', class_='grid')[0].find_all('li'):
        divs = li.find('a').find('div').find_all('div')

        # Get Date
        date_string = divs[1].contents[3]
        month = date_string.split()[0]
        day, year = re.search(r"–(\d+), (\d{4})", date_string).groups()
        date = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")

        if date < (datetime.now() - timedelta(days=14)):
            break

        # Get Tour ID
        tour_id = li.find('a').attrs['href'][1:5]

        # Get Tour Name
        tour_name = divs[0].contents[0].split()[2]

        # Append to lists
        tour_ids.append(tour_id)
        tour_names.append(tour_name)
        tour_dates.append(date)

    return tour_ids, tour_names, tour_dates


if __name__ == "__main__":

    standings = []
    pairings = []

    tour_ids, tour_names, tour_dates = get_tournaments()

    for tour_id in tour_ids:
        standings.append(get_standings(tour_id))
        pairings.append(get_pairings(tour_id))

    # For a single tournament
    if len(tour_ids) == 1:
        save_to_excel(pairings[0], standings[0], f"{tour_dates[0].strftime('%Y')}_{tour_names[0]}_{CATEGORY}")

    # For multiple tournaments
    elif len(tour_ids) > 1:

        merged_standings_df = pd.DataFrame()
        merged_pairings_df = pd.DataFrame()

        dataset_name = f"{tour_dates[0].strftime('%Y')}"

        for standings_df, pairings_df, tour_name in zip(standings, pairings, tour_names):
                standings_df['Tournament'] = tour_name
                standings_df['Player'] = standings_df['Player'] + f" - {tour_name}"
                merged_standings_df = pd.concat([merged_standings_df, standings_df])

                pairings_df['Player 1'] = pairings_df['Player 1'] + f" - {tour_name}"
                pairings_df['Player 2'] = pairings_df['Player 2'] + f" - {tour_name}"
                merged_pairings_df = pd.concat([merged_pairings_df, pairings_df])

                dataset_name += f"_{tour_name}"

        
        save_to_excel(merged_pairings_df, merged_standings_df, f"{dataset_name}_{CATEGORY}")
            
