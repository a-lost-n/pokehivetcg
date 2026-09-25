TOUR_NAME = "27_baltimore"
POKEDATA_TOUR_ID = "0000213"
LIMITLESS_LABS_TOUR_ID = "0072"


CATEGORY = 'masters'
FORMAT_EXP = "pbl"


LIMITLESS_BASE_ENDPOINT = "https://limitlesstcg.com"
LIMITLESS_DECKS_ENDPOINT = f"{LIMITLESS_BASE_ENDPOINT}/decks?variants=true&show=100&time=all&type=all&format=svi-{FORMAT_EXP}&region=all&division=all"
LIMITLESS_LABS_BASE_ENDPOINT = "https://mew.limitlesstcg.com/labs/data/tcg/standings?tournamentId={}&division={}"
# RK9_BASE_ENDPOINT = "https://rk9.gg"
# RK9_ROSTER = f"{RK9_BASE_ENDPOINT}/roster/{RK9_TOUR_ID}"
POKEDATA_CSV = f'https://pokedata.ovh/standings/{POKEDATA_TOUR_ID}/{CATEGORY}/data.csv?'