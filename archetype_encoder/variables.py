TOUR_NAME = "25_stockholm"
RK9_TOUR_ID = "SH01wBRUXITiDQIIRukL"
POKEDATA_TOUR_ID = "0000153"
LIMITLESS_TOUR_ID = "468"
DAY1_ROUNDS = 8


CATEGORY = 'masters'
FORMAT_EXP = "PRE"


LIMITLESS_BASE_ENDPOINT = "https://limitlesstcg.com"
LIMITLESS_TOUR_ENDPOINT  = f"{LIMITLESS_BASE_ENDPOINT}/tournaments/{LIMITLESS_TOUR_ID}"
LIMITLESS_DECKS_ENDPOINT = f"{LIMITLESS_BASE_ENDPOINT}/decks?variants=true&show=100&time=all&type=all&format=BRS-{FORMAT_EXP}&region=all&division=all"
RK9_BASE_ENDPOINT = "https://rk9.gg"
RK9_ROSTER = f"{RK9_BASE_ENDPOINT}/roster/{RK9_TOUR_ID}"
POKEDATA_CSV = f'https://pokedata.ovh/standings/{POKEDATA_TOUR_ID}/{CATEGORY}/data.csv?'