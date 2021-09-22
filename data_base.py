from tinydb import TinyDB
from os import mkdir


class TournamentData:
    """
    Class that is used to store tournament and players data.
    """

    def __init__(self, name=None, resume=False, file=None, finish=False):
        """
        constructor will setup a TinyDB object, and two tables to store players
        and tournament/rounds
        if parameter resume is True, it will creat empty attribute and called
        the resume_tournament method.
        Aims : creat a TinyDB object with two tables in it
        params :
        -name : str of the tournament name
        resume : boolean, if true, will resume a tournament
        -file : str of the file to load if resume is true.
        -finish : boolean to indicate if a tournament is finish, so it can be
        stored in the proper folder
        return : None
        """
        try:
            mkdir('Tournois/Terminés/')
        except FileExistsError:
            pass
        try:
            mkdir('Tournois/Interrompus/')
        except FileExistsError:
            pass
        if not resume:
            self.name = name.replace(' ', '_')
            if finish:
                self.db = TinyDB(
                    'Tournois/Terminés/' + self.name + '.json',
                    indent=4)
            else:
                self.db = TinyDB(
                    'Tournois/Interrompus/'
                    + self.name + '.json', indent=4)
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
        Aims : load an existing file and its tables.
        params :
        -file : str of the name of the file to load
        return : None
        """
        target_file = file + '.json'
        self.db = TinyDB(target_file, indent=4)
        self.players_table = self.db.table('Joueurs')
        self.tournaments_table = self.db.table('Tournois')

    def save_tournament(self, list):
        """
        Aims : store tournament in data base.
        params :
        -list : list of all data from the Tournois object
        return : None
        """
        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(list)

    def save_players(self, players):
        """
        Aims : store players in database.
        params :
        -players : list of serialized Joueurs instances.
        return : None
        """
        self.players_table.truncate()
        self.players_table.insert_multiple(players)
