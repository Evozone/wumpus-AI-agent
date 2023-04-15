import random
import os
import cell
import player
import game
import instructions


# Get user input
def getUserInput():
    while True:
        try:
            action = input("Enter your move: ")
            if action not in ["w", "a", "s", "d", "x", " ", "q"]:
                raise ValueError
            return action
        except ValueError:
            print("Invalid input. Please enter 'w', 'a', 's', 'd','x' or ' '.")


# Main function
if __name__ == "__main__":
    # Tell Instructions
    instructions.display_instructions()
    # Create a new game
    game = game.Game()
    # Start the game
    game.start_game()

    # While game is not over
    while not game.game_over:

        # try catch to check valid input only pass w,a,s,d,spacebar
        action = getUserInput()

        # Execute the player's move
        game.update_game_state(action)

        # Clear the screen as per OS
        os.system("cls" if os.name == "nt" else "clear")

        game.print_board()

        game.print_score()

        game.print_sensors()
