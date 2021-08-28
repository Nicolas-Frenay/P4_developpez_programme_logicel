from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, MenuItem
from operator import attrgetter
from control import Tournois


class Menus:
    """
    Class that handle all the display of the programme
    """

    def __init__(self):
        """
        constructor creat a variable for Tournois instance, the main menu, and
        an empty list for the players instances, which will be sorted by their
        family name, as this list is used multiple times in the program.
        """
        self.T = None
        # self.R = None
        main_menu = ConsoleMenu('Centre échecs', 'Gestionnaire de tournois')
        new_tournament = FunctionItem('Nouveau tournois', self.new_t,
                                      menu=main_menu)
        resume_tournament = FunctionItem('Reprendre un tournois',
                                         self.resume_t, menu=main_menu)
        tournament_report = FunctionItem('Rapport de tournois', self.report_t,
                                         menu=main_menu)
        main_menu.append_item(new_tournament)
        main_menu.append_item(resume_tournament)
        main_menu.append_item(tournament_report)
        main_menu.show()
        self.player_name_sort = []

    def new_t(self):
        """
        method calling a Tournois instance, which will store as a class
        attribute. It then call the add_players method for creating 8 Joueur
        instances, then sort them by name and store them in a class list.
        """
        self.T = Tournois()
        self.T.add_players()
        self.player_name_sort = sorted(self.T.players,
                                       key=attrgetter('family_name'))
        self.tournament()

    def tournament(self):
        """
        Method creating and displaying tournament menu.
        Each element of the menu are calling class method.
        """
        tournament_menu = ConsoleMenu('Centre échecs',
                                      self.T.name + ' - ' + self.T.time)
        display_ranking = FunctionItem('Voire classement du tournois',
                                       self.dis_rank, menu=tournament_menu)
        rank_mod = FunctionItem('Modification classement', self.mod_rank_menu,
                                menu=tournament_menu)
        view_players = FunctionItem('Voir les joueurs du tournois',
                                    self.dis_players, menu=tournament_menu)
        rounds = FunctionItem('Voire les tours du tournois', self.show_rounds,
                              menu=tournament_menu)
        save_tournament = FunctionItem('Sauvegarder le tournois',
                                       self.save_tournament,
                                       menu=tournament_menu)
        enter_results = FunctionItem('Entrer les résultats du tour en cours',
                                     self.enter_results, menu=tournament_menu)
        tournament_menu.append_item(view_players)
        tournament_menu.append_item(rounds)
        tournament_menu.append_item(enter_results)
        tournament_menu.append_item(display_ranking)
        tournament_menu.append_item(rank_mod)
        tournament_menu.append_item(save_tournament)
        tournament_menu.show()

    def enter_results(self):
        current_round = self.T.rounds_list[-1]
        for item in current_round:
            self.results_menu(item)
        self.T.enter_results()
        self.show_rounds(True)

    def results_menu(self, players):

        players_list = []

        for i in range(0, len(players)):
            players_list.append(players[i].name + ' '
                                + players[i].family_name)
        players_list.append('Match nul')
        result_menu = SelectionMenu.get_selection(players_list,
                                                  'Centre échecs',
                                                  'Indiquez le vainqueur '
                                                  'ou le match nul')

        if result_menu < 3:
            self.T.current_round.match_results(players, result_menu)
        # TODO : terminer tournois au dernier tour

    def save_tournament(self):
        """
        Method for saving the tournament, player and rounds in a JSon database
        :return:
        """
        return

    def resume_t(self):
        """
        Method that will call a save tournament and load it
        :return:
        """
        return

    def report_t(self):
        """
        Methode that will generate a report of the tournament
        :return:
        """
        return

    def dis_rank(self):
        """
        Method displaying player sorted by rank.
        """
        players_list = sorted(self.T.players, key=attrgetter('rank'),
                              reverse=True)
        players_rank = []

        for i in players_list:
            players_rank.append(
                str(i.rank) + ' : ' + i.family_name + ', ' + i.name)

        rank_menu = SelectionMenu(players_rank, 'Center échecs', 'Classement')
        rank_menu.show()

    def dis_players(self):
        """
        Method displaying players sorted by family name.
        """
        players_name = []

        for i in self.player_name_sort:
            players_name.append(i.family_name + ', ' + i.name)

        players_menu = SelectionMenu(players_name, 'Center échecs', 'Joueurs')
        players_menu.show()

    def mod_rank_menu(self):
        """
        Method creating a menu to modify rank during tournament :
        it displays players, then the user choose which one to edit, and it
        change the rank attribut to the player instance, via the
        Joueur.new_rank() methode.
        """
        players_name = []

        for i in self.player_name_sort:
            players_name.append(
                i.family_name + ', ' + i.name + ' : ' + str(i.rank))
        sel = SelectionMenu.get_selection(players_name, 'Centre échecs',
                                          'Modification du classement')

        if sel < 8:
            new_rank = int(input(
                'Quel est le nouveau classement de ' + self.player_name_sort[
                    sel].name + ' ' + self.player_name_sort[
                    sel].family_name + ' ?'))
            self.player_name_sort[sel].new_rank(new_rank)
        else:
            pass

    def show_rounds(self, new_round=False):
        """
        Methode creating a menu that displays the rounds already created. At
        first it show only the first, then when the other are generate, they
        will show accordingly.
        When one round is selected, it called the round_menu method, which will
        display the matchs of that round.
        """
        list = self.T.rounds_list
        round_liste = []
        round_to_display = []
        displayed_round = ['Premier', 'Second', 'Troisième', 'Quatrième']
        rounds_sel = None

        if not new_round:
            # Creating the displayed menu items
            for i in range(0, len(list)):
                round_liste.append(displayed_round[i] + ' tours.')
            rounds_sel = SelectionMenu.get_selection(round_liste,
                                                     'Centre Echecs', 'Rounds')
        else:
            rounds_sel = -1

            # making the user input call the appropriate round menu
        if rounds_sel > len(list) - 1:
            pass
        else:
            for i in list[rounds_sel]:
                round_to_display.append(
                    i[0].name + ' ' + i[0].family_name + ' contre ' + i[
                        1].name + ' ' + i[1].family_name)

            self.round_menu(round_to_display)

    def round_menu(self, round_show):
        """
        Method that display the matchs of the selected round in the menu of
        show_rounds method.
        """

        rounds_menu = ConsoleMenu('Centre Echecs',
                                  self.T.current_round.name)

        for i in range(0, len(round_show)):
            tmp = MenuItem(round_show[i], menu=rounds_menu, should_exit=False)
            rounds_menu.append_item(tmp)

        rounds_menu.show()


if __name__ == '__main__':
    main = Menus()
