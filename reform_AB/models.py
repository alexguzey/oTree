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
    name_in_url = 'reform_AB'
    players_per_group = 5
    num_rounds = 5
    base_sales = 10 #16
    base_consumption = 0 # 4
    reform_penalty = 2.5 #4
    reform_benefits = 1 # 0.5
    approval_cost = 0 # 0.3
    solidarity_benefits = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # {0: 0.0, 1: 0.2, 2: 0.5, 3: 1, 4: 1.6, 5: 2.3}
    points_to_overthrow = 300 # 6
    max_overthrow_vote_for_player = 5 # 5
    max_reforms = 5
    losses_from_overthrow = 0 # 10
    losses_from_chaos = 0 # 5
    cost_reforms_reversal = 2.5
    votes_needed_to_pass_reform = 3
    payoff_reforms_reversal = base_sales * num_rounds - cost_reforms_reversal


class Subsession(BaseSubsession):
    # need to introduce reforms participant var in order for them to carry over to next rounds. The same thing with overthrow switch.
    # regarding reformed_this_round -- this is ugly, but I couldn't come up with a way to create indicator of whether a player was reformed this round without p.participant.vars
    def before_session_starts(self):
#        random.shuffle()
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['reforms'] = 0
                p.participant.vars['reformed_this_round'] = 0
                p.participant.vars['reformed_previous_round'] = 0
                p.participant.vars['called_to_be_reformed'] = 0
            self.session.vars['overthrow'] = 0 # if no reform, 1 if took place, 2 if final reform reversal
            self.session.vars['overthrow_round'] = 0
            self.session.vars['total_approvals'] = 0
            self.session.vars['num_approved_reforms'] = 0


class Group(BaseGroup):
    # before the overthrow, number of reforms is equal to round number
    # refapproved=models.IntegerField()
    # refcalled=models.IntegerField()
    # refpastcalled=models.IntegerField()

    def current_round(self):
        return self.subsession.round_number

    reformed_id = 0
    # pick one player to be reformed
    def reformed_player(self):
        print("get_player_by_id, before while", self.reformed_id)
        while True:
            self.reformed_id = random.randint(1,Constants.players_per_group)
            if self.current_round()  \
                    - self.get_player_by_id(self.reformed_id).participant.vars['called_to_be_reformed']*Constants.players_per_group > 0:
                # break runs if if is satisfied i.e. we picked the "right" player to reform
                self.get_player_by_id(self.reformed_id).participant.vars['called_to_be_reformed'] = 1
                break

        for p in self.get_players():
            if p.id_in_group == self.reformed_id:
                p.participant.vars['reformed_this_round'] = 1
            # remember that if "if" was satisfied, all next conditions are ignored
            elif p.participant.vars['reformed_this_round'] == 1:
                p.participant.vars['reformed_previous_round'] = 1
                p.participant.vars['reformed_this_round'] = 0
            else:
                p.participant.vars['reformed_this_round'] = 0
                p.participant.vars['reformed_previous_round'] = 0

    group_approved_reforms = models.IntegerField(initial=0)
    current_round_reform_approved = False
    def approvals(self):

        if sum(p.approval for p in self.get_players()) >= Constants.votes_needed_to_pass_reform:
            self.current_round_reform_approved = True
            if self.current_round() == 1:
                self.group_approved_reforms = 1
            else:
                self.group_approved_reforms = self.in_round(self.current_round()-1).group_approved_reforms + 1
        else:
            self.group_approved_reforms = self.in_round(self.current_round() - 1).group_approved_reforms

        for p in self.get_players():
            if p.participant.vars['reformed_this_round'] == 1 and self.current_round_reform_approved:
                p.participant.vars['reforms'] += 1

    def approvals_previous_round(self):
        return int(sum(p.in_previous_rounds()[-1].approval for p in self.get_players()))

    # sums up players votes for overthrow and switches regime, if necessary
    def total_votes_for_overthrow(self):
        if sum(p.vote_to_overthrow for p in self.get_players()) >= Constants.points_to_overthrow and self.session.vars['overthrow'] == 0:
            self.session.vars['overthrow'] = 1 #never takes place under current settings
            self.session.vars['overthrow_round'] = self.subsession.round_number
            # chaos loses or something
            for p in self.get_players():
                p.payoff -= Constants.losses_from_overthrow

        return sum(p.vote_to_overthrow for p in self.get_players())

    def final_decision(self):
        if sum(p.approval_final for p in self.get_players()) < 3:
            self.session.vars['overthrow'] = 2 #meaning reversal of all reform decisions

    reforms_votes_group = []
    # aggregate proposed number of reforms (after overthrow mechanic)
    def reform(self):
        for p in self.get_players():
            self.reforms_votes_group.append(p.reforms_votes)

    def payoffs(self):
        for p in self.get_players():
            p.payoff = \
                Constants.base_sales \
                - ( p.participant.vars['reforms'] * Constants.reform_penalty ) \
                + (( self.group_approved_reforms - p.participant.vars['reforms'] ) * Constants.reform_benefits)

class Player(BasePlayer):
    # form showing whether a player approves government's reforms
    approval_choices = ((1, "Одобряю"),(0, "Не одобряю"))
    approval = models.FloatField(widget=widgets.RadioSelect, choices=approval_choices)
    approval_final = models.FloatField(widget=widgets.RadioSelect, choices=approval_choices)

    # form showing how much a player is spending on trying to overthrow the system
    vote_to_overthrow = models.FloatField(widget=widgets.SliderInput(attrs={'step': '1'}), min=0, max=Constants.max_overthrow_vote_for_player, default=3)

    # form showing how much reforms a player desires after the overthrow
    reforms_votes = models.FloatField(widget=widgets.SliderInput(attrs={'step': '1'}), min=0, max=Constants.max_reforms, default=3)