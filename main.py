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
    sell_item,
    show_inventory,
    calculate_restock
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
    time_remaining,
    phase_elapsed,
    phase_start_from_elapsed
)

from car_dealership import (
    car_shop_inventory,
    car_sell_prices,
    buy_car,
    sell_car,
    show_garage
)

from night_store import get_customer_options
from bank import BankAccount
from arcade import arcades, arcade_income, buy_arcade, collect_arcade_income
from nightclub import nightclubs, nightclub_income, buy_nightclub, collect_nightclub_income

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 500
        self.dirty_money = 0
        self.reputation = 0
        self.inventory = {}
        self.owned_properties = []
        self.owned_nightclubs = []
        self.owned_arcades = []
        self.alive = True
        self.owned_cars = {}
        self.last_arcade_collection_day = 0
        self.last_club_collection_day = 0


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


def ask_number(prompt):

    while True:
        answer = input(prompt)

        try:
            number = int(answer)
        except ValueError:
            print("Please enter a whole number")
            continue

        if number <= 0:
            print("Please enter a number above 0")
        else:
            return number


def rank_rep(reputation, shop, customer_options):

    if reputation >= 5 and "protein" not in shop:
        shop["protein"] = 40
        customer_options.append("protein")
        print("NEW ITEM UNLOCKED: protein")

    if reputation >= 10 and "premium_coffee" not in shop:
        shop["premium_coffee"] = 75
        customer_options.append("premium_coffee")
        print("NEW ITEM UNLOCKED: premium coffee")


while player.alive:

    action = input(
        "Chose an action: View Status, Buy Stock, Serve Customer, "
        "Skip Customer, Buy property, View properties, View current customer, "
        "Upgrade property, Save game, Load game, Bank, View inventory, Restock, Buy arcade, "
        "Collect arcade income, Buy nightclub, collect club income, Buy car, Sell car, View garage, Quit ? "
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

            quantity = ask_number("How many do you want? ")

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
                customer_options
            )

            customer_queue = replace_customer(
                customer_queue,
                customer_options
            )

        else:
            print(f"Customer still wants: {current_order}")

    elif action == "skip customer":

        print(f"The customer who wanted {customer_queue[0]} walks out")

        if player.reputation > 0:
            player.reputation -= 1
            print(f"Reputation dropped to {player.reputation}")

        customer_queue = replace_customer(
            customer_queue,
            customer_options
        )

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
            bank.balance,
            player.owned_arcades,
            player.owned_nightclubs,
            player.owned_cars,
            player.dirty_money,
            day,
            time_of_day,
            phase_elapsed(phase_start_time),
            player.last_arcade_collection_day,
            player.last_club_collection_day
        )

    elif action == "load game":

        saved_data = load_game()

        if saved_data is not None:
            (
                player.money,
                player.reputation,
                player.inventory,
                player.owned_properties,
                property_levels,
                bank.balance,
                player.owned_arcades,
                player.owned_nightclubs,
                player.owned_cars,
                player.dirty_money,
                day,
                time_of_day,
                phase_elapsed_seconds,
                player.last_arcade_collection_day,
                player.last_club_collection_day
            ) = saved_data

            phase_start_time = phase_start_from_elapsed(phase_elapsed_seconds)

            rank_rep(
                player.reputation,
                shop,
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
                amount = ask_number("How much do you want to deposit? ")
                bank.deposit(player, amount)

            elif bank_action == "withdraw":
                amount = ask_number("How much do you want to withdraw ? ")
                bank.withdraw(player, amount)

            elif bank_action == "exit":
                break

            else:
                print("Incorrect input")
                

    elif action == "view inventory":
        show_inventory(player.inventory, sell_prices)

    elif action == "restock":

        item = input("What item do you want to restock? ").lower()

        if item not in shop:
            print("This item does not exist")

        else:
            target_stock = ask_number("What is your target stock? ")

            stock = player.inventory.get(item, 0)

            missing_stock = calculate_restock(
                player.inventory,
                item,
                target_stock
            )

            print("\n========== RESTOCK ==========")
            print(f"Product: {item}")
            print(f"Current stock: {stock}")
            print(f"Target stock: {target_stock}")
            print(f"Stock needed: {missing_stock}")

            if missing_stock == 0:
                print("You already have enough stock!")

            else:
                price = shop[item] * missing_stock

                print(f"Price per item: ${shop[item]}")
                print(f"Total cost: ${price}")
                print(f"Available money: ${player.money}")

                question = input(
                    "Would you like to purchase? (yes/no): "
                ).lower()

                if question == "yes" or question == "y":

                    player.money, player.inventory = buy_item(
                        player.money,
                        player.inventory,
                        item,
                        shop,
                        missing_stock
                    )

                else:
                    print("Restock cancelled")

            print("=============================")
    
    elif action == "buy arcade":
        player.money, player.owned_arcades = buy_arcade(
        player.money,
        player.owned_arcades,
        arcades
        )

    elif action == "collect arcade income":

        if day == player.last_arcade_collection_day:
            print("You've already collected income today")

        elif not player.owned_arcades:
            print("You don't own an arcade")

        else:    
            
            player.money = collect_arcade_income(
                player.money,
                player.owned_arcades,
                arcade_income
            )

            player.last_arcade_collection_day = day

    elif action == "buy nightclub":
        player.money, player.owned_nightclubs = buy_nightclub(
            player.money,
            player.owned_nightclubs,
            nightclubs
        )

    elif action == "collect club income":

        if day == player.last_club_collection_day:
            print("You've already collected income today")

        elif not player.owned_nightclubs:
            print("You don't own any nightclubs")

        else:
            player.money = collect_nightclub_income(
                player.owned_nightclubs,
                player.money,
                nightclub_income
            )

            player.last_club_collection_day = day

    elif action == "buy car":
        player.money, player.owned_cars = buy_car(
            car_shop_inventory,
            player.money,
            player.owned_cars
        )

    elif action == "sell car":
        player.money, player.owned_cars = sell_car(
            player.owned_cars,
            player.money,
            car_sell_prices
        )

    elif action == "view garage":
        show_garage(player.owned_cars)

    elif action == "quit":
        player.alive = False

    else:
        print("Invalid option")