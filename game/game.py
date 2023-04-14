import cell
import random
import player
import os


# Class for Game state
class Game:
    def __init__(self):
        self.board = []
        self.sensors = {
            'breeze': False,
            'stench': False,
            'glitter': False,
            'bump': False,
            'scream': False
        }
        self.player = player.Player(0, 0)
        self.game_over = False
        self.won = False

    # Create the 4x4 game board

    def create_board(self):
        board = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(cell.Cell(i, j))
            board.append(row)
        return board

    # Set the wumpus location
    def set_wumpus(self):
        # Wumpus can be placed in any cell except the starting cell
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        # If the wumpus is placed in the starting cell, move it to a random cell
        while x == 0 and y == 0:
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        self.board[x][y].set_wumpus()

        # Set the stench sensor to true for all adjacent cells
        if x > 0:
            self.board[x - 1][y].set_stench()
        if x < 3:
            self.board[x + 1][y].set_stench()
        if y > 0:
            self.board[x][y - 1].set_stench()
        if y < 3:
            self.board[x][y + 1].set_stench()

    # Set the pit locations
    def set_pits(self):
        # Two pits
        for i in range(2):
            x = random.randint(0, 3)
            y = random.randint(0, 3)

            # If the pit is placed in the starting cell or the same cell as another pit, move it to a random cell
            while (x == 0 and y == 0) or self.board[x][y].get_pit():
                x = random.randint(0, 3)
                y = random.randint(0, 3)

            self.board[x][y].set_pit()

            # Set the breeze sensor to true for all adjacent cells
            if x > 0:
                self.board[x - 1][y].set_breeze()
            if x < 3:
                self.board[x + 1][y].set_breeze()
            if y > 0:
                self.board[x][y - 1].set_breeze()
            if y < 3:
                self.board[x][y + 1].set_breeze()

    # Set the gold location
    def set_gold(self):
        # Gold can be placed in any cell except the starting cell or pits
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        # If the gold is placed in the starting cell or a pit, move it to a random cell
        while (x == 0 and y == 0) or self.board[x][y].get_pit():
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        self.board[x][y].set_gold()

    # Set the initial state of the game board
    def set_initial_state(self):
        self.board = self.create_board()
        self.set_wumpus()
        self.set_pits()
        self.set_gold()

    # Print the game board like a matrix using +, -, and |
    def print_board(self):

        # Where is the player?
        player_x = self.player.get_x()
        player_y = self.player.get_y()

        # Print the top border
        print('+' + '---+' * 4)

        # Print the board
        for i in range(4):
            for j in range(4):
                if i == player_x and j == player_y:
                    print('| P ', end='')
                else:
                    print('|   ', end='')
            print('|')
            print('+' + '---+' * 4)


if __name__ == '__main__':
    # Create a new game to test the game class
    game = Game()
    game.set_initial_state()

    # Print the game board
    game.print_board()