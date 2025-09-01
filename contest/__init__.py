from otree.api import *


doc = """
General-purpose contest experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class StartRound(WaitPage):
    pass


class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


class EndBlock(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    StartRound,
    Intro,
    Decision,
    ResultsWaitPage,
    Results,
    EndBlock,
]
