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
        self.csf = "allpay"
        self.is_paid = self.round_number % 2 == 1
        for group in self.get_groups():
            group.setup_round()

    def determine_outcome(self):
        for group in self.get_groups():
            group.determine_outcome()


class Group(BaseGroup):
    cost_per_ticket = models.CurrencyField()
    prize = models.CurrencyField()

    @property
    def total_tickets_purchased(self):
        return sum(player.tickets_purchased for player in self.get_players())

    def setup_round(self):
        self.cost_per_ticket = C.COST_PER_TICKET
        self.prize = C.PRIZE
        for player in self.get_players():
            player.setup_round()

    def determine_outcome_allpay(self):
        max_tickets = max(player.tickets_purchased for player in self.get_players())
        num_tied = len([player for player in self.get_players()
                        if player.tickets_purchased == max_tickets])
        for player in self.get_players():
            if player.tickets_purchased == max_tickets:
                player.prize_won = 1 / num_tied
            else:
                player.prize_won = 0

    def determine_outcome_share(self):
        total = self.total_tickets_purchased
        for player in self.get_players():
            try:
                player.prize_won = player.tickets_purchased / total
            except ZeroDivisionError:
                player.prize_won = 1 / len(self.get_players())

    def determine_outcome(self):
        if self.subsession.csf == "share":
            self.determine_outcome_share()
        elif self.subsession.csf == "allpay":
            self.determine_outcome_allpay()

        for player in self.get_players():
            player.earnings = (
                    player.endowment -
                    player.tickets_purchased * self.cost_per_ticket +
                    self.prize * player.prize_won
            )
            if player.subsession.is_paid:
                player.payoff = player.earnings


class Player(BasePlayer):
    endowment = models.CurrencyField()
    tickets_purchased = models.IntegerField()
    prize_won = models.FloatField()
    earnings = models.CurrencyField()

    def setup_round(self):
        self.endowment = C.ENDOWMENT

    @property
    def max_tickets_affordable(self):
        return int(self.endowment / self.group.cost_per_ticket)

    @property
    def coplayer(self):
        return self.group.get_player_by_id(3 - self.id_in_group)

    @property
    def tickets_purchased_by_others(self):
        return self.group.total_tickets_purchased - self.tickets_purchased


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

    @staticmethod
    def error_message(player, values):
        if values["tickets_purchased"] < 0:
            return "You cannot buy a negative number of tickets."
        elif values["tickets_purchased"] > player.max_tickets_affordable:
            return f"You can only afford to buy {player.max_tickets_affordable} tickets."
        return None


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.determine_outcome()


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
