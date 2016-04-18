# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Alex'

doc = """
reforming game
"""

class Constants(BaseConstants):
    name_in_url = 'reform'
    players_per_group = 2
    num_rounds = 3
    base_sales = 16
    base_consumption = 4
    reform_penalty = 4
    reform_benefits = 0.5
    approval_cost = 0.3
    solidarity_benefits = {0: 0.0, 1: 0.2, 2: 0.5, 3: 1, 4: 1.6, 5: 2.3}
    points_to_overthrow = 6
    max_overthrow_vote_for_player = 5
    max_reforms = 5


class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['reforms'] = 0
            self.session.vars['overthrow'] = 0

class Group(BaseGroup):
    # before any upheavals number of reforms is equal to round number
    def num_reforms(self):
        return self.subsession.round_number

    reformed_id = 0
    # pick one player to be reformed
    def reformed_player(self):
        while True:
            self.reformed_id = random.randint(1,Constants.players_per_group)
            if self.num_reforms() - self.get_player_by_id(self.reformed_id).participant.vars['reforms']*Constants.players_per_group > 0:
                break

    # increase number of reforms by 1 for reformed player
    def reform_a_player(self):
        for p in self.get_players():
            if p.id_in_group == self.reformed_id:
                p.participant.vars['reforms'] += 1
            else:
                pass


    total_approvals = 0
    def approvals(self):
        return sum(p.approval for p in self.get_players())

    # sums up players votes for overthrow and switches regime, if necessary
    def total_votes_for_overthrow(self):
        if sum(p.vote_to_overthrow for p in self.get_players()) >= Constants.points_to_overthrow and self.session.vars['overthrow'] == 0:
            self.session.vars['overthrow'] = 1
        return sum(p.vote_to_overthrow for p in self.get_players())

    def payoffs(self):
        if self.session.vars['overthrow'] == 0:
            for p in self.get_players():
                p.payoff = \
                Constants.base_sales \
                - ( p.participant.vars['reforms'] * Constants.reform_penalty ) \
                + Constants.base_consumption \
                + (( self.num_reforms() - p.participant.vars['reforms'] ) * Constants.reform_benefits) \
                - ( p.approval * Constants.approval_cost ) \
                + Constants.solidarity_benefits[self.approvals()] \
                - p.vote_to_overthrow
        else:
            for p in self.get_players():
                p.payoff = \
                Constants.base_sales

    reforms_votes_group = []
    # aggregate proposed number of reforms (after overthrow mechanic)
    def reform(self):
        for p in self.get_players():
            self.reforms_votes_group.append(p.reforms_votes)


class Player(BasePlayer):

    approval_choices = ((1, "Approve"),(0, "Disapprove"))
    approval = models.FloatField(widget=widgets.RadioSelect, choices=approval_choices)

    vote_to_overthrow = models.FloatField(widget=widgets.SliderInput(attrs={'step': '1'}), min=0, max=Constants.max_overthrow_vote_for_player, default=3)

    reforms_votes = models.FloatField(widget=widgets.SliderInput(attrs={'step': '1'}), min=0, max=Constants.max_reforms, default=3)