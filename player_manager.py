from __future__ import annotations

from player import Player
from headers import *

HEADERS = [
    "Server",
    "Nume",
    "Rank",
    "LP",
    "Link",
    "Winrate",
    "Top4",
    "Nr. meciuri",
    "Wins",
    "Nr.Top4",
]


class PlayerManager:
    def __init__(self, players_sheet: list[list[str]] | None = None):
        self.players = []

        if players_sheet is not None:
            self.create_from_sheet(players_sheet)

    def create_from_sheet(self, players_sheet: list[list[str]] | None):
        for player_as_list in players_sheet[1:]:
            if len(player_as_list) == len(FIELDS_TO_HEADERS.keys()):
                player_as_dict = {
                    k: player_as_list[list(FIELDS_TO_HEADERS.values()).index(k)]
                    for k in FIELDS_TO_HEADERS.values()
                }
                self.players.append(Player(player_as_dict))

    def add_player(self, player: Player) -> None:
        if player not in self:
            self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_players_as_list(self) -> list[list[str]]:
        ret_val = [list(DISPLAYED_HEADERS.values())]
        for player in self.players:
            ret_val.append(player.get_formatted_dict())
        return ret_val

    def __contains__(self, item: Player) -> bool:
        for player in self.players:
            if item.link == player.link or player.name == item.name:
                return True
        return False

    def sort(self):
        self.players.sort(key=Player.sort_key, reverse=True)

    @staticmethod
    def merge_and_sort(
        first_manager: PlayerManager, second_manager: PlayerManager
    ) -> PlayerManager:
        player_manager = PlayerManager.merge(first_manager, second_manager)
        player_manager.sort()
        return player_manager

    @staticmethod
    def merge(
        first_manager: PlayerManager, second_manager: PlayerManager
    ) -> PlayerManager:
        player_manager = PlayerManager()
        player_manager.players = first_manager.players.copy()
        for player in second_manager.players:
            if player not in player_manager:
                player_manager.add_player(player)

        return player_manager
