from businesses.bank import BankAccount
from businesses.customers import create_customer_queue
from businesses.properties import property_levels
from core.player import Player
from core import time_system


class GameState:
    """Everything that changes while the game runs, kept in one place."""

    def __init__(self, player_name):
        self.player = Player(player_name)
        self.bank = BankAccount(player_name)
        self.property_levels = property_levels
        self.customer_options = ["coffee", "energy", "snack"]
        self.customer_queue = create_customer_queue(self.customer_options)
        self.day = time_system.day
        self.time_of_day = time_system.time_of_day
        self.phase_start_time = time_system.phase_start_time
