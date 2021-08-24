import json


class Tournois:
    def __init__(self):
        """

        """
        # self.name = input('Nom du tournois ?')
        # self.place = input('Lieu du tournois ?')
        # self.date_start = input('Date de debut du tournois? (DD/MM/YYYY)')
        # self.date_end = input('Date de fin du tournois ? (DD/MM/YYYY)')
        # self.time = input('Quelle est le format des match (bullet, blitz, coup rapide') ?
        # self.desc = input('Description du tournois ?')
        # self.turns = input('En combien de tours se déroule le tournois ? (defaut : 4)') or 4
        # Temporaire pour les test, charge fichier json pour éviter de retaper les infos a chaque fois:
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

        self.current_round = 1
        self.players = []
        self.add_players()

    def add_players(self, nombre_de_joueur=8):
        """

        :param nombre_de_joueur:
        :return:
        """
        # TODO:-ajout dans TinyDB

        # for i in range(0, nombre_de_joueur):
        # family_name = input('Nom de famille du joueur {} ?'.format(i))
        # name = input('Prénom du joueur {} ?'.format(i))
        # dob = input('Date de naissance du joueur {} (DD/MM/YYYY) ?'.format(i))
        # sex = input('Sex du joueur {} (H/F) ?'.format(i))
        # rank = int(input('Classement du joueur {} ?'.format(i)))
        # self.player_infos.append(
        #     {'family_name': i['family_name'], 'name': i['name'], 'dob': i['dob'], 'sex': i['sex'],
        #      'rank': i['rank']})
        # self.player.append(Joueurs(family_name, name, dob, sex, rank))
        #
        # Temporaire pour les test, charge fichier json pour éviter de retaper les 8 joueurs a chaque fois:
        with open('joueurs.json') as f:
            data = json.load(f)
            for i in data:
                self.players.append(Joueurs(i['joueur'], i['family_name'], i['name'], i['dob'], i['sex'], i['rank'],
                                            i['points']))
        f.close()
        self.first_round()

    def first_round(self):
        """
        tri des joueurs selon la methode Suisse, et creation des rounds dans une liste
        """
        # TODO : check si nombre joueurs impaire
        start_round_list = []
        players_list = sorted(self.players, key=lambda k: k.rank, reverse=True)
        # TODO : /!\ attention, on trie les instances de joueurs, gérer l'affichage en fonction
        for i in range(0, len(players_list) // 2):
            start_round_list.append([players_list[i], players_list[i + len(players_list) // 2]])

    def next_round(self):
        """

        :return:
        """
        # TODO : exceptions si joueurs se sont déjà rencontré
        new_round = []
        i = 0
        tmp = sorted(self.players, key=lambda k: (k.points, k.rank), reverse=True)
        while i < len(tmp):
            new_round.append([tmp[i], tmp[i + 1]])
            i += 2

    def round_results(self, family_name):
        """

        :param family_name:
        :return:
        """


        return

    def resume_tournois(self):
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


# TODO : faire une classe round ?
# class Round:
#     def __init__(self, ):


class Joueurs:
    """

    """

    def __init__(self, joueur, family_name, name, dob, sex, rank, points=0):
        # TODO : check self.id(self), pour éviter un attribut inutile
        self.joueur = joueur
        self.family_name = family_name
        self.name = name
        self.dob = dob
        self.sex = sex
        self.rank = rank
        self.points = points

    def new_rank(self, new_rank):
        self.rank = new_rank

    def new_points(self, new_points):
        self.points = new_points


if __name__ == '__main__':
    T = Tournois()
    T.next_round()
