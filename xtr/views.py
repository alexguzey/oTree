# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 600
    def is_displayed(self):
        return  self.subsession.round_number == 2

class Pick_box(Page):

    form_model = models.Player
    form_fields = ['points']

    def vars_for_template(self):
        return {
            'picked_box': 0
        }

class Guess(Page):

    form_model = models.Player
    form_fields = ['guess']

    def vars_for_template(self):
        return {
            'picked_box': self.player.points
        }

class Final(Page):
    pass

page_sequence =[
    Introduction,
    Pick_box,
    Guess,
    Final
]
