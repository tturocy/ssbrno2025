import string

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

    def setup_round(self):
        self.payment_per_correct = Currency(0.10)
        self.lookup_table = string.ascii_uppercase
        self.word = "ABABA"

    @property
    def lookup_dict(self):
        lookup = {}
        for letter in string.ascii_uppercase:
            lookup[letter] = self.lookup_table.index(letter)+1
        return lookup


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField()

    def check_response(self):
        self.is_correct = (
            self.response_1 == self.subsession.lookup_dict[self.subsession.word[0]] and
            self.response_2 == self.subsession.lookup_dict[self.subsession.word[1]] and
            self.response_3 == self.subsession.lookup_dict[self.subsession.word[2]] and
            self.response_4 == self.subsession.lookup_dict[self.subsession.word[3]] and
            self.response_5 == self.subsession.lookup_dict[self.subsession.word[4]]
        )
        if self.is_correct:
            self.payoff = self.subsession.payment_per_correct


def creating_session(subsession):
    subsession.setup_round()


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
        "response_3",
        "response_4",
        "response_5",
    ]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.check_response()


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Intro,
    Decision,
    Results,
]
