from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, MenuItem
from operator import attrgetter
from control import Tournois, Report
import re
from glob import glob


class Menus:
    """
    Class that handle all the display of the program
    """

    def __init__(self):
        """
         Aims : constructor : Set base class attributes : two empty variables
         to store a Tournament object and a report object, an empty list to
         store players instances sorted by name, and display the first menu.
         params : None
         return : None
        """
        self.chess_tournament = None
        self.report = None
        self.player_name_sort = []
        self.first_menu()

    def first_menu(self):
        """
        Aims: Creating the first menu
        params : None
        Return: None
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
        Aims : Creating a new Tournois instanc, then calling add_players
        method, and sorting players instance by name in a list.
        Params : None
        Return : None
        """
        self.chess_tournament = Tournois()
        self.chess_tournament.add_players()
        self.player_name_sort = sorted(self.chess_tournament.players,
                                       key=attrgetter('family_name'))
        self.tournament()

    def tournament(self):
        """
        Aims : creating and displaying tournament menu.
        Params : None
        Return : None
        """
        tournament_menu = ConsoleMenu('Centre échecs',
                                      self.chess_tournament.name + ' - '
                                      + self.chess_tournament.time)
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
        self.save_tournament()
        tournament_menu.show()

    def dis_players(self):
        """
        Aims : displaying players sorted by family name.
        Params: None
        Return : None
        """
        players_name = []

        for player in self.player_name_sort:
            player_name = player.family_name + ', ' + player.name
            players_name.append(player_name)

        players_menu = SelectionMenu(players_name, 'Center échecs', 'Joueurs')
        players_menu.show()

    def mod_player(self):
        """
        Aims : Displaying the modify players menu
        Params : None
        Return : None
        """
        players_name = []

        for player in self.player_name_sort:
            player_name = (player.family_name + ', '
                           + player.name + ' : ' + str(player.rank))
            players_name.append(player_name)
        sel = SelectionMenu.get_selection(players_name, 'Centre échecs',
                                          'Modification de joueur')

        if sel < len(players_name):
            self.player_name_sort[sel].mod_player()
            self.save_tournament()
            self.dis_players()
        else:
            pass

    def show_rounds(self, new_round=False):
        """
        Aims : Displaying rounds menu, the user can select one to display
        matchs of that round.
        Params :
        -new_round : Boolean, if True, will display the last created
        round (which is the current one.)
        Return: None
        """
        list = self.chess_tournament.get_round_matchs()
        round_liste = []
        round_to_display = []
        displayed_round = ['Premier', 'Second', 'Troisième', 'Quatrième']
        rounds_sel = None

        if new_round:
            rounds_sel = -1
        else:
            # Creating the displayed menu items by creating a list of
            # names-string for each rounds.
            for index, rounds in enumerate(list):
                numbered_round = displayed_round[index] + ' tours.'
                round_liste.append(numbered_round)

            # the get_selection method allows to get the user's choice
            rounds_sel = SelectionMenu.get_selection(round_liste,
                                                     'Centre Echecs', 'Rounds')

            # making the user input call the appropriate round menu. If the
            # user select the last item (the menu "exit"), it will passe.
        if rounds_sel > len(list) - 1:
            pass

        # creating a list of the players playing against each other by
        # calling there attributes, then sending this list to the round_menu
        # method to display it, with the proper round number.
        else:
            for match in list[rounds_sel]:
                displayed_match = (match[0].name + ' ' + match[0].family_name
                                   + ' contre ' + match[1].name + ' '
                                   + match[1].family_name)
                round_to_display.append(displayed_match)
            if rounds_sel == -1:
                self.round_menu(round_to_display,
                                round_num=self.chess_tournament.round_number)
            else:
                self.round_menu(round_to_display, round_num=rounds_sel + 1)

    @staticmethod
    def round_menu(round_show, round_num):
        """
        Aims : Displaying matchs of the selected round
        Params :
        -round_show : list of matchs (pairs of players instance)
        -round_number : Current round number
        Return : None

        """

        rounds_menu = ConsoleMenu('Centre Echecs',
                                  'Round ' + str(round_num))

        for index, match in enumerate(round_show):
            tmp = MenuItem(round_show[index], menu=rounds_menu,
                           should_exit=False)
            rounds_menu.append_item(tmp)

        rounds_menu.show()

    def enter_results(self):
        """
        Aims : send each pair of players in result_menu, to register match's
        winner. If tournament is finish after that, call end_tournament()
        Params : None
        Return : None
        """
        current_round = self.chess_tournament.current_round.round_matches

        for match in current_round:
            self.results_menu(match)
        self.chess_tournament.end_round()
        self.save_tournament()

        # Checking if this is the last round of the tournament.
        if not self.chess_tournament.tournament_finish:
            self.show_rounds(True)
        else:
            self.end_tournament()

    def results_menu(self, players):
        """
        Aims : Select the winner of each matchs (pair of players), and send it
        to the match_results method of the Round Class.
        params :
        -players : pair of players instance sent by the enter_results method.
        Return : None
        """
        players_list = []
        for index, player in enumerate(players):
            player_name = (players[index].name + ' '
                           + players[index].family_name)
            players_list.append(player_name)

        players_list.append('Match nul')
        result_menu = SelectionMenu.get_selection(players_list,
                                                  'Centre échecs',
                                                  'Indiquez le vainqueur '
                                                  'ou le match nul')

        # This is to avoid an index error, since the result_menu variable is
        # the user selection, and the last choice of the menu is the exit of
        # the menu
        if result_menu < 3:
            self.chess_tournament.current_round.match_results(players,
                                                              result_menu)

    def end_tournament(self):
        """
        Aims : display the final results of the tournaments. (players sorted
        by their points)
        Params : None
        Return : None
        """
        self.save_tournament()
        players_list = sorted(self.chess_tournament.players,
                              key=attrgetter('points'),
                              reverse=True)
        players_rank = []

        for players in players_list:
            player_points = (players.family_name + ' ' + players.name + ' : '
                             + str(players.points))
            players_rank.append(player_points)

        end_menu = SelectionMenu(players_rank, 'Center échecs',
                                 'Fin de tournois',
                                 prologue_text='résultats finaux')
        end_menu.show()

    def dis_rank(self):
        """
        Aims : displaying player sorted by rank.
        params : None
        Return : None
        """
        players_list = sorted(self.chess_tournament.players,
                              key=attrgetter('rank'),
                              reverse=True)
        players_rank = []

        for player in players_list:
            player_ranking = (str(player.rank) + ' : ' + player.family_name
                              + ', ' + player.name)
            players_rank.append(player_ranking)

        rank_menu = SelectionMenu(players_rank, 'Center échecs', 'Classement')
        rank_menu.show()

    def mod_rank_menu(self):
        """
        Aims : Display menu to change a player's rank via the Joueur.new_rank()
        methode.
        Params : None
        Return : None
        """
        players_name = []

        for player in self.player_name_sort:
            name_player = (player.family_name + ', ' + player.name + ' : '
                           + str(player.rank))
            players_name.append(name_player)
        sel = SelectionMenu.get_selection(players_name, 'Centre échecs',
                                          'Modification du classement')

        # This is to avoid index error, since the last menu selection is the
        # exit one.
        if sel < len(players_name):
            user_mod = input('Quel est le nouveau classement de '
                             + self.player_name_sort[sel].name + ' '
                             + self.player_name_sort[sel].family_name + ' ?')
            new_rank = int(user_mod)
            self.player_name_sort[sel].new_rank(new_rank)
            self.save_tournament()
        else:
            pass

    def save_tournament(self):
        """
        Aims : saving the tournament, player and rounds in a JSon database
        params : None
        return : None
        """
        self.chess_tournament.save_tournament()

    def resume_t(self):
        """
        Aims : display a list of un-finish tournament to choose from. The
        selected tournament will be load from data base.
        params : None
        returns : None
        """
        tournament_list = []
        for files in glob('Tournois/Interrompus/*.json'):
            tournament_displayed = re.search('(?<=Interrompus/).*?(?=.json)',
                                             files).group()
            tournament_list.append(tournament_displayed)
        sel = SelectionMenu.get_selection(tournament_list, 'Centre échecs',
                                          "Reprise d'un tournois interrompu")

        # This is to avoid index error, since the last menu selection is the
        # exit one.
        if sel < len(tournament_list):
            self.chess_tournament = Tournois(
                file='Tournois/Interrompus/' + tournament_list[sel],
                resume=True)
            self.player_name_sort = sorted(self.chess_tournament.players,
                                           key=attrgetter('family_name'))
            self.tournament()
        else:
            pass

    def report_t(self):
        """
        Aims : generate a menu to choose a type of report
        params : None
        return : None
        """
        self.report = Report()

        # Arguments list to be sent to the sel_tournament methode, so it calls
        # the proper Report method
        args_list = [[True, False, False, False], [False, True, False, False],
                     [False, False, True, False], [False, False, False, True]]
        report_menu = ConsoleMenu('Centre échecs', 'menu de rapport')

        show_all_actors = FunctionItem('Voir tout les acteurs',
                                       self.report.all_players,
                                       menu=report_menu)

        show_all_tournament = FunctionItem('Voir tout les tournois términés',
                                           self.sel_tournament,
                                           args=args_list[3])

        show_all_t_players = FunctionItem(
            "Voir tout les joueurs d'un tournois",
            self.sel_tournament, args=args_list[0], menu=report_menu)

        show_t_rounds = FunctionItem('Voir les rounds d\'un tournois',
                                     self.sel_tournament, args=args_list[1])

        show_t_results = FunctionItem('Voir les resultats d\' un tournois',
                                      self.sel_tournament, args=args_list[2])

        report_menu.append_item(show_all_actors)
        report_menu.append_item(show_all_tournament)
        report_menu.append_item(show_all_t_players)
        report_menu.append_item(show_t_rounds)
        report_menu.append_item(show_t_results)
        report_menu.show()

    def sel_tournament(self, players=False, rounds=False, matchs=False,
                       tournaments=False):
        """
        Method that will display saved finish tournaments, the user selection
        will then called the proper Report method, depending on the argument
        passes by report_t method.

        If the user choose to see all saved tournaments, it will just displays
        them, without calling a Report object.
        Aims : display lists of finished tournament to choose from.
        Params :
        -players : boolean, if True, will display all players from all saved
        tournaments.
        -rounds : boolean, if true, will display a list of all finished
        tournaments, the user-selected one will call tournament_round method
        of Report class.
        -matchs : boolean, if true, will display a list of all finished
        tournaments, the user-selected one will call tournament_matchs method
        of Report class.
        -tournament : boolean, if true, will show all finished tournaments in
        data base.
        """
        tournament_list = []
        folder = 'Tournois/Terminés/'

        if glob(folder + '*.json'):
            for files in glob(folder + '*.json'):
                tournament_list.append(files[18:-5])

            if tournaments:
                menu = SelectionMenu(tournament_list, 'Centre échecs',
                                     'Liste de tournois terminés')
                menu.show()

            else:
                sel = SelectionMenu.get_selection(tournament_list,
                                                  'Centre échecs',
                                                  'Pour quel tournois '
                                                  'souhaitez vous générer un '
                                                  'rapport ?')

                if players:
                    self.report.tournament_players(tournament_list[sel])

                elif rounds:
                    self.report.tournament_rounds(tournament_list[sel])

                elif matchs:
                    self.report.tournament_matchs(tournament_list[sel])
        else:
            input('Aucuns tournois terminés enregistrés, Appuyez sur <Entrée>'
                  ' pour revenir au menu précédent.')


if __name__ == '__main__':
    main = Menus()
