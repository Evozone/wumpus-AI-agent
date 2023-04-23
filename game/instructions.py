# Display game instructions
def display_instructions():
    print()
    print('=' * 60)
    print("Welcome to Wumpus World!")
    print('=' * 60)
    print("Instructions:")
    print(
        "- Use 'a' to turn left, 'd' to turn right, 'w' to move forward, and 's' to move backward."
    )
    print("- Use 'x' to shoot an arrow.")
    print("- Use 'q' to quit the game.")
    print("- You have 1 arrow.")

    print("- You can feel the breeze ('B') when you are near a pit ('P').")
    print("- You can smell the stench ('S') when you are near the Wumpus ('W').")

    print(
        "- Try to find the gold ('G') without falling into pits ('P') or getting caught by the Wumpus ('W')."
    )
    print("- You can grab the gold ('G') by moving to the same square as the gold.")
    print("- You can shoot the Wumpus ('W') by moving to the same square as the Wumpus.")
    print("- You can shoot the Wumpus ('W') by shooting an arrow to the same column or row as the Wumpus.")

    print("- Return to the starting point with the gold to win the game.")
    print('=' * 60)
    print("- Good luck!")
    print('=' * 60)
    print()


def display_concise_instructions():
    print('-' * 50)
    print('w: move forward | s: move backward | a: turn left | d: turn right | x: shoot arrow | g: grab gold | q: quit')
