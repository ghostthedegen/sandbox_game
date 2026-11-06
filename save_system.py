import json

def save_game(
    money,
    reputation,
    inventory,
    owned_properties,
    property_levels,
    bank_balance,
    owned_arcades,
    owned_nightclubs,
    owned_cars,
    dirty_money,
    day,
    time_of_day,
    phase_elapsed_seconds,
    last_arcade_collection_day,
    last_club_collection_day
):
    game_data = {
        "money": money,
        "reputation": reputation,
        "inventory": inventory,
        "owned_properties": owned_properties,
        "property_levels": property_levels,
        "bank_balance": bank_balance,
        "owned_arcades": owned_arcades,
        "owned_nightclubs": owned_nightclubs,
        "owned_cars": owned_cars,
        "dirty_money": dirty_money,
        "day": day,
        "time_of_day": time_of_day,
        "phase_elapsed_seconds": phase_elapsed_seconds,
        "last_arcade_collection_day": last_arcade_collection_day,
        "last_club_collection_day": last_club_collection_day
    }

    with open("save_data.json", "w") as file:
        json.dump(game_data, file, indent=4)

    print("Game saved")


def load_game():

    try:
        with open("save_data.json", "r") as file:
            game_data = json.load(file)
            print("Loading save file")

        return (
            game_data.get("money", 500),
            game_data.get("reputation", 0),
            game_data.get("inventory", {}),
            game_data.get("owned_properties", []),
            game_data.get("property_levels", {"small_shop": 1}),
            game_data.get("bank_balance", 0),
            game_data.get("owned_arcades", []),
            game_data.get("owned_nightclubs", []),
            game_data.get("owned_cars", {}),
            game_data.get("dirty_money", 0),
            game_data.get("day", 1),
            game_data.get("time_of_day", "day"),
            game_data.get("phase_elapsed_seconds", 0),
            game_data.get("last_arcade_collection_day", 0),
            game_data.get("last_club_collection_day", 0)
        )

    except FileNotFoundError:
        print("No save file found. Current progress preserved.")
        return None

    except json.JSONDecodeError:
        print("Save file is corrupted. Current progress preserved.")
        return None