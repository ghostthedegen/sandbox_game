import json
import math
from pathlib import Path

from businesses.arcade import arcades
from businesses.nightclub import nightclubs
from businesses.properties import property_name, MAX_LEVEL
from core.time_system import phase_elapsed, phase_start_from_elapsed

# Always next to main.py, whichever folder the game is started from
SAVE_FILE = Path(__file__).resolve().parent.parent / "save_data.json"


def is_amount(value):
    """True for a normal number that is 0 or more."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False

    # Checked first because math.isfinite can't handle very large whole numbers
    if isinstance(value, int):
        return value >= 0

    return math.isfinite(value) and value >= 0


def is_whole_number(value, minimum):

    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= minimum
    )


def is_stock(value):
    """True for a {name: quantity} dictionary, such as the inventory."""

    return isinstance(value, dict) and all(
        is_whole_number(quantity, 1) for quantity in value.values()
    )


def is_owned_list(value, known_names):
    """True for a list that only contains names the game knows about."""

    return isinstance(value, list) and all(
        isinstance(name, str) and name in known_names for name in value
    )


def has_valid_levels(levels):
    """True if every property has a level the game can use."""

    return isinstance(levels, dict) and all(
        building in levels
        and is_whole_number(levels[building], 1)
        and levels[building] <= MAX_LEVEL
        for building in property_name
    )


def is_valid_save(data):
    """True if the save has the right contents, so loading it can't crash later."""

    return (
        is_amount(data["money"])
        and is_amount(data["bank_balance"])
        and is_amount(data["dirty_money"])
        and is_amount(data["phase_elapsed_seconds"])
        and is_whole_number(data["reputation"], 0)
        and is_whole_number(data["day"], 1)
        and is_whole_number(data["last_arcade_collection_day"], 0)
        and is_whole_number(data["last_club_collection_day"], 0)
        and data["time_of_day"] in ("day", "night")
        and is_stock(data["inventory"])
        and is_stock(data["owned_cars"])
        and is_owned_list(data["owned_properties"], property_name)
        and is_owned_list(data["owned_arcades"], arcades)
        and is_owned_list(data["owned_nightclubs"], nightclubs)
        and has_valid_levels(data["property_levels"])
    )


def save_game(game):
    player = game.player

    game_data = {
        "money": player.money,
        "reputation": player.reputation,
        "inventory": player.inventory,
        "owned_properties": player.owned_properties,
        "property_levels": game.property_levels,
        "bank_balance": game.bank.balance,
        "owned_arcades": player.owned_arcades,
        "owned_nightclubs": player.owned_nightclubs,
        "owned_cars": player.owned_cars,
        "dirty_money": player.dirty_money,
        "day": game.day,
        "time_of_day": game.time_of_day,
        "phase_elapsed_seconds": phase_elapsed(game.phase_start_time),
        "last_arcade_collection_day": player.last_arcade_collection_day,
        "last_club_collection_day": player.last_club_collection_day
    }

    with open(SAVE_FILE, "w") as file:
        json.dump(game_data, file, indent=4)

    print("Game saved")


def load_game(game):
    """Fill the game from the save file. Returns True if a save was loaded."""

    try:
        with open(SAVE_FILE, "r") as file:
            saved_data = json.load(file)

    except FileNotFoundError:
        print("No save file found. Current progress preserved.")
        return False

    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Save file is corrupted. Current progress preserved.")
        return False

    if not isinstance(saved_data, dict):
        print("Save file is corrupted. Current progress preserved.")
        return False

    # Defaults fill the gaps so older save files without a field still load
    data = {
        "money": 500,
        "reputation": 0,
        "inventory": {},
        "owned_properties": [],
        "property_levels": {"small_shop": 1},
        "bank_balance": 0,
        "owned_arcades": [],
        "owned_nightclubs": [],
        "owned_cars": {},
        "dirty_money": 0,
        "day": 1,
        "time_of_day": "day",
        "phase_elapsed_seconds": 0,
        "last_arcade_collection_day": 0,
        "last_club_collection_day": 0,
        **saved_data
    }

    if not is_valid_save(data):
        print("Save file is corrupted. Current progress preserved.")
        return False

    print("Loading save file")

    player = game.player

    player.money = data["money"]
    player.reputation = data["reputation"]
    player.inventory = data["inventory"]
    player.owned_properties = data["owned_properties"]
    player.owned_arcades = data["owned_arcades"]
    player.owned_nightclubs = data["owned_nightclubs"]
    player.owned_cars = data["owned_cars"]
    player.dirty_money = data["dirty_money"]
    player.last_arcade_collection_day = data["last_arcade_collection_day"]
    player.last_club_collection_day = data["last_club_collection_day"]

    game.property_levels = data["property_levels"]
    game.bank.balance = data["bank_balance"]
    game.day = data["day"]
    game.time_of_day = data["time_of_day"]
    game.phase_start_time = phase_start_from_elapsed(
        data["phase_elapsed_seconds"]
    )

    return True
