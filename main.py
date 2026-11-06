from actions.handlers import ACTIONS, MENU
from businesses.night_store import get_customer_options
from core.game_state import GameState
from core.time_system import update_time_of_day


def print_status(player):
    print("PLAYER STATUS")
    print(f"Money: {player.money}")
    print(f"Reputation: {player.reputation}")
    print(f"Inventory: {player.inventory}")
    print(f"Owned Properties: {player.owned_properties}")


def main():
    name = input("What is your name? ")

    game = GameState(name)

    print_status(game.player)

    while game.player.alive:

        action = input(MENU).strip().lower()

        game.time_of_day, game.phase_start_time, game.day = update_time_of_day(
            game.time_of_day,
            game.phase_start_time,
            game.day
        )

        game.customer_options = get_customer_options(
            game.time_of_day,
            game.player.reputation
        )

        handler = ACTIONS.get(action)

        if handler:
            handler(game)
        else:
            print("Invalid option")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D or Ctrl+C: close cleanly instead of showing an error dump
        print("\nGame closed. Anything since your last save was not saved.")
