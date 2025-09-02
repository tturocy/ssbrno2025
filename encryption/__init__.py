from otree.api import *


doc = """
Encryption task
"""


class C(BaseConstants):
    NAME_IN_URL = 'encryption'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3


class Subsession(BaseSubsession):
    payment_per_correct = models.CurrencyField()
    word = models.StringField()
    lookup_table = models.StringField()
    time_for_task = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    form_model = "player"
    form_fields = [
        "response_1",
        "response_2",
    ]


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Intro,
    Decision,
    Results,
]
