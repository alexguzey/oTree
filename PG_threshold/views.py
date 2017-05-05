from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Contribution(Page):
    form_model = models.Player
    form_fields = ['contribution']
    def vars_for_template(self):
        return {
           'current_round': self.subsession.round_number
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        self.player.my_method()
        return {
            'my_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
            'me_in_all_rounds_1': self.group.get_player_by_id(1).my_payoff,
            'me_in_all_rounds_2': self.group.get_player_by_id(2).my_payoff,
            'me_in_all_rounds_3': self.group.get_player_by_id(3).my_payoff,
            'me_in_all_rounds_4': self.group.get_player_by_id(4).my_payoff,
            'me_in_all_rounds_5': self.group.get_player_by_id(5).my_payoff,
            'p1_contr': self.group.get_player_by_id(1).my_contribution,
            'p2_contr': self.group.get_player_by_id(2).my_contribution,
            'p3_contr': self.group.get_player_by_id(3).my_contribution,
            'p4_contr': self.group.get_player_by_id(4).my_contribution,
            'p5_contr': self.group.get_player_by_id(5).my_contribution,
            'current_round': self.subsession.round_number
        }

   # def vars2_for_template(self):
   # #    self.player.my_method()
   #     all_payoffs = []
   #
   #     for players_ind in self.player.get_others_in_group():
   #         all_payoffs.append({
   #             'others_payoff': players_ind.my_payoff
   #         })
   #     other_player_ids = [p.id_in_group for p in self.player.get_others_in_group()]
   #     #     my_payoff = sum([p.payoff for p in self.player.in_all_rounds()]),
   #     #     me_in_all_rounds = self.player.get_others_in_group(),
   #     return {
   #         'all_payoffs': all_payoffs,  # sum([p.payoff for p in self.player.in_all_rounds()]),
   #         'other_player_ids': other_player_ids  # self.player.get_others_in_group(),
   #     }

#
#
#class ChoiceOne(Page):
#    def is_displayed(self):
#        return self.player.id_in_group == 1

# def var1_for_template(self):
#        self.group.globcont
#        #return {
#        #    'global_contribution': sum([p.total_contribution for p in self.player.in_all_rounds()])
#        #}

page_sequence = [
    Contribution,
    ResultsWaitPage,
    Results
]
