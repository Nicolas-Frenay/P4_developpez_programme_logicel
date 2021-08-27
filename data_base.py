from tinydb import TinyDB
from os import mkdir


class TournamentData:
    def __init__(self):
        self.db = TinyDB('Centre_échecs')
        self.players_table = self.db.table('Joueurs')
        self.tournaments_table = self.db.table('Tournois')

    def resume_tournament(self):
        return

    def save_tournament(self):
        return

    def end_tournament(self):
        return

    def save_players(self, tournois, player):
        return

    def serialize_player(self, player):
        serialize_p = {'family_name': player.family_name, 'name': player.name,
                       'dob': player.dob, 'sex': player.sex,
                       'rank': player.rank}
