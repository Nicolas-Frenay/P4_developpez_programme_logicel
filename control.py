import json


class Tournois:
    def __init__(self):
        self.name = input('Nom du tournois ?')
        self.place = input('Lieu du tournois ?')
        self.date_start = input('Date de debut du tournois? (DD/MM/YYYY)')
        self.date_end = input('Date de fin du tournois ? (DD/MM/YYYY)')
        self.time = input('Quelle est le format des match ? (bullet, blitz, coup rapide')
        self.desc = input('Description du tournois ?')
        self.player = []
        self.player_infos = []
        self.add_players()

    def add_players(self, nombre_de_joueur=8):
        """
        TO DO:
        -ajout dans TinyDB
        -self.rounds_list()
        """
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
        # Ca ca marche:
        with open('joueurs.json') as f:
            data = json.load(f)
            for i in data:
                self.player_infos.append(
                    {'family_name': i['family_name'], 'name': i['name'], 'dob': i['dob'], 'sex': i['sex'],
                     'rank': i['rank']})
                self.player.append(Joueurs(i['family_name'], i['name'], i['dob'], i['sex'], i['rank']))

    def rounds_list(self):
        """
        tri des joueurs selon la methode Suisse, et creatin des rounds dans une liste
        self.rounds = rounds
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


class Joueurs:
    def __init__(self, family_name, name, dob, sex, rank):
        self.family_name = family_name
        self.name = name
        self.dob = dob
        self.sex = sex
        self.rank = rank
        #
        # print(self.family_name, self.name, self.dob, self.sex, self.rank)
        #

    def new_rank(self, new_rank):
        self.rank = new_rank


if __name__ == '__main__':
    T = Tournois()
