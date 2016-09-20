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
Point guessing game
"""

class Constants(BaseConstants):
    name_in_url = 'xtr_random'
    players_per_group = None
    num_rounds = 5

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    points = models.TextField()
    x_coordinate_form_pick = models.IntegerField()
    y_coordinate_form_pick = models.IntegerField()
    x_coordinate_form_guess = models.IntegerField()
    y_coordinate_form_guess = models.IntegerField()
    box_1_offset_left_form = models.IntegerField()
    box_1_offset_top_form = models.IntegerField()
    box_2_offset_left_form = models.IntegerField()
    box_2_offset_top_form = models.IntegerField()
    box_3_offset_left_form = models.IntegerField()
    box_3_offset_top_form = models.IntegerField()
    guess = models.TextField()