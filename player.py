from __future__ import annotations

from rank_tiers import Rank
from headers import *

class Player:
    def __init__(self, player_dict: dict):
        self.server = player_dict[FIELDS_TO_HEADERS["server"]]
        self.name = player_dict[FIELDS_TO_HEADERS["name"]]
        self.rank = player_dict[FIELDS_TO_HEADERS["rank"]].upper()

        if any(str(number) in self.rank for number in [1, 2, 3, 4]):
            self.rank = self.rank.replace("1", "I")
            self.rank = self.rank.replace("2", "II")
            self.rank = self.rank.replace("3", "III")
            self.rank = self.rank.replace("4", "IV")

        self.lp = player_dict[FIELDS_TO_HEADERS["lp"]]
        self.link = player_dict[FIELDS_TO_HEADERS["link"]]
        self.winrate = player_dict[FIELDS_TO_HEADERS["winrate"]]
        self.toprate = player_dict[FIELDS_TO_HEADERS["toprate"]]
        self.played = player_dict[FIELDS_TO_HEADERS["played"]]
        self.wins = player_dict[FIELDS_TO_HEADERS["wins"]]
        self.tops = player_dict[FIELDS_TO_HEADERS["tops"]]

    def get_formatted_dict(self) -> list:
        values = [self.__getattribute__(key) for key in FIELDS_TO_HEADERS]
        return values

    def __repr__(self):
        return f"{self.name} {self.rank} {self.lp}"

    @staticmethod
    def sort_key(player: Player) -> tuple:
        # Sort by Rank > Division > LP
        rank_spit = player.rank.split()
        rank = Rank[rank_spit[0].upper()].value
        sort_key_value = [rank]
        # Division does not exist for Master+

        if len(rank_spit) > 1:
            division = rank_spit[1]
            if division == "I":
                division = 1
            if division == "II":
                division = 2
            if division == "III":
                division = 3
            if division == "IV":
                division = 4
            sort_key_value.append(division * -1)

        sort_key_value.append(int(player.lp.lower().replace("lp", "")))
        return tuple(sort_key_value)
