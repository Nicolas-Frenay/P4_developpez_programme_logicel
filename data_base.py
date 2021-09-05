from tinydb import TinyDB
from os import mkdir


class TournamentData:
    def __init__(self, name):
        self.name = name.replace(' ', '_')
        self.db = TinyDB('Centre_échecs - ' + name + '.json', indent=4)
        self.players_table = self.db.table('Joueurs')
        self.tournaments_table = self.db.table('Tournois')

    def resume_tournament(self):
        return

    def save_tournament(self, list):
        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(list)

    def save_players(self, players):
        players_list = []

        for i in players:
            players_list.append(self.serialize_player(i))

        self.players_table.truncate()
        self.players_table.insert_multiple(players_list)


    def serialize_player(self, player):
        serialize_p = {'family_name': player.family_name, 'name': player.name,
                       'dob': player.dob, 'sex': player.sex,
                       'rank': player.rank, 'points': player.points}
        return serialize_p

    def serialize_tournament(self, list):
        return
