import json
from operator import attrgetter
from datetime import datetime
from data_base import TournamentData


class Tournois:
    def __init__(self, file=None, resume=False):
        """

        """
        self.players = []
        self.current_round = None
        self.rounds_list = []
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

            # Temporaire pour les test, charge fichier json pour éviter de retaper
            # les infos a chaque fois:
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

    def create_round(self):
        self.current_round = Rounds('Round ' + str(self.round_number))

    def add_players(self, nombre_de_joueur=8):
        """

        :param nombre_de_joueur:
        :return:
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
        #
        # Temporaire pour les test, charge fichier json pour éviter de retaper
        # les 8 joueurs a chaque fois:
        with open('joueurs.json') as f:
            data = json.load(f)
            for i in data:
                self.players.append(
                    Joueurs(i['ident'], i['family_name'], i['name'], i['dob'],
                            i['sex'], i['rank'], i['points']))
        f.close()

        first_round = self.first_round()
        self.rounds_list.append(first_round)
        self.create_round()
        self.current_round.matches(first_round)

    def save_tournament(self):
        tournament_save = TournamentData(self.name)

        players_list = []

        for i in self.players:
            players_list.append(i.serialize_player())

        tournament_save.players_table.truncate()
        tournament_save.players_table.insert_multiple(players_list)

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

        tournament_save.save_tournament(tournament_infos)

    @staticmethod
    def save_rounds(rounds):
        name = rounds.name
        results = rounds.results
        time_start = rounds.time_start
        time_end = rounds.time_end
        matchs = rounds.round_matches
        round_to_save = {'name': name, 'results': results, 'matchs': matchs,
                         'time_start': time_start, 'time_end': time_end}
        return round_to_save

    def resume_tournament(self, file):
        resumed_tournament = TournamentData(resume=True, file=file)

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

        tournament_infos = resumed_tournament.tournaments_table.get(doc_id=1)
        self.name = tournament_infos['name']
        self.place = tournament_infos['place']
        self.date_start = tournament_infos['date_start']
        self.date_end = tournament_infos['date_end']
        self.time = tournament_infos['time']
        self.desc = tournament_infos['description']
        self.turns = tournament_infos['turns']
        self.round_number = tournament_infos['round_number']

    def enter_results(self):
        new_round = self.next_round()
        self.rounds_list.append(new_round)
        self.round_number += 1
        if self.round_number <= 4:
            self.current_round.time_stamp(end=True)
            self.rounds.append(self.current_round)
            self.create_round()
            self.current_round.matches(new_round)
        else:
            self.tournament_finish = True

    def first_round(self):
        """
        tri des joueurs selon la methode Suisse, et creation des matchs du
        premier tour dans une liste
        """
        start_round_list = []
        players_list = sorted(self.players, key=attrgetter('rank'),
                              reverse=True)
        for i in range(0, len(players_list) // 2):
            start_round_list.append(
                [players_list[i], players_list[i + len(players_list) // 2]])
        return start_round_list

    def next_round(self):
        # TODO : exceptions si joueurs se sont déjà rencontré
        new_round = []
        i = 1
        tmp = sorted(self.players, key=attrgetter('points', 'rank'),
                     reverse=True)

        while tmp:
            for tours in self.rounds_list:
                if [tmp[0], tmp[i]] in tours:
                    i = 2
                if len(tmp) < 3:
                    i = 1
            new_round.append([tmp[0], tmp[i]])
            tmp.pop(i)
            tmp.pop(0)

        return new_round


class Rounds:
    def __init__(self, name):
        self.results = []
        self.name = name
        self.round_matches = []
        self.time_start = None
        self.time_end = None
        self.time_stamp()

    def time_stamp(self, end=False):
        date = datetime.now()

        if not end:
            self.time_start = date.strftime("%d/%m/%Y %H:%M:%S")
        else:
            self.time_end = date.strftime("%d/%m/%Y %H:%M:%S")

    def matches(self, matches):
        for i in matches:
            self.round_matches.append(
                {'id_player_1': i[0].ident, 'id_player_2': i[1].ident})

    def match_results(self, players, index):

        if index == 0 or index == 1:
            players[index].new_points(1)
            p1 = [players[index].family_name + ', ' + players[
                index].name + ' (id:' + str(players[index].ident) + ')', 1]
            players.pop(index)
            p2 = [players[0].family_name + ', ' + players[
                0].name + ' (id:' + str(players[0].ident) + ')', 0]
            print(p1)
            print(p2)
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

    """

    def __init__(self, ident, family_name, name, dob, sex, rank, points=0.):
        self.ident = ident
        self.family_name = family_name
        self.name = name
        self.dob = dob
        self.sex = sex
        self.rank = rank
        self.points = points

    def new_rank(self, new_rank):
        self.rank = new_rank

    def new_points(self, new_points):
        self.points += new_points

    def mod_player(self):
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
        serialize_p = {'ident': self.ident, 'family_name': self.family_name,
                       'name': self.name, 'dob': self.dob,
                       'sex': self.sex, 'rank': self.rank,
                       'points': self.points}
        return serialize_p


if __name__ == '__main__':
    T = Tournois()
    T.add_players()
    print(T.current_round.round_matches)
