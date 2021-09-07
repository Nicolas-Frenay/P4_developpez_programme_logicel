from tinydb import TinyDB


# from os import mkdir


class TournamentData:
    def __init__(self, name=None, resume=False, file=None):
        if not resume:
            self.name = name.replace(' ', '_')
            self.db = TinyDB('Tournois/Centre_échecs - ' + self.name + '.json',
                             indent=4)
            self.players_table = self.db.table('Joueurs')
            self.tournaments_table = self.db.table('Tournois')
        else:
            self.name = None
            self.db = None
            self.players_table = None
            self.tournaments_table = None
            self.resume_tournament(file)

    def resume_tournament(self, file):
        target_file = file + '.json'
        self.db = TinyDB(target_file, indent=4)
        self.players_table = self.db.table('Joueurs')
        self.tournaments_table = self.db.table('Tournois')

    def save_tournament(self, list):
        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(list)
