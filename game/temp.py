# Create the 4x4 game board


def create_board():
    board = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(cell.Cell(i, j))
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
