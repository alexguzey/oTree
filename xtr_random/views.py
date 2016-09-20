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
    form_fields = ['points','x_coordinate_form_pick','y_coordinate_form_pick', 'box_1_offset_left_form','box_1_offset_top_form',
                   'box_2_offset_left_form', 'box_2_offset_top_form', 'box_3_offset_left_form', 'box_3_offset_top_form'
                   ]

    def vars_for_template(self):
        return {
            'picked_box': 0
        }

class Guess(Page):

    form_model = models.Player
    form_fields = ['guess','x_coordinate_form_guess','y_coordinate_form_guess']

    def vars_for_template(self):
        return {
            'picked_box': self.player.points,
            'box_1_offset_left': self.player.box_1_offset_left_form,
            'box_1_offset_top': self.player.box_1_offset_top_form,
            'box_2_offset_left': self.player.box_2_offset_left_form,
            'box_2_offset_top': self.player.box_2_offset_top_form,
            'box_3_offset_left': self.player.box_3_offset_left_form,
            'box_3_offset_top': self.player.box_3_offset_top_form
        }

class Result(Page):

    def vars_for_template(self):
        return {
            'guess': self.player.guess,
            'picked_box': self.player.points,
            'pick_x_coordinate': self.player.x_coordinate_form_pick,
            'pick_y_coordinate': self.player.y_coordinate_form_pick,
            'guess_x_coordinate': self.player.x_coordinate_form_guess,
            'guess_y_coordinate': self.player.y_coordinate_form_guess,
            'box_1_offset_left': self.player.box_1_offset_left_form,
            'box_1_offset_top': self.player.box_1_offset_top_form,
            'box_2_offset_left': self.player.box_2_offset_left_form,
            'box_2_offset_top': self.player.box_2_offset_top_form,
            'box_3_offset_left': self.player.box_3_offset_left_form,
            'box_3_offset_top': self.player.box_3_offset_top_form

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
