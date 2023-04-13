import random
import os

sensors = {
    'breeze': False,
    'stench': False,
    'glitter': False,
    'bump': False,
    'scream': False
}


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.has_wumpus = False
        self.has_pit = False
        self.has_gold = False

    def __repr__(self):
        return f"Cell(x={self.x}, y={self.y}, visited={self.visited}, has_wumpus={self.has_wumpus}, has_pit={self.has_pit}, has_gold={self.has_gold})"


# Create the 4x4 game board
def create_board():
    board = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(Cell(i, j))
        board.append(row)
    return board


# Set the initial state of the game board
def set_initial_state(board):
    # Set the initial player position
    board[0][0].visited = True

    # Set the initial wumpus position
    wumpus_x = random.randint(0, 3)
    wumpus_y = random.randint(0, 3)
    board[wumpus_x][wumpus_y].has_wumpus = True

    # Set the initial pit positions
    pit_x = random.randint(0, 3)
    pit_y = random.randint(0, 3)
    while pit_x == wumpus_x and pit_y == wumpus_y:
        pit_x = random.randint(0, 3)
        pit_y = random.randint(0, 3)
    board[pit_x][pit_y].has_pit = True

    # Set the initial gold position
    gold_x = random.randint(0, 3)
    gold_y = random.randint(0, 3)
    while gold_x == wumpus_x and gold_y == wumpus_y:
        gold_x = random.randint(0, 3)
        gold_y = random.randint(0, 3)
    board[gold_x][gold_y].has_gold = True


# Function to display the game board with borders
def display_board(board):
    print("|---|---|---|---|")
    for i in range(4):
        print("|", end="")
        for j in range(4):
            if board[i][j].visited:
                if board[i][j].has_wumpus:
                    print(" W ", end="|")
                elif board[i][j].has_pit:
                    print(" O ", end="|")
                elif board[i][j].has_gold:
                    print(" G ", end="|")
                else:
                    print("   ", end="|")
            else:
                print(" X ", end="|")
        print("\n|---|---|---|---|")


# Function to update the sensors based on the current player position


# Function to move the player based on user input
def move_player(direction, board):
    # Get the current player position
    player_x = 0
    player_y = 0
    for i in range(4):
        for j in range(4):
            if board[i][j].visited:
                player_x = i
                player_y = j

    # Move the player based on user input
    if direction == 'up':
        if player_x == 0:
            print("You can't move up!")
            sensors['bump'] = True
        else:
            board[player_x][player_y].visited = False
            board[player_x - 1][player_y].visited = True
    elif direction == 'down':
        if player_x == 3:
            print("You can't move down!")
            sensors['bump'] = True
        else:
            board[player_x][player_y].visited = False
            board[player_x + 1][player_y].visited = True
    elif direction == 'left':
        if player_y == 0:
            print("You can't move left!")
            sensors['bump'] = True
        else:
            board[player_x][player_y].visited = False
            board[player_x][player_y - 1].visited = True
    elif direction == 'right':
        if player_y == 3:
            print("You can't move right!")
            sensors['bump'] = True
        else:
            board[player_x][player_y].visited = False
            board[player_x][player_y + 1].visited = True


# Display game instructions
def display_instructions():
    print("Welcome to Wumpus World!")
    print("Instructions:")
    print(
        "- Use 'w' to move up, 's' to move down, 'a' to move left, and 'd' to move right."
    )
    print(
        "- Try to find the gold ('G') without falling into pits ('P') or getting caught by the Wumpus ('W')."
    )
    print("- Good luck!")
    print()


# Function to initialize the game
def init_game():
    # Clear the screen
    os.system('clear')

    # Display game instructions
    display_instructions()

    # Create the game board
    board = create_board()

    # Set the initial state of the game board
    set_initial_state(board)

    # Display initial game board
    display_board(board)

    return board


# Function to check if the game is over
def check_game_over(board):
    # Get the current player position
    player_x = 0
    player_y = 0
    for i in range(4):
        for j in range(4):
            if board[i][j].visited:
                player_x = i
                player_y = j

    # Check if the player has fallen into a pit or been eaten by the Wumpus
    if board[player_x][player_y].has_pit:
        print("You fell into a pit! Game over.")
        return True
    elif board[player_x][player_y].has_wumpus:
        print("You were eaten by the Wumpus! Game over.")
        return True

    # Check if the player has found the gold
    if board[player_x][player_y].has_gold:
        print("You found the gold! You win!")
        return True


def game_loop(board):
    # Main game loop
    while True:
        # Get user input for direction
        direction = input("\n\n Enter your move (w/s/a/d): \n").lower()

        # Move the player based on user input
        if direction == 'w':
            move_player('up', board)
        elif direction == 's':
            move_player('down', board)
        elif direction == 'a':
            move_player('left', board)
        elif direction == 'd':
            move_player('right', board)
        else:
            print("Invalid input. Please try again.")
            continue

        # Check if the game is over
        if check_game_over(board):
            # Clear the screen (if Windows, use 'cls' instead of 'clear')
            break
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        # Display updated game board
        display_board(board)

        # Show sensors
        print(sensors)

        # Reset the sensors
        for key in sensors:
            sensors[key] = False


if __name__ == "__main__":
    board = init_game()
    game_loop(board)
