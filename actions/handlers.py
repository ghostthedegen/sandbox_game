from businesses.arcade import (
    arcades,
    arcade_income,
    buy_arcade,
    collect_arcade_income
)
from businesses.car_dealership import (
    car_shop_inventory,
    car_sell_prices,
    buy_car,
    sell_car,
    show_garage
)
from businesses.customers import complete_order, replace_customer
from businesses.nightclub import (
    nightclubs,
    nightclub_income,
    buy_nightclub,
    collect_nightclub_income
)
from businesses.properties import (
    property_name,
    buy_property,
    upgrade_property,
    property_bonus
)
from businesses.shop import (
    shop,
    sell_prices,
    buy_item,
    show_inventory,
    calculate_restock
)
from core.save_system import save_game, load_game
from core.time_system import time_remaining


MENU = (
    "Chose an action: View Status, Buy Stock, Serve Customer, "
    "Skip Customer, Buy property, View properties, View current customer, "
    "Upgrade property, Save game, Load game, Bank, View inventory, Restock, Buy arcade, "
    "Collect arcade income, Buy nightclub, collect club income, Buy car, Sell car, View garage, Quit ? "
)


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


# ---------- Status ----------

def handle_view_status(game):
    player = game.player

    print(player.money)
    print(player.reputation)
    print(player.inventory)
    print(f"Day: {game.day}")
    print(f"Time of day: {game.time_of_day}")

    minutes_left = time_remaining(game.phase_start_time)
    print(f"Time remaining: {int(minutes_left)} minutes")


def handle_quit(game):
    game.player.alive = False


# ---------- Shop stock ----------

def handle_buy_stock(game):
    player = game.player

    while True:
        print(f"Current inventory: {player.inventory}")

        item = input("What do you want to buy? ").strip().lower()

        quantity = ask_number("How many do you want? ")

        player.money, player.inventory = buy_item(
            player.money,
            player.inventory,
            item,
            shop,
            quantity
        )

        question = input("Do you want anything else ? ").strip().lower()

        if question == "yes" or question == "y":
            print("No problem")
        else:
            break


def handle_view_inventory(game):
    show_inventory(game.player.inventory, sell_prices)


def handle_restock(game):
    player = game.player

    item = input("What item do you want to restock? ").strip().lower()

    if item not in shop:
        print("This item does not exist")
        return

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
        ).strip().lower()

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


# ---------- Customers ----------

def handle_serve_customer(game):
    player = game.player

    current_order = game.customer_queue[0]

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

    if order_completed:

        for building in player.owned_properties:

            bonus = property_bonus(
                building,
                player.owned_properties,
                game.property_levels
            )

            player.money += bonus

        rank_rep(
            player.reputation,
            shop,
            game.customer_options
        )

        game.customer_queue = replace_customer(
            game.customer_queue,
            game.customer_options
        )

    else:
        print(f"Customer still wants: {current_order}")


def handle_skip_customer(game):
    player = game.player

    print(f"The customer who wanted {game.customer_queue[0]} walks out")

    if player.reputation > 0:
        player.reputation -= 1
        print(f"Reputation dropped to {player.reputation}")

    game.customer_queue = replace_customer(
        game.customer_queue,
        game.customer_options
    )


def handle_view_customers(game):
    print(f"Customer queue: {game.customer_queue}")


# ---------- Properties ----------

def handle_buy_property(game):
    player = game.player

    player.money, player.owned_properties = buy_property(
        player.money,
        property_name,
        player.owned_properties
    )


def handle_view_properties(game):

    for building in game.player.owned_properties:
        print(
            f"{building} - Level: "
            f"{game.property_levels[building]}"
        )


def handle_upgrade_property(game):
    player = game.player

    for building in player.owned_properties:
        print(building)

    building = input(
        "Which property do you want to upgrade? "
    ).strip().lower()

    player.money, building, game.property_levels = upgrade_property(
        building,
        player.owned_properties,
        game.property_levels,
        player.money
    )


# ---------- Save and load ----------

def handle_save_game(game):
    save_game(game)


def handle_load_game(game):

    if load_game(game):
        rank_rep(
            game.player.reputation,
            shop,
            game.customer_options
        )


# ---------- Bank ----------

def handle_bank(game):
    player = game.player
    bank = game.bank

    while True:
        bank_action = input(
            "What do you want ? View balance, Deposit, Withdraw, Exit "
        ).strip().lower()

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


# ---------- Arcades ----------

def handle_buy_arcade(game):
    player = game.player

    player.money, player.owned_arcades = buy_arcade(
        player.money,
        player.owned_arcades,
        arcades
    )


def handle_collect_arcade_income(game):
    player = game.player

    if game.day == player.last_arcade_collection_day:
        print("You've already collected income today")

    elif not player.owned_arcades:
        print("You don't own an arcade")

    else:
        player.money = collect_arcade_income(
            player.money,
            player.owned_arcades,
            arcade_income
        )

        player.last_arcade_collection_day = game.day


# ---------- Nightclubs ----------

def handle_buy_nightclub(game):
    player = game.player

    player.money, player.owned_nightclubs = buy_nightclub(
        player.money,
        player.owned_nightclubs,
        nightclubs
    )


def handle_collect_club_income(game):
    player = game.player

    if game.day == player.last_club_collection_day:
        print("You've already collected income today")

    elif not player.owned_nightclubs:
        print("You don't own any nightclubs")

    else:
        player.money = collect_nightclub_income(
            player.owned_nightclubs,
            player.money,
            nightclub_income
        )

        player.last_club_collection_day = game.day


# ---------- Cars ----------

def handle_buy_car(game):
    player = game.player

    player.money, player.owned_cars = buy_car(
        car_shop_inventory,
        player.money,
        player.owned_cars
    )


def handle_sell_car(game):
    player = game.player

    player.money, player.owned_cars = sell_car(
        player.owned_cars,
        player.money,
        car_sell_prices
    )


def handle_view_garage(game):
    show_garage(game.player.owned_cars)


# What the player types -> the function that handles it
ACTIONS = {
    "view status": handle_view_status,
    "buy stock": handle_buy_stock,
    "serve customer": handle_serve_customer,
    "skip customer": handle_skip_customer,
    "view current customer": handle_view_customers,
    "buy property": handle_buy_property,
    "view properties": handle_view_properties,
    "upgrade property": handle_upgrade_property,
    "save game": handle_save_game,
    "load game": handle_load_game,
    "bank": handle_bank,
    "view inventory": handle_view_inventory,
    "restock": handle_restock,
    "buy arcade": handle_buy_arcade,
    "collect arcade income": handle_collect_arcade_income,
    "buy nightclub": handle_buy_nightclub,
    "collect club income": handle_collect_club_income,
    "buy car": handle_buy_car,
    "sell car": handle_sell_car,
    "view garage": handle_view_garage,
    "quit": handle_quit,
}
