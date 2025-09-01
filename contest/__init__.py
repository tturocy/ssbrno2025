from otree.api import *


doc = """
General-purpose contest experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    ENDOWMENT = 10
    COST_PER_TICKET = 0.5
    PRIZE = 8


class Subsession(BaseSubsession):
    csf = models.StringField()
    is_paid = models.BooleanField()

    def setup_round(self):
        self.csf = "share"
        self.is_paid = True
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup):
    cost_per_ticket = models.CurrencyField()
    prize = models.CurrencyField()

    def setup_round(self):
        self.cost_per_ticket = C.COST_PER_TICKET
        self.prize = C.PRIZE
        for player in self.get_players():
            player.setup_round()


class Player(BasePlayer):
    endowment = models.CurrencyField()
    tickets_purchased = models.IntegerField()
    prize_won = models.FloatField()
    earnings = models.CurrencyField()

    def setup_round(self):
        self.endowment = C.ENDOWMENT

    @property
    def coplayer(self):
        return self.group.get_player_by_id(3 - self.id_in_group)

    @property
    def tickets_purchased_by_others(self):
        return self.coplayer.tickets_purchased


# PAGES
class StartRound(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup_round()


class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    form_model = "player"
    form_fields = ["tickets_purchased"]


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
