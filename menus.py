from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import *
from control import Tournois


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

    def new_t(self):
        # methode appelant un nouvel objet Tournois, puis lançant l'affichage de menu de tournoi
        self.T = Tournois()
        self.tournament()

    def tournament(self):
        # TODO : affichage du round en cours
        tournament_menu = ConsoleMenu('Centre échecs', self.T.name + ' - ' + self.T.time)
        display_ranking = FunctionItem('Voire classement du tournois', self.dis_rank, menu=tournament_menu)
        rank_mod = FunctionItem('Modification classement', self.mod_rank, menu=tournament_menu)
        view_players = FunctionItem('Voir les joueurs du tournois', self.dis_players, menu=tournament_menu)
        rounds = FunctionItem('Voire les tours du tournois', self.show_round(), menu=tournament_menu)
        tournament_menu.append_item(rounds)
        tournament_menu.append_item(display_ranking)
        tournament_menu.append_item(rank_mod)
        tournament_menu.append_item(view_players)
        tournament_menu.show()

    def resume_t(self):
        return

    def report_t(self):
        return

    def dis_rank(self):
        # menu classement
        players_list = sorted(self.T.player_infos, key=lambda k: k['rank'])
        players_rank = []
        for i in players_list:
            players_rank.append(str(i['rank']) + ' : ' + i['family_name'] + ', ' + i['name'])
        rank_menu = SelectionMenu(players_rank, 'Center échecs', 'Classement')
        rank_menu.show()

    def dis_players(self):
        players_list = sorted(self.T.player_infos, key=lambda k: k['family_name'])
        players_name = []
        for i in players_list:
            players_name.append(i['family_name'] + ', ' + i['name'])
        players_menu = SelectionMenu(players_name, 'Center échecs', 'Joueurs')
        players_menu.show()

    def mod_rank(self):
        # mod_classement = FunctionItem('classement', rank_menu, menu=rank_menu)
        return

    def show_round(self):
        # utiliser selection menu pour créer la liste des menu en fonction de la liste des round
        return


if __name__ == '__main__':
    main = Menus()
