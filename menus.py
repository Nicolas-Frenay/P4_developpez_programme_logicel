from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, MenuItem
from operator import attrgetter
from control import Tournois, Report
from glob import glob


class Menus:
    """
    Class that handle all the display of the programme
    """

    def __init__(self):
        """
        constructor creat a variable for storing a Tournois, calling the main
        menu, and an empty list for the players instances, which will be sorted
         by their family name, as this list is used multiple times in the
         program.
        """
        self.T = None
        self.player_name_sort = []
        self.first_menu()
        self.report = None

    def first_menu(self):
        """
        Methode creating the first menu, from which the user can either create
        a tournament, resume one, or do a report of a tournament.
        """
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

    def new_t(self):
        """
        method calling a Tournois instance, which will stores it as a class
        attribute. It then call the add_players method for creating 8 Joueur
        instances, then sort them by name and store them in a class list.
        Finally, it called the tournament menu.
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
        view_players = FunctionItem('Voir les joueurs du tournois',
                                    self.dis_players, menu=tournament_menu)
        mod_player = FunctionItem('Modifier un joueur', self.mod_player,
                                  menu=tournament_menu)
        rounds = FunctionItem('Voire les tours du tournois', self.show_rounds,
                              menu=tournament_menu)
        enter_results = FunctionItem('Entrer les résultats du tour en cours',
                                     self.enter_results, menu=tournament_menu)
        display_ranking = FunctionItem('Voire classement du tournois',
                                       self.dis_rank, menu=tournament_menu)
        rank_mod = FunctionItem('Modification classement', self.mod_rank_menu,
                                menu=tournament_menu)
        save_tournament = FunctionItem('Sauvegarder le tournois',
                                       self.save_tournament,
                                       menu=tournament_menu)

        tournament_menu.append_item(view_players)
        tournament_menu.append_item(mod_player)
        tournament_menu.append_item(rounds)
        tournament_menu.append_item(enter_results)
        tournament_menu.append_item(display_ranking)
        tournament_menu.append_item(rank_mod)
        tournament_menu.append_item(save_tournament)
        tournament_menu.show()

    def dis_players(self):
        """
        Method displaying players sorted by family name.
        """
        players_name = []

        for i in self.player_name_sort:
            players_name.append(i.family_name + ', ' + i.name)

        players_menu = SelectionMenu(players_name, 'Center échecs', 'Joueurs')
        players_menu.show()

    def mod_player(self):
        """
        Method which display a menu to modify a player's infos.
        """
        players_name = []

        for i in self.player_name_sort:
            players_name.append(
                i.family_name + ', ' + i.name + ' : ' + str(i.rank))
        sel = SelectionMenu.get_selection(players_name, 'Centre échecs',
                                          'Modification de joueur')

        if sel < 8:
            self.player_name_sort[sel].mod_player()
            self.dis_players()
            self.save_tournament()
        else:
            pass

    def show_rounds(self, new_round=False):
        """
        Methode creating a menu that displays the rounds already created. At
        first it show only the first, then when the other are generate, they
        will show accordingly.
        When one round is selected, it called the round_menu method, which will
        display the matchs of that round.
        is the argument new_round is True, it will display the latest round
        created.
        """
        list = self.T.get_round_matchs()
        round_liste = []
        round_to_display = []
        displayed_round = ['Premier', 'Second', 'Troisième', 'Quatrième']
        rounds_sel = None

        if not new_round:
            # Creating the displayed menu items by creating a list of
            # names-string for each rounds.
            for i in range(0, len(list)):
                round_liste.append(displayed_round[i] + ' tours.')

            # the get_selection method allows to get the user's choice
            rounds_sel = SelectionMenu.get_selection(round_liste,
                                                     'Centre Echecs', 'Rounds')

        else:
            rounds_sel = -1

            # making the user input call the appropriate round menu. If the
            # user select the last item (the menu "exit"), it will passe.
        if rounds_sel > len(list) - 1:
            pass

        # creating a list of the players playing against each other by
        # calling there attributes, then sending this list to the round_menu
        # method to display it.
        else:
            for i in list[rounds_sel]:
                round_to_display.append(
                    i[0].name + ' ' + i[0].family_name + ' contre ' + i[
                        1].name + ' ' + i[1].family_name)
            if rounds_sel == -1:
                self.round_menu(round_to_display,
                                round_num=self.T.round_number)
            else:
                self.round_menu(round_to_display, round_num=rounds_sel + 1)

    @staticmethod
    def round_menu(round_show, round_num):
        """
        Method that display the matchs of the selected round in the menu of
        show_rounds method.
        """

        rounds_menu = ConsoleMenu('Centre Echecs',
                                  'Round ' + str(round_num))

        for i in range(0, len(round_show)):
            tmp = MenuItem(round_show[i], menu=rounds_menu, should_exit=False)
            rounds_menu.append_item(tmp)

        rounds_menu.show()

    def enter_results(self):
        """
        method that get each pair of players from the round, and pass them to
        the result menu. then it called the enter_result method of the Tournois
        class.
        If the Tournament is finish (4 rounds played), it display the end menu.
        Otherwise, it shows the next round's matchs.
        """
        current_round = self.T.current_round.round_matches

        for item in current_round:
            self.results_menu(item)
        self.T.enter_results()

        # Checking if this is the last round of the tournament.
        if not self.T.tournament_finish:
            self.show_rounds(True)
        else:
            self.end_tournament()

    def results_menu(self, players):
        """
        Methode that get a list of 2 players, and ask the user which one wons
        (or if this was a draw).
        The user selection is use to call the method match_results from the
        Round class, that will store the results as tuples.
        """
        players_list = []
        for i in range(0, len(players)):
            players_list.append(players[i].name + ' '
                                + players[i].family_name)

        players_list.append('Match nul')
        result_menu = SelectionMenu.get_selection(players_list,
                                                  'Centre échecs',
                                                  'Indiquez le vainqueur '
                                                  'ou le match nul')

        # This is to avoid an index error, since the result_menu variable is
        # the user selection, and the last choice of the menu is the exit of
        # the menu
        if result_menu < 3:
            self.T.current_round.match_results(players, result_menu)

    def end_tournament(self):
        """
        Simple menu, that display the final results of the tournaments.
        (players sorted by their points)
        """
        players_list = sorted(self.T.players, key=attrgetter('points'),
                              reverse=True)
        players_rank = []

        for i in players_list:
            players_rank.append(
                i.family_name + ' ' + i.name + ' : ' + str(i.points))

        end_menu = SelectionMenu(players_rank, 'Center échecs',
                                 'Fin de tournois',
                                 prologue_text='résultats finaux')
        self.save_tournament()
        end_menu.show()

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

        # This is to avoid index error, since the last menu selection is the
        # exit one.
        if sel < 8:
            new_rank = int(input(
                'Quel est le nouveau classement de ' + self.player_name_sort[
                    sel].name + ' ' + self.player_name_sort[
                    sel].family_name + ' ?'))
            self.player_name_sort[sel].new_rank(new_rank)
            self.save_tournament()
        else:
            pass

    def save_tournament(self):
        """
        Method for saving the tournament, player and rounds in a JSon database
        calling a Tournois method.
        """
        self.T.save_tournament()

    def resume_t(self):
        """
        Method that will call a save tournament and load it
        It get a list of json files, then displays it.
        """
        tournament_list = []
        for files in glob('Tournois/Interrompus/*.json'):
            tournament_list.append(files[21:-5])
        sel = SelectionMenu.get_selection(tournament_list, 'Centre échecs',
                                          "Reprise d'un tournois interrompu")

        # This is to avoid index error, since the last menu selection is the
        # exit one.
        if sel < len(tournament_list):
            self.T = Tournois(
                file='Tournois/Interrompus/' + tournament_list[sel],
                resume=True)
            self.player_name_sort = sorted(self.T.players,
                                           key=attrgetter('family_name'))
            self.tournament()
        else:
            pass

    def report_t(self):
        """
        Methode that will generate a menu to display a report
        """
        # faire un menu qui permet de choisir entre :
        # -liste de tout les joueurs ayant participés a un tournois, classés
        # par ordre alphabetique ET par classement

        # self.report.all_players()

        # -liste de tout les tournois
        # -liste des tours d'un tournois (juste les matchs)
        # -list de tout les matchs d'un tournois (avec resultats)
        self.report = Report()
        args_list = [[True, False, False, False], [False, True, False, False],
                     [False, False, True, False], [False, False, False, True]]
        report_menu = ConsoleMenu('Centre échecs', 'menu de rapport')

        show_all_actors = FunctionItem('Voir tout les acteurs',
                                       self.report.all_players,
                                       menu=report_menu)

        show_all_tournament = FunctionItem('Voir tout les tournois términés',
                                           self.sel_tournament,
                                           args=args_list[3])

        show_all_T_players = FunctionItem(
            "Voir tout les joueurs d'un tournois",
            self.sel_tournament, args=args_list[0], menu=report_menu)

        show_T_rounds = FunctionItem('Voir les rounds d\'un tournois',
                                     self.sel_tournament, args=args_list[1])

        report_menu.append_item(show_all_actors)
        report_menu.append_item(show_all_tournament)
        report_menu.append_item(show_all_T_players)
        report_menu.append_item(show_T_rounds)
        report_menu.show()

    def sel_tournament(self, players=False, rounds=False, matchs=False,
                       tournaments=False):
        tournament_list = []
        # folder = 'Tournois/Terminés/'

        for files in glob(folder + '*.json'):
            tournament_list.append(files[18:-5])

        if tournaments:
            menu = ConsoleMenu('Centre échecs', 'Liste de tournois términés')
            for i in tournament_list:
                tmp = MenuItem(i, menu=menu, should_exit=True)
                menu.append_item(tmp)
            menu.show()

        else:
            sel = SelectionMenu.get_selection(tournament_list, 'Centre échecs',
                                              'Pour quel tournois souhaitez '
                                              'vous générer un rapport ?')

            if players:
                self.report.tournament_players(tournament_list[sel])

            elif rounds:
                self.report.tournament_rounds(tournament_list[sel])

            elif matchs:
                return


if __name__ == '__main__':
    main = Menus()
