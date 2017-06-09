# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.Introduction)
        yield (views.PreOverthrow, {'approval': 1, 'vote_to_overthrow': 3})
        yield (views.PreOverthrow, {'approval': 1, 'vote_to_overthrow': 3})
        yield (views.PreOverthrow, {'approval': 0, 'vote_to_overthrow': 3})
        yield (views.PreOverthrow, {'approval': 1, 'vote_to_overthrow': 3})
        yield (views.PreOverthrow, {'approval': 1, 'vote_to_overthrow': 3})
        yield (views.FinalVote, {'approval_final': 1, 'vote_to_overthrow': 3})
        yield (views.FinalResults)
