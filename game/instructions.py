# Display game instructions
def display_instructions():
    print()
    print('=' * 60)
    print("Welcome to Wumpus World!")
    print('=' * 60)
    print("Instructions:")
    print(
        "- Use 'w' to move up, 's' to move down, 'a' to move left, and 'd' to move right."
    )
    print("- Use 'x' to shoot an arrow.")
    print("- Use 'q' to quit the game.")
    print("- You have 1 arrow.")

    print("- You can feel the breeze ('B') when you are near a pit ('P').")
    print("- You can smell the stench ('S') when you are near the Wumpus ('W').")

    print(
        "- Try to find the gold ('G') without falling into pits ('P') or getting caught by the Wumpus ('W')."
    )
    print("- Return to the starting point to win the game.")
    print('=' * 60)
    print("- Good luck!")
    print('=' * 60)
    print()


def display_concise_instructions():
    print('-' * 50)
    print('w: up | s: down | a: left | d: right | x: shoot | g: grab | q: quit')
