import random
import sys
from save_system import save_game, load_game
from properties import (
    property_name,
    property_levels,
    buy_property,
    upgrade_property,
    property_bonus
)
from shop import (
    shop,
    sell_prices,
    add_item,
    remove_item,
    buy_item,
    sell_item
)
from customers import (
    complete_order,
    create_customer_queue,
    replace_customer
)
from time_system import (
    update_time_of_day,
    time_of_day,
    phase_start_time,
    day,
    time_remaining
)
from nigh_store import get_customer_options
from bank import BankAccount


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 500
        self.reputation = 0
        self.inventory = {}
        self.alive = True
        self.owned_properties = []


name = input("What is your name? ")

player = Player(name)

bank = BankAccount(player.name)


customer_options = ["coffee", "energy", "snack"]
customer_queue = create_customer_queue(customer_options)


print("PLAYER STATUS")
print(f"Money: {player.money}")
print(f"Reputation: {player.reputation}")
print(f"Inventory: {player.inventory}")
print(f"Owned Properties: {player.owned_properties}")


def rank_rep(reputation, shop, sell_prices, customer_options):

    if reputation >= 5 and "protein" not in shop:
        shop["protein"] = 40
        sell_prices["protein"] = 60
        customer_options.append("protein")
        print("NEW ITEM UNLOCKED: protein")

    if reputation >= 10 and "premium_coffee" not in shop:
        shop["premium_coffee"] = 75
        sell_prices["premium_coffee"] = 110
        customer_options.append("premium_coffee")
        print("NEW ITEM UNLOCKED: premium coffee")


while player.alive:

    action = input(
        "Chose an action: View Status, Buy Stock, Serve Customer, "
        "Buy property, View properties, View current customer, "
        "Upgrade property, Save game, Load game, Bank, Quit ? "
    ).lower()

    time_of_day, phase_start_time, day = update_time_of_day(
        time_of_day,
        phase_start_time,
        day
    )

    customer_options = get_customer_options(
        time_of_day,
        player.reputation
    )

    if action == "view status":
        print(player.money)
        print(player.reputation)
        print(player.inventory)
        print(f"Day: {day}")
        print(f"Time of day: {time_of_day}")

        minutes_left = time_remaining(phase_start_time)
        print(f"Time remaining: {int(minutes_left)} minutes")

    elif action == "buy stock":

        while True:
            print(f"Current inventory: {player.inventory}")

            item = input("What do you want to buy? ").lower()

            quantity = int(input("How many do you want? "))

            player.money, player.inventory = buy_item(
                player.money,
                player.inventory,
                item,
                shop,
                quantity
            )

            question = input("Do you want anything else ? ").lower()

            if question == "yes" or question == "y":
                print("No problem")
            else:
                break

    elif action == "serve customer":

        current_order = customer_queue[0]

        print("Serving the customer now...")

        (
            player.money,
            player.inventory,
            player.reputation,
            order_completed
        ) = complete_order(
            player.money,
            player.inventory,
            player.reputation,
            current_order,
            sell_prices
        )

        if order_completed == True:

            for building in player.owned_properties:

                bonus = property_bonus(
                    building,
                    player.owned_properties,
                    property_levels
                )

                player.money += bonus

            rank_rep(
                player.reputation,
                shop,
                sell_prices,
                customer_options
            )

            customer_queue = replace_customer(
                customer_queue,
                customer_options
            )

        else:
            print(f"Customer still wants: {current_order}")

    elif action == "view current customer":
        print(f"Customer queue: {customer_queue}")

    elif action == "buy property":

        player.money, player.owned_properties = buy_property(
            player.money,
            property_name,
            player.owned_properties
        )

    elif action == "view properties":

        for building in player.owned_properties:
            print(
                f"{building} - Level: "
                f"{property_levels[building]}"
            )

    elif action == "upgrade property":

        for building in player.owned_properties:
            print(building)

        building = input(
            "Which property do you want to upgrade? "
        ).lower()

        player.money, building, property_levels = upgrade_property(
            building,
            player.owned_properties,
            property_levels,
            player.money
        )

    elif action == "save game":

        save_game(
            player.money,
            player.reputation,
            player.inventory,
            player.owned_properties,
            property_levels,
            bank.balance
        )

    elif action == "load game":

        (
            player.money,
            player.reputation,
            player.inventory,
            player.owned_properties,
            property_levels,
            bank.balance
        ) = load_game()

        rank_rep(
            player.reputation,
            shop,
            sell_prices,
            customer_options
        )

    elif action == "bank":
        while True: 
            bank_action = input(
                "What do you want ? View balance, Deposit, Withdraw, Exit "
            ).lower()

            if bank_action == "view balance":
                print(f"Bank balance: ${bank.balance}")

            elif bank_action == "deposit":
                amount = int(input("How much do you want to deposit? "))
                bank.deposit(player, amount)

            elif bank_action == "withdraw":
                amount = int(input("How much do you want to withdraw ? "))
                bank.withdraw(player, amount)

            elif bank_action == "exit":
                break

            else:
                print("Incorrect input")
                

            

    elif action == "quit":
        player.alive = False

    else:
        print("Invalid option")