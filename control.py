import json
from operator import attrgetter
from datetime import datetime
from data_base import TournamentData


class Tournois:
    """
    Class that handles all the Tournament related computations.
    """

    def __init__(self, file=None, resume=False):
        """
        constructor that will creat a list to store Joueurs instances, the
        current Round instance, the past Round instances, a round_list that
        store lists of pairs of players playing against each other each rounds,
        a round counter, and and tournament finish flag.

        if it's a new tournament, it will then ask the user for the tournament
        infos.

        If it's a resumed tournament, it will called the resume_tournament
        method that will get the infos from the database.
        """
        self.players = []
        self.current_round = None
        self.rounds = []
        self.round_number = 1
        self.tournament_finish = False

        if resume:
            self.name = None
            self.place = None
            self.date_start = None
            self.date_end = None
            self.time = None
            self.desc = None
            self.turns = None
            self.resume_tournament(file)
        else:
            # self.name = input('Nom du tournois ?')
            # self.place = input('Lieu du tournois ?')
            # self.date_start = input('Date de debut du tournois? (DD/MM/YYYY)')
            # self.date_end = input('Date de fin du tournois ? (DD/MM/YYYY)')
            # self.time = input(
            #     'Quelle est le format des match (bullet, blitz,coup rapide) ?')
            # self.desc = input('Description du tournois ?')
            # self.turns = input(
            #     'En combien de tours se déroule le tournois ?(défaut : 4)') or 4

            # bit of code for testing purposes, it loads tournament info from
            # json file.
            with open('tournois.json') as f:
                data = json.load(f)
            self.name = data['name']
            self.place = data['place']
            self.date_start = data['date_start']
            self.date_end = data['date_end']
            self.time = data['time']
            self.desc = data['desc']
            self.turns = data['turns']
            f.close()

    def get_round_matchs(self):
        match = []
        for i in self.rounds:
            match.append(i.round_matches)
        match.append(self.current_round.round_matches)
        return match

    def create_round(self, matches):

        """
        methode creating a new round instance, naming it via the round counter
        of the tournament class and passing matches.
        """
        self.current_round = Rounds(name='Round ' + str(self.round_number),
                                    matches=matches)

    def add_players(self, nombre_de_joueur=8):
        """
        method asking the user for each players infos.
        then it called the first_round method to creat the first matchs, then
         create a new round instance, and passes it the matchs list.
        """

        # for i in range(0, nombre_de_joueur):
        #     ident = i
        #     family_name = input('Nom de famille du joueur {} ?'.format(i))
        #     name = input('Prénom du joueur {} ?'.format(i))
        #     dob = input('Date de naissance du joueur {} (DD/MM/YYYY) ?'
        #                 .format(i))
        #     sex = input('Sex du joueur {} (H/F) ?'.format(i))
        #     rank = int(input('Classement du joueur {} ?'.format(i)))
        #
        #     self.players.append(Joueurs(ident, family_name, name, dob, sex, rank))

        # bit of code for testing purposes, it loads players info from json
        # file.
        with open('joueurs.json') as f:
            data = json.load(f)
            for i in data:
                self.players.append(
                    Joueurs(i['ident'], i['family_name'], i['name'], i['dob'],
                            i['sex'], i['rank'], i['points']))
        f.close()

        first_round = self.first_round()
        self.create_round(first_round)

    def save_tournament(self):
        """
        method to save the tournament as a json file using TinyDB.

        """
        # creating a tournamentData object
        tournament_save = TournamentData(self.name)

        players_list = []

        # serializing the players instances
        for i in self.players:
            players_list.append(i.serialize_player())

        # saving the serialized players' infos
        tournament_save.save_players(players_list)

        # saving tournament
        tournament_infos = []
        name = self.name
        place = self.place
        date_start = self.date_start
        date_end = self.date_end
        time = self.time
        desc = self.desc
        turns = self.turns
        tournament_infos.append(
            {'name': name, 'place': place, 'date_start': date_start,
             'date_end': date_end, 'time': time, 'description': desc,
             'turns': turns, 'round_number': self.round_number})
        if self.rounds:
            for i in self.rounds:
                tournament_infos.append(self.save_rounds(i))

        # saving current round
        tournament_infos.append(self.save_rounds(self.current_round))

        tournament_save.save_tournament(tournament_infos)

    @staticmethod
    def save_rounds(rounds):
        """
        static method that serialized Rounds instances
        """

        name = rounds.name
        results = rounds.results
        time_start = rounds.time_start
        time_end = rounds.time_end
        matchs = rounds.saved_matches
        round_to_save = {'name': name, 'results': results, 'matchs': matchs,
                         'time_start': time_start, 'time_end': time_end}
        return round_to_save

    def resume_tournament(self, file):
        """
        method to resume an un-finish tournament.
        it creat a tournament_data objet, then us it to load the tournaments
        and players infos.
        """

        resumed_tournament = TournamentData(resume=True, file=file)
        doc_in_table = 1

        # getting players serialized infos, then calling new Joueurs instances.
        for player in resumed_tournament.players_table:
            ident = player['ident']
            family_name = player['family_name']
            name = player['name']
            dob = player['dob']
            sex = player['sex']
            rank = player['rank']
            points = player['points']
            self.players.append(
                Joueurs(ident, family_name, name, dob, sex, rank, points))

        # getting tournament infos
        tournament_infos = resumed_tournament.tournaments_table.get(
            doc_id=doc_in_table)
        self.name = tournament_infos['name']
        self.place = tournament_infos['place']
        self.date_start = tournament_infos['date_start']
        self.date_end = tournament_infos['date_end']
        self.time = tournament_infos['time']
        self.desc = tournament_infos['description']
        self.turns = tournament_infos['turns']
        self.round_number = tournament_infos['round_number']
        doc_in_table += 1

        # getting round infos, then calling new rounds instances
        rounds_infos = resumed_tournament.tournaments_table.get(
            doc_id=doc_in_table)

        while rounds_infos:

            temp = Rounds(rounds_infos['name'], resume=True)
            temp.results = rounds_infos['results']
            temp.saved_matches = rounds_infos['matchs']
            temp.time_start = rounds_infos['time_start']
            temp.time_end = rounds_infos['time_end']

            # getting pairs of players, then storing them in tournament
            # instance, and the proper round instance.
            players_list = sorted(self.players, key=attrgetter('ident'))
            matchs_list = []

            for i in temp.saved_matches:
                p1 = players_list[i['id_player_1']]
                p2 = players_list[i['id_player_2']]
                matchs_list.append([p1, p2])

            temp.round_matches = matchs_list

            if not temp.time_end:
                self.current_round = temp
            else:
                self.rounds.append(temp)

            doc_in_table += 1
            rounds_infos = resumed_tournament.tournaments_table.get(
                doc_id=doc_in_table)

    def enter_results(self):
        """
        method to enter the results of a round.
        it first creat the new pairs of players for the next round via
        the next_round method, then adds it to the rounds list.
        it increment the round counter, and if the tournament isn't finish,
        call the time_stamp for the end of the round, put the finish round in
        the rounds variable, and creat a new round.
        """
        new_round = self.next_round()
        self.round_number += 1
        if self.round_number <= 4:
            self.current_round.time_stamp(end=True)
            self.rounds.append(self.current_round)
            self.create_round(new_round)
        else:
            self.tournament_finish = True

    def first_round(self):
        """
        Method that creat the first pairs of player, using the swiss sorting
        system.
        """
        start_round_list = []
        players_list = sorted(self.players, key=attrgetter('rank'),
                              reverse=True)
        for i in range(0, len(players_list) // 2):
            start_round_list.append(
                [players_list[i], players_list[i + len(players_list) // 2]])
        return start_round_list

    def next_round(self):
        """
        Method that creat the rounds after the first one, using the swiss
        system.
        """
        new_round = []
        i = 1
        tmp = sorted(self.players, key=attrgetter('points', 'rank'),
                     reverse=True)

        # if the two first players already met, it puts #1 with #3.
        past_rounds = self.get_round_matchs()
        while tmp:
            for tours in past_rounds:
                if [tmp[0], tmp[i]] in tours or [tmp[i], tmp[0]] in tours:
                    i = 2
                    break
                # this avoid index error. It can allows two players to meet
                # twice in a tournament, but it's the swiss system.
            if len(tmp) < 3:
                i = 1
            new_round.append([tmp[0], tmp[i]])
            tmp.pop(i)
            tmp.pop(0)
            i = 1

        return new_round


class Rounds:
    """
    class that creats rounds
    """

    def __init__(self, name, matches=None, resume=False):
        """
        constructor creat a list for store the results, a name attribute, a
        list of the patch of that round (pairs of players), a list of matches
        that will be saved and two variables to store timestaps of the star
         and end of the round. For the start one, it calls the time_stamp
         method.
        """
        self.results = []
        self.name = name
        self.round_matches = matches
        self.saved_matches = []
        self.time_start = None
        self.time_end = None
        if not resume:
            self.time_stamp()
            self.matches()

    def time_stamp(self, end=False):
        """
        method that creat time stamp, it uses the end booelan to store either
        the start or end time.
        """
        date = datetime.now()

        if not end:
            self.time_start = date.strftime("%d/%m/%Y %H:%M:%S")
        else:
            self.time_end = date.strftime("%d/%m/%Y %H:%M:%S")

    def matches(self):
        """
        Method that store the matchs as string with player's indent, to be
        store in the database.
        """
        for i in self.round_matches:
            self.saved_matches.append(
                {'id_player_1': i[0].ident, 'id_player_2': i[1].ident})

    def match_results(self, players, index):
        """
        method that store each match result as a tuple of lists :each list is
        the name and ident of the player, and results of the match.
        It also change the player's instance points.
        index and players are passed by the result_menu method of the Menus
        class.
        """
        if index == 0:
            players[index].new_points(1)
            p1 = [players[index].family_name + ', ' + players[
                index].name + ' (id:' + str(players[index].ident) + ')', 1]
            p2 = [players[1].family_name + ', ' + players[
                1].name + ' (id:' + str(players[1].ident) + ')', 0]
            self.results.append((p1, p2))
        elif index == 1:
            players[index].new_points(1)
            p1 = [players[index].family_name + ', ' + players[
                index].name + ' (id:' + str(players[index].ident) + ')', 1]
            p2 = [players[0].family_name + ', ' + players[
                0].name + ' (id:' + str(players[0].ident) + ')', 0]
            self.results.append((p1, p2))
        else:
            players[0].new_points(0.5)
            players[1].new_points(0.5)
            p1 = [players[0].family_name + ', ' + players[
                0].name + ' (id:' + str(players[0].ident) + ')', 0.5]
            p2 = [players[1].family_name + ', ' + players[
                1].name + ' (id:' + str(players[1].ident) + ')', 0.5]
            self.results.append((p1, p2))


class Joueurs:
    """
    Class creating players for the tournament.
    """

    def __init__(self, ident, family_name, name, dob, sex, rank, points=0):
        """
        constructor creats infos attributes
        """
        self.ident = ident
        self.family_name = family_name
        self.name = name
        self.dob = dob
        self.sex = sex
        self.rank = rank
        self.points = points

    def new_rank(self, new_rank):
        """
        method that change the rank of the player
        """
        self.rank = new_rank

    def new_points(self, new_points):
        """
        method that change the points of the player
        """
        self.points += new_points

    def mod_player(self):
        """
        Method that allow the user to change the player infos.
        """
        family_name = input('Nom de famille du joueur ?')
        name = input('Prénom du joueur ?')
        dob = input('Date de naissance du joueur (DD/MM/YYYY) ?')
        sex = input('Sex du joueur (H/F) ?')
        rank = int(input('Classement du joueur ?'))
        self.family_name = family_name
        self.name = name
        self.dob = dob
        self.sex = sex
        self.rank = rank

    def serialize_player(self):
        """
        method that serialized the player's instance so it can be stored.
        """
        serialize_p = {'ident': self.ident, 'family_name': self.family_name,
                       'name': self.name, 'dob': self.dob,
                       'sex': self.sex, 'rank': self.rank,
                       'points': self.points}
        return serialize_p
