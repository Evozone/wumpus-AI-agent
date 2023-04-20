# Imports
import os
import time
import game.cell as cell
import random
import game.player as player
import game.instructions as instructions


# Class for Game state
class Game:
    # Constructor
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
        self.size = 4
        self.was_last_sensor_bump = False

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

        # If the wumpus is placed in the starting cell, or 0, 1 or 1, 0, move it to a random cell
        while (x == 0 and y == 0) or (x == 0 and y == 1) or (x == 1 and y == 0):
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        self.board[x][y].set_wumpus(True)

        # Set the stench sensor to true for all adjacent cells
        if x > 0:
            self.board[x - 1][y].set_stench(True)
        if x < 3:
            self.board[x + 1][y].set_stench(True)
        if y > 0:
            self.board[x][y - 1].set_stench(True)
        if y < 3:
            self.board[x][y + 1].set_stench(True)

    # Set the pit locations
    def set_pits(self):
        # Two pits
        for i in range(2):
            x = random.randint(0, 3)
            y = random.randint(0, 3)

            # If the pit is placed in the starting cell or the same cell as another pit, move it to a random cell
            while (x == 0 and y == 0) or (x == 0 and y == 1) or (x == 1 and y == 0) or self.board[x][y].get_pit():
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
        if x > 0:
            self.board[x - 1][y].set_glitter()
        if x < 3:
            self.board[x + 1][y].set_glitter()
        if y > 0:
            self.board[x][y - 1].set_glitter()
        if y < 3:
            self.board[x][y + 1].set_glitter()

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
                    print('| ⨀ ', end='')
                else:
                    print('|   ', end='')
            print('|')
            print('+' + '---+' * 4)

    # Update the sensors for gold, breeze, and stench
    def update_sensors(self):
        x, y = self.player.get_x(), self.player.get_y()
        cell = self.board[x][y]
        self.sensors['glitter'] = cell.has_gold
        self.sensors['breeze'] = cell.has_breeze
        self.sensors['stench'] = cell.has_stench

    # Update game state using the action
    def update_game_state(self, action):
        # Determine if the action is a movement or interaction
        if action in ['w', 'a', 's', 'd']:
            # Sensor for bump is updated inside move_player
            self.player.set_num_moves(self.player.get_num_moves() + 1)
            self.move_player(action)

            # Check if the player is in a cell with a pit or Wumpus
            if self.board[self.player.get_x()][self.player.get_y()].has_pit:
                self.player.set_alive(False)
                # print("You fell into a pit and died!")
            elif self.board[self.player.get_x()][self.player.get_y()].has_wumpus:
                self.player.set_alive(False)
                # print("You were eaten by the Wumpus!")

        elif action in ['g', 'q', 'xw', 'xa', 'xs', 'xd']:
            # Sensor for scream is updated inside interact
            self.player.set_num_moves(self.player.get_num_moves() + 1)
            self.interact(action)

        # If the player is dead, the game is over
        if not self.player.get_alive():
            # Decrease score by 1000
            self.player.set_score(self.player.get_score() - 10000)
            self.game_over = True
            return

        # Update the sensors for gold, breeze, and stench
        self.update_sensors()

        # If the player is in 0, 0 with the gold, the game is over and the player wins
        if self.player.get_x() == 0 and self.player.get_y() == 0 and self.player.has_gold:
            # Increase score by 1000
            self.player.set_score(self.player.get_score() + 5000)
            self.game_over = True
            self.won = True

    # Move the player
    def move_player(self, action):

        # Define a dictionary that maps actions to position changes
        action_to_delta = {
            'w': (-1, 0),
            's': (1, 0),
            'a': (0, -1),
            'd': (0, 1),
        }

        # decrease score by 1
        self.player.set_score(self.player.get_score() - 1)

        # Get the position change for the given action from the dictionary
        delta = action_to_delta.get(action)

        if delta is None:
            return

        # Calculate the new position of the player
        new_x = self.player.get_x() + delta[0]
        new_y = self.player.get_y() + delta[1]

        # Check if the new position is out of bounds
        if new_x < 0 or new_x >= self.size or new_y < 0 or new_y >= self.size:
            # decrease score by amount of times bumped
            if self.was_last_sensor_bump:
                self.player.set_score(
                    self.player.get_score() - 1000)
            else:
                self.player.set_score(
                    self.player.get_score() - 50)
            self.sensors['bump'] = True
            self.was_last_sensor_bump = True
            return

        # Move the player and update the sensors
        self.player.set_x(new_x)
        self.player.set_y(new_y)

        self.was_last_sensor_bump = False

    # Interact with the environment
    def interact(self, action):
        if action == 'g':
            # Grab the gold if the player is on the same cell as the gold
            x, y = self.player.get_x(), self.player.get_y()
            if self.board[x][y].has_gold:
                self.board[x][y].has_gold = False
                self.player.has_gold = True
                self.player.set_score(self.player.get_score() + 2000)
                self.sensors['glitter'] = False
            else:
                # No gold to grab: punish the ai
                self.player.set_score(self.player.get_score() - 100)

        elif action == 'q':
            # Quit the game
            self.game_over = True

        # Else if action starts with x, it is an arrow action
        elif action[0] == 'x':
            # Check if the player has an arrow
            if self.player.has_arrow:
                self.player.has_arrow = False
                self.shoot_arrow(action[1:])
            else:
                # print("You don't have an arrow!")
                self.player.set_score(self.player.get_score() - 500)

    # Kill wumpus and remove stench
    def kill_wumpus(self, x, y):
        # Check if the cell has a wumpus
        if self.board[x][y].has_wumpus:
            self.board[x][y].has_wumpus = False
            self.sensors['scream'] = True

            # Remove the stench from the surrounding cells
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i < self.size and j >= 0 and j < self.size:
                        self.board[i][j].has_stench = False

            # Update the sensors
            self.update_sensors()

    # Shoot the arrow
    def shoot_arrow(self, arrow_direction):
        # Decrease score by 10
        self.player.set_score(self.player.get_score() - 10)

        # Get the current position of the player
        x, y = self.player.get_x(), self.player.get_y()

        # Get which column or row the arrow will travel on
        if arrow_direction in ['w', 's']:
            arrow_travel = y

            # Kill wumpus in all cells in the column
            for i in range(self.size):
                self.kill_wumpus(i, arrow_travel)
        else:
            arrow_travel = x

            # Kill wumpus in all cells in the row
            for j in range(self.size):
                self.kill_wumpus(arrow_travel, j)

    # Functions for the AI agent
    def get_fitness(self):
        return self.player.score

    def get_state(self):
        # Convert sensors's dictionary to a list of true/false values
        sensors = [self.sensors['breeze'], self.sensors['stench'], self.sensors['glitter'], self.sensors['bump'],
                   self.sensors['scream']]

        return self.player.score, sensors

    def is_game_over(self):
        return self.game_over

    def is_won(self):
        return self.won

    def run_game_with_ai(self, ai_agent, step_by_step=False):
        # Run the game until it is over
        self.set_initial_state()

        while not self.game_over:
            # Get the current state of the game and pass it to the AI agent
            state = self.get_state()

            # Get the action from the AI agent
            action = ai_agent.get_action(state, self.game_over)

            # Update the game state
            self.update_game_state(action)

            if step_by_step:
                # Print the board
                self.print_board()

                # Print the action
                print('Action: ' + action)

                # Print the score
                self.print_score()

            # Restrict to a certain number of moves using player's get_num_moves()
            if self.player.get_num_moves() >= 30:
                self.game_over = True
                self.won = False

            if step_by_step:
                # Print the sensors
                self.print_sensors()

                # Sleep for 0.1 seconds
                time.sleep(0.1)

                # Clear the screen
                os.system('cls' if os.name == 'nt' else 'clear')

            # Reset the sensors
            self.reset_sensors()

        if step_by_step:
            # Print the final score
            self.print_score()

            # Print the game over message
            if self.won:
                print('You won!')
            else:
                print('You lost!')

    # Functions for the human player
    def print_score(self):
        print('Score: ' + str(self.player.get_score()))

    def print_sensors(self):
        # print('Sensors: ' + str(self.sensors))

        # In human like language. Whatever is true is printed.
        if self.sensors['breeze']:
            print('You feel a breeze. Something cold, dark and deep is nearby.')
        if self.sensors['stench']:
            print('You smell a stench. Ew!')
        if self.sensors['glitter']:
            print('You see a glitter. Something shiny!')
        if self.sensors['bump']:
            print('You bump into a wall. Ouch!')
        if self.sensors['scream']:
            print('You hear a wild, blood-curdling scream.')

    def reset_sensors(self):
        self.sensors = {
            'breeze': False,
            'stench': False,
            'glitter': False,
            'bump': False,
            'scream': False,
        }

    def game_loop(self):
        instructions.display_concise_instructions()
        print('-' * 50)
        self.print_board()
        print('-' * 50)
        self.print_score()
        print('-' * 50)
        self.update_sensors()
        self.print_sensors()
        print('-' * 50)
        self.reset_sensors()

    def start_game(self):
        self.set_initial_state()
        self.game_loop()


if __name__ == '__main__':
    print('game.py test')
