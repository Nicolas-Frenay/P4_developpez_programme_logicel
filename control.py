import json
from operator import attrgetter, itemgetter
from datetime import datetime
from data_base import TournamentData
from glob import glob


class Tournois:
    """
    Class that handles all the Tournament related computations.
    """

    def __init__(self, file=None, resume=False):
        """
        constructor that will creat a list to store Joueurs instances, an
        empty attribut to store the current Round instance, the past Round
        instances, a round_list that store finished rounds, a round counter,
        and and tournament finish flag.

        Aims : constructor will creat a list to store Joueurs instances, an
        empty attribut to store the current Round instance, a round_list that
        store finished rounds, a round counter, and and tournament finish flag.
        params :
        -file : str : filename used to load a un-finished tournament from data
        base
        -resume : boolean, if true : will set attributes to None before loading
        the resumed tournament.
        returns : None
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
            # self.date_start = input('Date de debut du tournois? '
            #                         '(DD/MM/YYYY)')
            # self.date_end = input('Date de fin du tournois ? (DD/MM/YYYY)')
            # self.time = input(
            #     'Quelle est le format des match (bullet, '
            #     'blitz,coup rapide) ?')
            # self.desc = input('Description du tournois ?')
            # self.turns = input(
            #     'En combien de tours se déroule le tournois ? '
            #     '(<Entrée> pour la valeur par defaut : 4)') or 4

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

    def add_players(self, nb_of_players=8):
        """
        Aims : ask the user for each players infos, called the first_round
        method to creat the first matchs, create a new round instance, and
        passes it the matchs list.
        params :
        -nb_of_players : int, default 8.
        return : None
        """

        # # bit of code for testing purposes, it loads players info from json
        # # file.
        with open('joueurs.json') as f:
            data = json.load(f)
            for i in data:
                self.players.append(
                    Joueurs(i['ident'], i['family_name'], i['name'], i['dob'],
                            i['sex'], i['rank'], i['points']))
        f.close()

        first_round = self.first_round()
        self.create_round(first_round)

    def get_round_matchs(self):
        """
        Aims :  get all round (finished and current) into a list
        params None
        return : List of all Round instances.
        """
        match = []
        for rounds in self.rounds:
            match.append(rounds.round_matches)
        match.append(self.current_round.round_matches)
        return match

    def create_round(self, matches):
        """
        Aims : creat a new round instance
        params :
        -Matches : List of matchs (pairs of players instances)
        return : None
        """
        self.current_round = Rounds(name='Round ' + str(self.round_number),
                                    matches=matches)

    def first_round(self):
        """
        Aims : creat the first pairs of player, using the swiss sorting
        system.
        params : None
        return : list of matchs (pairs of players instances)
        """
        start_round_list = []
        players_list = sorted(self.players, key=attrgetter('rank'),
                              reverse=True)
        for i in range(0, len(players_list) // 2):
            start_round_list.append(
                [players_list[i],
                 players_list[i + len(players_list) // 2]])
        return start_round_list

    def next_round(self):
        """
        Aims : creat the rounds after the first one, using the swiss system.
        params : None
        return : list of matchs (pairs of players instances)
        """
        new_round = []
        i = 1
        tmp = sorted(self.players, key=attrgetter('points', 'rank'),
                     reverse=True)

        # if the two first players already met, put #1 with #3.
        past_rounds = self.get_round_matchs()
        while tmp:
            for tours in past_rounds:
                if [tmp[0], tmp[i]] in tours or [tmp[i], tmp[0]] in tours:
                    i = 2
                    break

                # this avoid index error. During testing, it appears that with
                # that algorithm, it start to make player met again after 4
                # rounds. I suppose it's a math problem, and that with N
                # players, it works only with N/2 -1 round...
                # Since during chess tournament, it should be use only 3 times,
                # it will work properly, but i let it just in case.
            if len(tmp) < 3:
                i = 1

            new_round.append([tmp[0], tmp[i]])
            tmp.pop(i)
            tmp.pop(0)
            i = 1

        return new_round

    def end_round(self):
        """
        Aims :End a round. call next_round method to get the next match,
        increase round counter, if it's not the last round, called time_stamp
        method from current round, put it in past round list, and creat a new
        round.
        params : None
        return : None
        """
        new_round = self.next_round()
        self.round_number += 1
        if self.round_number <= 4:
            self.current_round.time_stamp(end=True)
            self.rounds.append(self.current_round)
            self.create_round(new_round)
        else:
            self.tournament_finish = True

    def save_tournament(self):
        """
        Aims : save the tournament as a json file using TinyDB.
        params : None
        return : None
        """

        # creating a tournamentData object
        tournament_save = TournamentData(self.name,
                                         finish=self.tournament_finish)

        # if tournament is finish, put the end time stamp on current round.
        if self.tournament_finish:
            self.current_round.time_stamp(end=True)

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

        # If there is finished round in self.rounds, it saves it.
        if self.rounds:
            for rounds in self.rounds:
                round_saved = self.save_rounds(rounds)
                tournament_infos.append(round_saved)

        # saving current round
        current_round_saved = self.save_rounds(self.current_round)
        tournament_infos.append(current_round_saved)

        tournament_save.save_tournament(tournament_infos)

        del tournament_save

    @staticmethod
    def save_rounds(rounds):
        """
        Aims : serialized Rounds instances
        params :
        -rounds : Round instance
        return : dictionary of the serialized round
        """

        name = rounds.name
        results = rounds.results
        time_start = rounds.time_start
        time_end = rounds.time_end
        matchs = rounds.saved_matches
        round_to_save = {'name': name, 'results': results,
                         'matchs': matchs,
                         'time_start': time_start, 'time_end': time_end}

        return round_to_save

    def resume_tournament(self, file):
        """
        Aims : resume an un-finished tournament
        params :
        -file : str of the file to resume the tournament from
        return : None
        """

        resumed_tournament = TournamentData(resume=True, file=file)
        # doc_in_table is use to select the proper set of data in the save
        # file.
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

        # scrapping next document in table
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

            # getting pairs of players, then setting them in Round instance
            players_list = sorted(self.players, key=attrgetter('ident'))
            matchs_list = []

            for match in temp.saved_matches:
                p1 = players_list[match['id_player_1']]
                p2 = players_list[match['id_player_2']]
                matchs_list.append([p1, p2])

            temp.round_matches = matchs_list

            # if Round has no time_end attribute, set it as the current round
            if not temp.time_end:
                self.current_round = temp
            else:
                self.rounds.append(temp)

            doc_in_table += 1
            rounds_infos = resumed_tournament.tournaments_table.get(
                doc_id=doc_in_table)

        del resumed_tournament


class Rounds:
    """
    class that creats rounds objects
    """

    def __init__(self, name, matches=None, resume=False):
        """
        Aims : constructor creat a list for store the results, a name
        attribute, a list of the matches of that round, a list of matches for
        saving, and two variables to store timestamps of the start and end of
        the round.
        params :
        -name : str to name the Round
        -matches : list of matches of the round (pairs of players)
        resume : Boolean : if True, constructor will not put start time stamp,
        and won't store matches as dictionaries.
        return : None
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
        Aims : creat time stamps
        params :
        -end : Boolean, if True, will store the time stamp in time_end
        atribute, otherwise, it stores it in time_start.
        :return : None
        """
        date = datetime.now()

        if not end:
            self.time_start = date.strftime("%d/%m/%Y %H:%M:%S")
        else:
            self.time_end = date.strftime("%d/%m/%Y %H:%M:%S")

    def matches(self):
        """
        Aims : store the matchs as string with player's ident, to be
        store in the database.
        params : None
        return : None
        """
        for match in self.round_matches:
            match_saved = {'id_player_1': match[0].ident,
                           'id_player_2': match[1].ident}
            self.saved_matches.append(match_saved)

    def match_results(self, players, index):
        """
        Aims : store each match result as a tuple of  2 lists :each list is
        the name and ident of the player, and results of the match. It also
        change the player's instance points via the new_points method of
        Joueurs class.
        params :
        -players : list of a pair of players instances (matches)
        -index : int, user selection to determine the winner (or a draw). sent
        by the results_menu method, of the Menu class
        return : None
        """
        if index == 0:
            players[index].new_points(1)
            p1 = [players[0].family_name + ', ' + players[
                0].name + ' (id:' + str(players[0].ident) + ')', 1]
            p2 = [players[1].family_name + ', ' + players[
                1].name + ' (id:' + str(players[1].ident) + ')', 0]
            self.results.append((p1, p2))
        elif index == 1:
            players[index].new_points(1)
            p1 = [players[0].family_name + ', ' + players[
                0].name + ' (id:' + str(players[0].ident) + ')', 0]
            p2 = [players[1].family_name + ', ' + players[
                1].name + ' (id:' + str(players[1].ident) + ')', 1]
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
        Aims : constructor, player's infos attributes
        params :
        -ident : int, attribute that set a identifier for each player
        -family_name : str
        -name : str
        -dob : str of date of birth
        -sex : str
        -rank : int
        -point : float (default : 0)
        returns : None
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
        Aims : change the rank of the player
        :params :
        -new_rank : int
        return : None
        """
        self.rank = new_rank

    def new_points(self, new_points):
        """
        Aims : change the points of the player
        params :
        -new_points : float
        """
        self.points += new_points

    def mod_player(self):
        """
        Aims : allow the user to change the player infos.
        params : None
        return : None
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
        Aims : serialized the player's instance so it can be stored.
        params : None
        return : None
        """
        serialize_p = {'ident': self.ident,
                       'family_name': self.family_name,
                       'name': self.name, 'dob': self.dob,
                       'sex': self.sex, 'rank': self.rank,
                       'points': self.points}
        return serialize_p


class Report:
    """
    Create a Report objet to display tournaments reports.
    """

    def __init__(self):
        """
        Aims : Creat a variable of the finished tournament folder
        params : None
        return : None
        """
        self.main_folder = 'Tournois/Terminés/'

    def all_players(self):
        """
        Aims : print all players that have played in stored tournaments
        params : None
        return : None
        """

        tournament_list = []
        actors_list = []

        # geting the list of stored finish tournaments
        # TODO : remplacer glob par autre chose, et utiliser regex pour le nom de fichier
        for files in glob(self.main_folder + '*.json'):
            strip_file_name = files[18:-5]
            tournament_list.append(strip_file_name)

        # looping through each stored tournaments to extract players list, then
        # adding them in actors_list as dictionaries
        for file in tournament_list:
            saved_tournament = TournamentData(file=self.main_folder + file,
                                              resume=True)

            for player in saved_tournament.players_table:
                family_name = player['family_name']
                name = player['name']
                rank = player['rank']
                player = {'family_name': family_name, 'name': name,
                          'rank': rank}
                actors_list.append(player)
            del saved_tournament

        # sorting players list by name and by rank
        actors_name = sorted(actors_list, key=itemgetter('family_name'))
        actors_rank = sorted(actors_list, key=itemgetter('rank'),
                             reverse=True)

        print(
            'Ensemble des joueurs enregistrés (par ordre alphabetique) : \n')
        for actors in actors_name:
            actor_name = actors['family_name'] + ', ' + actors['name']
            print(actor_name)

        print('\n-------------------\n')

        print('Ensemble des joueurs enregistrés (par classement) :\n')
        for actors in actors_rank:
            actor_rank = (
                    str(actors['rank']) + ' : ' + actors['family_name']
                    + ', ' + actors['name'])
            print(actor_rank)

        # allow the program to wait for a user input to display the previous
        # menu
        input('\n Appuyez sur <Entrée> pour retourner au menu.')
        return

    def tournament_players(self, file):
        """
        Aims : display the list of player of a selected tournament
        params :
        -file : str of the selected tournament file name
        return : None
        """
        sel_tournament = TournamentData(resume=True,
                                        file=self.main_folder + file)

        # TODO : regex pour nom de fichier
        print('Joueurs du tournois ' + file[18:] + ' :\n')
        # getting players serialized infos
        for player in sel_tournament.players_table:
            family_name = player['family_name']
            name = player['name']
            print(family_name + ', ' + name)
        del sel_tournament

        # allow the program to wait for a user input to display the previous
        # menu
        input('\n Appuyez sur <Entrée> pour retourner au menu.')
        return

    def tournament_rounds(self, file):
        """
        Aims : display all rounds of a selected tournament
        params :
        -file : str of the selected tournament file name
        return : None
        """
        sel_tournament = TournamentData(resume=True,
                                        file=self.main_folder + file)
        players = []
        doc_in_table = 2
        tournament_rounds = []
        round_number = 1

        # getting players names and identifyer from the database, then storing
        # them as dict in a list
        for player in sel_tournament.players_table:
            family_name = player['family_name']
            name = player['name']
            ident = player['ident']
            player = {'family_name': family_name, 'name': name,
                      'ident': ident}
            players.append(player)

        players_sorted = sorted(players, key=itemgetter('ident'))

        rounds_infos = sel_tournament.tournaments_table.get(
            doc_id=doc_in_table)

        # for each round in the tournament, getting the matchs' pairs, then
        # storing them in a list, based on their identifyer
        while rounds_infos:
            round_matchs = []
            matchs = rounds_infos['matchs']
            for i in matchs:
                p1 = players_sorted[i['id_player_1']]
                p2 = players_sorted[i['id_player_2']]
                round_matchs.append([p1, p2])
            tournament_rounds.append(round_matchs)
            doc_in_table += 1
            rounds_infos = sel_tournament.tournaments_table.get(
                doc_id=doc_in_table)

        # printing each matchs from each rounds.
        for rounds in tournament_rounds:
            print('\nRound ' + str(round_number))
            for i in rounds:
                p1 = i[0]['family_name'] + ', ' + i[0]['name']
                p2 = i[1]['family_name'] + ', ' + i[1]['name']
                print(p1 + ' - ' + p2)
            round_number += 1
        del sel_tournament

        # allow the program to wait for a user input to display the previous
        # menu
        input('\n Appuyez sur <Entrée> pour retourner au menu.')
        return

    def tournament_matchs(self, file):
        """
        Aims : display the list of matchs and their results of a selected
        tournament
        params :
        -file : str of the selected tournament file name
        return : None
        """
        sel_tournament = TournamentData(resume=True,
                                        file=self.main_folder + file)

        doc_in_table = 2
        tournament_rounds = []
        round_number = 1

        rounds_infos = sel_tournament.tournaments_table.get(
            doc_id=doc_in_table)

        # for each round in the tournament, getting the results, then
        # storing them in a list, based on their identifyer
        while rounds_infos:
            round_matchs = []
            matchs = rounds_infos['results']
            for i in matchs:
                p1 = i[0][0][:-7] + ' : ' + str(i[0][1])
                p2 = i[1][0][:-7] + ' : ' + str(i[1][1])
                round_matchs.append([p1, p2])
            tournament_rounds.append(round_matchs)
            doc_in_table += 1
            rounds_infos = sel_tournament.tournaments_table.get(
                doc_id=doc_in_table)

        # printing each matchs' results from each rounds.
        for rounds in tournament_rounds:
            print('\nRound ' + str(round_number))
            for i in rounds:
                print(i[0] + ' / ' + i[1])
            round_number += 1
        del sel_tournament

        input('\n Appuyez sur <Entrée> pour retourner au menu.')
        return
