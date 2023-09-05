from sheets import Sheets
from get_data import get_players_data

URl = 'https://lolchess.gg/favorites?id=9ad17d45df624e2ab150d632671d644a#'


data = get_players_data(URl)
sheets_obj = Sheets()
sheets_obj.add_data(data)
