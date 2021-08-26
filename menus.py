from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import *
from operator import attrgetter
from control import Tournois


# from data_base import Tournament_data


class Menus:

    def __init__(self):
        self.T = None
        main_menu = ConsoleMenu('Centre échecs', 'Gestionnaire de tournois')
        new_tournament = FunctionItem('Nouveau tournois', self.new_t, menu=main_menu)
        resume_tournament = FunctionItem('Reprendre un tournois', self.resume_t, menu=main_menu)
        tournament_report = FunctionItem('Rapport de tournois', self.report_t, menu=main_menu)
        main_menu.append_item(new_tournament)
        main_menu.append_item(resume_tournament)
        main_menu.append_item(tournament_report)
        main_menu.show()
        self.player_name_sort = []

    def new_t(self):
        # methode appelant un nouvel objet Tournois, puis lançant l'affichage de menu de tournoi
        self.T = Tournois()
        self.T.add_players()
        self.player_name_sort = sorted(self.T.players, key=attrgetter('family_name'))
        self.tournament()

    def tournament(self):
        # TODO : affichage du round en cours
        tournament_menu = ConsoleMenu('Centre échecs', self.T.name + ' - ' + self.T.time)
        display_ranking = FunctionItem('Voire classement du tournois', self.dis_rank, menu=tournament_menu)
        rank_mod = FunctionItem('Modification classement', self.mod_rank_menu, menu=tournament_menu)
        view_players = FunctionItem('Voir les joueurs du tournois', self.dis_players, menu=tournament_menu)
        rounds = FunctionItem('Voire les tours du tournois', self.show_round, menu=tournament_menu)
        save_tournament = FunctionItem('Sauvegarder le tournois', self.save_tournament, menu=tournament_menu)
        tournament_menu.append_item(rounds)
        tournament_menu.append_item(display_ranking)
        tournament_menu.append_item(rank_mod)
        tournament_menu.append_item(view_players)
        tournament_menu.append_item(save_tournament)
        tournament_menu.show()

    def save_tournament(self):
        return

    def resume_t(self):
        return

    def report_t(self):
        return

    def dis_rank(self):
        # menu classement
        players_list = sorted(self.T.players, key=attrgetter('rank'), reverse=True)
        players_rank = []
        for i in players_list:
            players_rank.append(str(i.rank) + ' : ' + i.family_name + ', ' + i.name)
        rank_menu = SelectionMenu(players_rank, 'Center échecs', 'Classement')
        rank_menu.show()

    def dis_players(self):
        players_name = []
        for i in self.player_name_sort:
            players_name.append(i.family_name + ', ' + i.name)
        players_menu = SelectionMenu(players_name, 'Center échecs', 'Joueurs')
        players_menu.show()

    def mod_rank_menu(self):
        players_name = []
        for i in self.player_name_sort:
            players_name.append(i.family_name + ', ' + i.name + ' : ' + str(i.rank))
        sel = SelectionMenu.get_selection(players_name, 'Centre échecs', 'Modification du classement')
        new_rank = int(input(
            'Quel est le nouveau classement de ' + self.player_name_sort[sel].name + ' ' + self.player_name_sort[
                sel].family_name + ' ?'))
        self.player_name_sort[sel].new_rank(new_rank)

    def show_round(self):
        # utiliser selection menu pour créer la liste des menu en fonction de la liste des round
        # TODO : implementer la visualisation pour les autres rounds
        round_liste = []
        for i in self.T.round[0]:
            round_liste.append(i[0].name + ' ' + i[0].family_name + ' contre ' + i[1].name + ' ' + i[1].family_name)

        print(round_liste)
        rounds_menu = SelectionMenu(round_liste, 'Centre Echecs', 'Rounds')
        rounds_menu.show()



if __name__ == '__main__':
    main = Menus()
