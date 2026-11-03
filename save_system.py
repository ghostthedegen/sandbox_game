import json

def save_game(money, reputation, inventory, owned_properties, property_levels, bank_balance):

    game_data = {
        "money": money,
        "reputation": reputation,
        "inventory": inventory,
        "owned_properties": owned_properties,
        "property_levels": property_levels,
        "bank_balance": bank_balance
    }

    with open("save_data.json", "w")as file:
        json.dump(game_data, file, indent=4)

    print("Game saved")

def load_game():

    try:
        with open("save_data.json", "r") as file:
            game_data = json.load(file)
            print("Loading save file")
        
        # .get() fills in defaults so older save files without a field still load
        return (
            game_data.get("money", 500),
            game_data.get("reputation", 0),
            game_data.get("inventory", {}),
            game_data.get("owned_properties", []),
            game_data.get("property_levels", {"small_shop": 1}),
            game_data.get("bank_balance", 0)
        )
    except FileNotFoundError:
        print("No saved files")
        return (
            500,
            0,
            {},
            [],
            {"small_shop": 1},
            0
        )
