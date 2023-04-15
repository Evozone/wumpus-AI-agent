import os
import game
import instructions


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
if __name__ == "__main__":
    # Tell Instructions
    instructions.display_instructions()

    # Press enter to start the game
    input("Press enter to start the game...")

    os.system("cls" if os.name == "nt" else "clear")

    # Create a new game and start it
    game = game.Game()
    game.start_game()

    while not game.game_over:

        action = getUserInput()

        game.update_game_state(action)

        os.system("cls" if os.name == "nt" else "clear")

        game.game_loop()

    # If game over, won or lost?
    if game.game_over:
        if game.won:
            print("Congratulations! You took the gold and escaped the cave alive!")
            print('-' * 50)
        else:
            print("You died! Better luck next time!")
            print('-' * 50)

        # Press enter to exit the game
        input("Press enter to exit the game...")
        os.system("cls" if os.name == "nt" else "clear")
