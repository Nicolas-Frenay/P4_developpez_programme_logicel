import json
from operator import attrgetter


class Tournois:
    def __init__(self):
        """

        """
        # self.name = input('Nom du tournois ?')
        # self.place = input('Lieu du tournois ?')
        # self.date_start = input('Date de debut du tournois? (DD/MM/YYYY)')
        # self.date_end = input('Date de fin du tournois ? (DD/MM/YYYY)')
        # self.time = input('Quelle est le format des match (bullet, blitz,
        # coup rapide') ?
        # self.desc = input('Description du tournois ?')
        # self.turns = input('En combien de tours se déroule le tournois ?
        # (defaut : 4)') or 4
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

        self.players = []
        self.round_generator = None
        self.current_round = None
        self.rounds_list = []

    def add_players(self, nombre_de_joueur=8):
        """

        :param nombre_de_joueur:
        :return:
        """
        # TODO:-ajout dans TinyDB

        # for i in range(0, nombre_de_joueur):
        #     family_name = input('Nom de famille du joueur {} ?'.format(i))
        #     name = input('Prénom du joueur {} ?'.format(i))
        #     dob = input('Date de naissance du joueur {} (DD/MM/YYYY) ?'
        #                 .format(i))
        #     sex = input('Sex du joueur {} (H/F) ?'.format(i))
        #     rank = int(input('Classement du joueur {} ?'.format(i)))
        #
        #     self.players.append(Joueurs(family_name, name, dob, sex, rank))
        #
        # Temporaire pour les test, charge fichier json pour éviter de retaper
        # les 8 joueurs a chaque fois:
        with open('joueurs.json') as f:
            data = json.load(f)
            for i in data:
                self.players.append(
                    Joueurs(i['family_name'], i['name'], i['dob'], i['sex'],
                            i['rank'],
                            i['points']))
        f.close()
        #
        #
        #
        # TODO : temporaire, ne doit pas s'effectuer en cas de chargement de
        #  tournois (flag booléen en argument ?)
        self.round_generator = Rounds(self.players)
        self.current_round = 0
        self.rounds_list.append(self.round_generator.first_round())

    def save_tournament(self):
        return

    def resume_tournament(self):
        """
        *
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.time = time
        self.joueurs = joueurs
        self.desc = desc
        """
        return

    def enter_results(self):
        self.current_round += 1
        new_round = self.round_generator.next_round()
        self.rounds_list.append(new_round)


# TODO : timestamp pour les rounds =
#  https://www.programiz.com/python-programming/datetime/current-datetime
class Rounds:
    def __init__(self, players_list):
        self.players = players_list
        self.rounds_list = []
        self.results = [[], ]
        self.first_round()

    def first_round(self):
        """
        tri des joueurs selon la methode Suisse, et creation des matchs du
        premier tour dans une liste
        """
        # TODO : check si nombre joueurs impaire
        start_round_list = []
        players_list = sorted(self.players, key=attrgetter('rank'),
                              reverse=True)
        for i in range(0, len(players_list) // 2):
            start_round_list.append(
                [players_list[i], players_list[i + len(players_list) // 2]])
        self.rounds_list.append(start_round_list)
        return start_round_list

    def next_round(self):
        # TODO : exceptions si joueurs se sont déjà rencontré
        new_round = []
        i = 0
        tmp = sorted(self.players, key=attrgetter('points', 'rank'),
                     reverse=True)
        while i < len(tmp):
            new_round.append([tmp[i], tmp[i + 1]])
            i += 2
        self.rounds_list.append(new_round)
        return new_round
        # TODO : terminer tournois et sauvegarder si self.round_number < 4

    # TODO : les resultat de chaque matche doivent etre un tuple
    #  ([Joueur1, resultat], [Joueur2, resultat])
    def match_results(self, players, index, current_round):

        round_results = []

        if index == 0 or index == 1:
            players[index].new_points(1)
            p1 = [players[index].name + ' ' + players[index].family_name, 1]
            players.pop(index)
            p2 = [players[0].name + ' ' + players[0].family_name, 0]
            self.results[current_round].append((p1, p2))
        else:
            players[0].new_points(0.5)
            players[1].new_points(0.5)
            p1 = [players[0].name + ' ' + players[0].family_name, 0.5]
            p2 = [players[1].name + ' ' + players[1].family_name, 0.5]
            self.results[current_round].append((p1, p2))


class Joueurs:
    """

    """

    def __init__(self, family_name, name, dob, sex, rank, points=0.):
        # TODO : check self.id(self), pour éviter un attribut inutile
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
