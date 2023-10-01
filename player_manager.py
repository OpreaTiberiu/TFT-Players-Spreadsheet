from __future__ import annotations

from player import Player


class PlayerManager:
    def __init__(self, players_sheet: list[list[str]] | None = None):
        self.players = []
        self.headers = []

        if players_sheet is not None:
            self.create_from_sheet(players_sheet)

    def create_from_sheet(self, players_sheet: list[list[str]] | None):
        self.headers = [h.lower() for h in players_sheet[0]]
        for player_as_list in players_sheet[1:]:
            if len(player_as_list) == len(self.headers):
                player_as_dict = {
                    k.lower(): player_as_list[self.headers.index(k)]
                    for k in self.headers
                }
                self.players.append(Player(player_as_dict))

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_players_as_list(self) -> list[list[str]]:
        ret_val = [self.headers]
        for player in self.players:
            ret_val.append(player.get_formatted_dict(self.headers))
        return ret_val

    def __contains__(self, item: Player) -> bool:
        for player in self.players:
            if item.link == player.link:
                return True
        return False

    def set_headers(self) -> None:
        self.headers = list(self.players[0].__dict__.keys())

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
        player_manager.headers = (
            first_manager.headers if first_manager.headers else second_manager.headers
        )
        player_manager.players = first_manager.players.copy()
        for player in second_manager.players:
            if player not in player_manager:
                player_manager.add_player(player)

        return player_manager
