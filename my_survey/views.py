from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = models.Player
    form_fields = ['age',
                   'gender',
                   'height']


class City(Page):
    form_model = models.Player
    form_fields = ['city',
                   'yearsinmsc', 'mscyourcity', 'achieve', 'deput']


class Yourself(Page):
    form_model = models.Player
    form_fields = ['univ',
                   'study',
                   'riskat',
                   'income',
                   'satis',
                   'trust']

class polit(Page):
    form_model = models.Player
    form_fields = ['freedom',
                       'politics',
                       'leftright',
                       'ownership',
                       'responsibility',
                       'democracy', 'democracy_today']

    def before_next_page(self):
        self.player.set_payoff()


page_sequence = [
    MyPage, City, Yourself, polit
   ]
