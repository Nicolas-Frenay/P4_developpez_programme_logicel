from tinydb import TinyDB


# from os import mkdir


class TournamentData:
    """
    Class that is used to store tournament and players data.
    """

    def __init__(self, name=None, resume=False, file=None):
        """
        constructor will setup a TinyDB object, and two tables to store players
        and tournament/rounds
        if parameter resume is Ture, it will creat empty attribute and called
        the resume_tournament method.
        """
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
        """
        method that load an existing file and its tables.
        """
        target_file = file + '.json'
        self.db = TinyDB(target_file, indent=4)
        self.players_table = self.db.table('Joueurs')
        self.tournaments_table = self.db.table('Tournois')

    def save_tournament(self, list):
        """
        methode that will store tournament in data base.
        """
        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(list)

    def save_players(self, players):
        """
        methode that store players in database.
        """
        self.players_table.truncate()
        self.players_table.insert_multiple(players)
