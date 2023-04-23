import os
from game import game as WumpusWorld
from game import instructions


# Get user input
def getUserInput():
    while True:
        try:
            action = input("Enter your move: ")
            if action not in ["w", "a", "s", "d", "x", "q", "g"]:
                raise ValueError
            return action
        except ValueError:
            print("Invalid input. Please enter 'w', 'a', 's', 'd', 'x', 'q', or 'g'.")


# Main function
def run_game_with_human():
    # Tell Instructions
    instructions.display_instructions()

    # Press enter to start the game
    input("Press enter to start the game...")

    os.system("cls" if os.name == "nt" else "clear")

    # Create a new game and start it
    seed = WumpusWorld.generate_seed()
    game = WumpusWorld.Game(seed)
    game.start_game()

    while not game.game_over:

        action = getUserInput()

        game.update_game_state(action, step_by_step=True)

        os.system("cls" if os.name == "nt" else "clear")

        game.game_loop()

    # If game over, won or lost?
    if game.game_over:
        if game.game_won:
            print("Congratulations! You took the gold and escaped the cave alive!")
            print('-' * 50)
        else:
            print("Use a better strategy next time. You died!")
            print('-' * 50)

        # Press enter to exit the game
        input("Press enter to exit the game...")
        os.system("cls" if os.name == "nt" else "clear")
