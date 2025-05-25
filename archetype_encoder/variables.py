TOUR_NAME = "25_santiago"
RK9_TOUR_ID = "ST01mJpZ3qImEgxMPdhAa"
POKEDATA_TOUR_ID = "0000161"
LIMITLESS_TOUR_ID = "475"
LIMITLESS_LABS_TOUR_ID = "0031"
DAY1_ROUNDS = 8


CATEGORY = 'masters'
FORMAT_EXP = "jtg"


LIMITLESS_BASE_ENDPOINT = "https://limitlesstcg.com"
LIMITLESS_TOUR_ENDPOINT  = f"{LIMITLESS_BASE_ENDPOINT}/tournaments/{LIMITLESS_TOUR_ID}"
LIMITLESS_DECKS_ENDPOINT = f"{LIMITLESS_BASE_ENDPOINT}/decks?variants=true&show=100&time=all&type=all&format=svi-{FORMAT_EXP}&region=all&division=all"
LIMILESS_LABS_BASE_ENDPOINT = "https://mew.limitlesstcg.com/labs/data/standings?tournamentId={}&division={}"
RK9_BASE_ENDPOINT = "https://rk9.gg"
RK9_ROSTER = f"{RK9_BASE_ENDPOINT}/roster/{RK9_TOUR_ID}"
POKEDATA_CSV = f'https://pokedata.ovh/standings/{POKEDATA_TOUR_ID}/{CATEGORY}/data.csv?'