import os
import sys

from urllib.parse import urlparse

import click

from get_website_data import *
from sheets import Sheets

SET = "set10"
URL = "https://lolchess.gg/favorites?id=9ad17d45df624e2ab150d632671d644a#"


@click.command()
@click.option(
    "--check_website",
    is_flag=True,
    help="Try to grab data from lolchess and merge the 2 sources of data",
)
def update_players(check_website):
    check_website = True
    # get players from sheet
    sheets_obj = Sheets()
    sheets_obj.get_sheet_from_drive()
    sheet_data = sheets_obj.get_values()
    sheets_player_manager = PlayerManager(sheet_data["values"])

    # check and update any new links added
    for player in sheet_data["values"]:
        player_data_list = [data for data in player if bool(str(data).strip())]
        if len(player_data_list) == 1:
            url = player_data_list[0]
            if SET in url:
                url = url.replace(SET, "")
            complete_player_data = get_player_data(url, SET)
            if complete_player_data:
                sheets_player_manager.add_player(complete_player_data)

    if check_website:
        # get players from website
        # website_player_manager = get_players(URL)
        # merge the website and sheet players

        ##############################################################
        # FORCE RELOAD ALL PLAYERS
        # new_sheets_player_manager = PlayerManager()
        # for player in sheets_player_manager.players:
        #     renamed_player = get_player_site_data(player.link, SET)
        #     if renamed_player:
        #         new_sheets_player_manager.add_player(renamed_player)
        # complete_player_manager = PlayerManager.merge(
        #     website_player_manager, new_sheets_player_manager
        # )
        ##############################################################

        # complete_player_manager = PlayerManager.merge(
        #     website_player_manager, sheets_player_manager
        # )

        updated_complete_manager = PlayerManager()
        for player in sheets_player_manager.players:
            if type(player.link) is str and "http" in player.link:
                info_as_url = urlparse(player.link)
                if (
                    info_as_url.netloc == "lolchess.gg"
                    and "profile" in info_as_url.path
                ):
                    updated_player = get_player_data(url=player.link, set=SET)
                    if updated_player:
                        updated_complete_manager.add_player(updated_player)
        updated_complete_manager.sort()
        sheets_obj.clear()
        sheets_obj.update(updated_complete_manager.get_players_as_list())
    else:
        sheets_player_manager.sort()
        sheets_obj.clear()
        sheets_obj.update(sheets_player_manager.get_players_as_list())


if __name__ == "__main__":
    update_players()
