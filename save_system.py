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
        
        return (
            game_data["money"],
            game_data["reputation"],
            game_data["inventory"],
            game_data["owned_properties"],
            game_data["property_levels"],
            game_data["bank_balance"]
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
