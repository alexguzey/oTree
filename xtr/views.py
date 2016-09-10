# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 600
    def is_displayed(self):
        return  self.subsession.round_number == 0

class Pick_box(Page):

    form_model = models.Player
    form_fields = ['points','x_coordinate_form_pick','y_coordinate_form_pick']

    def vars_for_template(self):
        return {
            'picked_box': 0
        }

class Guess(Page):

    form_model = models.Player
    form_fields = ['guess','x_coordinate_form_guess','y_coordinate_form_guess']

    def vars_for_template(self):
        return {
            'picked_box': self.player.points
        }

class Result(Page):

    def vars_for_template(self):
        return {
            'guess': self.player.guess,
            'round_number': self.subsession.round_number,
            'picked_box': self.player.points,
            'pick_x_coordinate_1': self.player.in_round(1).x_coordinate_form_pick,
            'pick_x_coordinate_2': self.player.in_round(2).x_coordinate_form_pick,
            'pick_y_coordinate_1': self.player.in_round(1).y_coordinate_form_pick,
            'pick_y_coordinate_2': self.player.in_round(2).y_coordinate_form_pick,
            'guess_x_coordinate_1': self.player.in_round(1).x_coordinate_form_guess,
            'guess_x_coordinate_2': self.player.in_round(2).x_coordinate_form_guess,
            'guess_y_coordinate_1': self.player.in_round(1).y_coordinate_form_guess,
            'guess_y_coordinate_2': self.player.in_round(2).y_coordinate_form_guess
        }

class Final(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

page_sequence =[
    Introduction,
    Pick_box,
    Guess,
    Result,
    Final
]
