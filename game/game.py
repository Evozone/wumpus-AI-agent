# Imports
import os
import time
import game.cell as cell
import random
import game.player as player
import game.instructions as instructions

# Constants for rewards/punishments
REWARD_FOR_MOVING = -1
REWARD_FOR_SHOOTING = -10
REWARD_FOR_WINNING = 5000
REWARD_FOR_GRABBING_GOLD = 2000
REWARD_FOR_KILLING_WUMPUS = 1000
REWARD_FOR_VISITING_NEW_CELL = 200
REWARD_FOR_VISITING_OLD_CELL = -50

PUNISHMENT_FOR_DYING = -1000
PUNISHMENT_FOR_TURNING = -1
PUNISHMENT_FOR_BUMPING = -10
PUNISHMENT_FOR_REDUNDANT_ACTION = -300

# Function to generate a random seed


def generate_seed():
    seed = []

    # 0,1 = wumpus location, which cannot be (0,0)
    # 2,3 = pit 1 location, which cannot be (0,0) or (0,1) or (1,0)
    # 4,5 = pit 2 location, which cannot be (0,0) or (0,1) or (1,0) or previous pit
    # 6,7 = gold location, which cannot be (0,0) or previous pits

    # Generate the wumpus location
    seed.append(random.randint(0, 3))
    seed.append(random.randint(0, 3))
    while seed[0] == 0 and seed[1] == 0:
        seed[0] = random.randint(0, 3)
        seed[1] = random.randint(0, 3)

    # Generate the pit 1 location
    seed.append(random.randint(0, 3))
    seed.append(random.randint(0, 3))
    while (seed[2] == 0 and seed[3] == 0) or (seed[2] == 0 and seed[3] == 1) or (seed[2] == 1 and seed[3] == 0):
        seed[2] = random.randint(0, 3)
        seed[3] = random.randint(0, 3)

    # Generate the pit 2 location
    seed.append(random.randint(0, 3))
    seed.append(random.randint(0, 3))
    while (seed[4] == 0 and seed[5] == 0) or (seed[4] == 0 and seed[5] == 1) or (seed[4] == 1 and seed[5] == 0) or (seed[4] == seed[2] and seed[5] == seed[3]):
        seed[4] = random.randint(0, 3)
        seed[5] = random.randint(0, 3)

    # Generate the gold location
    seed.append(random.randint(0, 3))
    seed.append(random.randint(0, 3))
    while (seed[6] == 0 and seed[7] == 0) or (seed[6] == seed[2] and seed[7] == seed[3]) or (seed[6] == seed[4] and seed[7] == seed[5]):
        seed[6] = random.randint(0, 3)
        seed[7] = random.randint(0, 3)

    return seed


# Class for Game state
class Game:
   # Constructor
    def __init__(self, seed):
        self.seed = seed
        self.board = []
        self.sensors = {
            'breeze': False,
            'stench': False,
            'glitter': False,
            'bump': False,
            'scream': False
        }
        self.previous_sensors = {
            'breeze': False,
            'stench': False,
            'glitter': False,
            'bump': False,
            'scream': False
        }
        self.player = player.Player(0, 0)
        self.game_over = False
        self.game_won = False
        self.size_of_cave = 4
        self.num_pits = 2

    # Create the 4x4 game board (the cave)
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
        x = self.seed[0]
        y = self.seed[1]

        # Set the wumpus in the cell
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
        for i in range(self.num_pits):
            x = self.seed[2 + (i * 2)]
            y = self.seed[3 + (i * 2)]

            # If the pit is placed in the starting cell or the same cell as another pit, move it to a random cell
            # Wumpus is big enough to not fall in a pit, so it is not checked here
            while (x == 0 and y == 0) or (x == 0 and y == 1) or (x == 1 and y == 0) or self.board[x][y].get_pit():
                x = random.randint(0, 3)
                y = random.randint(0, 3)

            # Set the pit in the cell
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
        x = self.seed[6]
        y = self.seed[7]

        # If the gold is placed in the starting cell or a pit, move it to a random cell
        while (x == 0 and y == 0) or self.board[x][y].get_pit():
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        # Set the gold in the cell
        self.board[x][y].set_gold(True)

    # Set the initial state of the game board
    def set_initial_state(self):
        self.board = self.create_board()
        self.set_wumpus()
        self.set_pits()
        self.set_gold()

    # Print the game board like a matrix using +, -, and |
    def print_board(self):
        # Where is the player?
        player_x, player_y = self.player.get_player_position()
        player_direction = self.player.get_player_direction()

        # Print the top border
        print('+' + '---+' * 4)

        # Print the board
        for i in range(4):
            for j in range(4):
                if i == player_x and j == player_y:
                    # If player direction is north, print ^, else if player direction is east, print >, etc.
                    if player_direction == 'north':
                        print('| ^ ', end='')
                    elif player_direction == 'east':
                        print('| > ', end='')
                    elif player_direction == 'south':
                        print('| v ', end='')
                    elif player_direction == 'west':
                        print('| < ', end='')
                else:
                    print('|   ', end='')
            print('|')
            print('+' + '---+' * 4)

    # Update the sensors for gold, breeze, and stench
    def update_sensors(self):
        x, y = self.player.get_player_position()
        cell = self.board[x][y]
        self.sensors['glitter'] = cell.get_glitter()
        self.sensors['breeze'] = cell.get_breeze()
        self.sensors['stench'] = cell.get_stench()

    # Update game state using the action
    def update_game_state(self, action, step_by_step=False):
        # Determine if the action is a movement, direction change, or interaction
        if action in ['w', 's']:
            # Sensor for bump is updated inside move_player
            self.player.set_num_moves(self.player.get_num_moves() + 1)
            self.move_player(action)

            x, y = self.player.get_player_position()

            # Check if the player is in a cell with a wumpus or pit after moving
            if self.board[x][y].get_wumpus():
                self.player.set_alive(False)
                print("You were eaten by the Wumpus!") if step_by_step else None
                input("Press enter to continue...") if step_by_step else None
            elif self.board[x][y].get_pit():
                self.player.set_alive(False)
                print("You fell into a pit and died!") if step_by_step else None
                input("Press enter to continue...") if step_by_step else None

        elif action in ['a', 'd']:
            self.player.set_num_moves(self.player.get_num_moves() + 1)
            self.change_direction(action)

        elif action in ['g', 'q', 'x']:
            # Sensor for scream is updated inside interact
            self.player.set_num_moves(self.player.get_num_moves() + 1)
            self.interact(action, step_by_step)

        # Update the sensors for gold, breeze, and stench after the action
        self.update_sensors()

        # If the player is dead after the action, the game is over
        if not self.player.get_alive():
            # Decrease score by 1000 and set game over to true
            self.player.set_score(
                self.player.get_score() + PUNISHMENT_FOR_DYING)
            self.game_over, self.game_won = True, False
            return

        # If the player is in 0, 0 with the gold, the game is over and the player wins
        if self.player.get_player_position() == (0, 0) and self.player.get_has_gold():
            # Increase score by 5000 and set game over to true
            self.player.set_score(self.player.get_score() + REWARD_FOR_WINNING)
            self.game_over = True
            self.game_won = True

        # If the player didn't change cell, decrease score by REWARD_FOR_VISITING_OLD_CELL
        if self.player.get_player_position() == self.player.get_previous_position(-1):
            self.player.set_score(
                self.player.get_score() + REWARD_FOR_VISITING_OLD_CELL // 2)

        # If the position same as 4th last position (full circle with direction change)
        if self.player.get_player_position() == self.player.get_previous_position(-4):
            self.player.set_score(
                self.player.get_score() + REWARD_FOR_VISITING_OLD_CELL * 5)

    # Move the player
    def move_player(self, action):
        # Define a dictionary that maps actions to position changes
        action_to_delta = {'w': 1, 's': -1}

        # Moving costs 20 points
        self.player.set_score(self.player.get_score() + REWARD_FOR_MOVING)

        # Get the current direction and position
        direction = self.player.get_player_direction()
        x, y = self.player.get_player_position()

        # Get the change in x and y based on the direction
        delta_x, delta_y = 0, 0
        if direction == 'north':
            delta_x = -action_to_delta[action]
        elif direction == 'east':
            delta_y = action_to_delta[action]
        elif direction == 'south':
            delta_x = action_to_delta[action]
        elif direction == 'west':
            delta_y = -action_to_delta[action]

        # Calculate the new position
        new_x, new_y = x + delta_x, y + delta_y

        # Check if the new position is out of bounds
        if new_x < 0 or new_x >= self.size_of_cave or new_y < 0 or new_y >= self.size_of_cave:
            # If so, set the bump sensor to true and don't move the player
            self.sensors['bump'] = True

            # Punish the ai for bumping into the wall. If the previous sensors contained a bump, punish the ai even more
            if self.previous_sensors['bump']:
                self.player.set_score(
                    self.player.get_score() + PUNISHMENT_FOR_REDUNDANT_ACTION * 2)
            else:
                self.player.set_score(
                    self.player.get_score() + PUNISHMENT_FOR_BUMPING)

            return

        # Move the player and update the sensors
        self.player.set_player_position(new_x, new_y)
        # Check if cell is new or not
        if not self.board[new_x][new_y].get_visited():
            self.board[new_x][new_y].set_visited()
            self.player.set_score(
                self.player.get_score() + REWARD_FOR_VISITING_NEW_CELL)
        else:
            self.player.set_score(
                self.player.get_score() + REWARD_FOR_VISITING_OLD_CELL * 2)

        self.sensors['bump'] = False

    # Change the direction of the player
    def change_direction(self, action):
        DIRECTIONS = ['north', 'east', 'south', 'west']
        # Directions are a to the left and d to the right
        # Define a dictionary that maps actions to direction changes
        action_to_delta = {'a': -1, 'd': 1}

        # Get the current direction and position
        direction = self.player.get_player_direction()

        # Get the change in direction based on the action
        delta = action_to_delta[action]

        # Calculate the new direction
        new_direction = DIRECTIONS[(DIRECTIONS.index(direction) + delta) % 4]

        # Change the direction of the player
        self.player.set_player_direction(new_direction)
        # The position of the player doesn't change
        x, y = self.player.get_player_position()
        self.player.set_player_position(x, y)

        # Turning costs 10 points
        self.player.set_score(self.player.get_score() + PUNISHMENT_FOR_TURNING)

    # Interact with the environment
    def interact(self, action, step_by_step=False):
        if action == 'g':
            # Grab the gold if the player is on the same cell as the gold
            x, y = self.player.get_player_position()
            if self.board[x][y].get_gold():
                self.board[x][y].set_gold(False)
                self.player.set_has_gold(True)
                self.player.set_score(
                    self.player.get_score() + REWARD_FOR_GRABBING_GOLD)
                self.sensors['glitter'] = False
            else:
                # No gold to grab: punish the ai
                self.player.set_score(self.player.get_score(
                ) + PUNISHMENT_FOR_REDUNDANT_ACTION)

        elif action == 'q':
            # Quit the game
            self.game_over = True

        # Else if action is to shoot an arrow
        elif action == 'x':
            # Check if the player has an arrow
            if self.player.get_has_arrow():
                self.player.set_has_arrow(False)
                self.shoot_arrow()
            else:
                print("You don't have an arrow!") if step_by_step else None
                input("Press enter to continue...") if step_by_step else None
                self.player.set_score(self.player.get_score(
                ) + PUNISHMENT_FOR_REDUNDANT_ACTION)

    # Shoot the arrow
    def shoot_arrow(self):
        # Decrease score by 10
        self.player.set_score(self.player.get_score() + REWARD_FOR_SHOOTING)

        # Get the current position and direction of the player
        x, y = self.player.get_player_position()
        arrow_direction = self.player.get_player_direction()

        arrow_cells = [(x, y)]

        if arrow_direction == 'north':
            for i in range(x - 1, -1, -1):
                arrow_cells.append((i, y))
        elif arrow_direction == 'east':
            for i in range(y + 1, self.size_of_cave):
                arrow_cells.append((x, i))
        elif arrow_direction == 'south':
            for i in range(x + 1, self.size_of_cave):
                arrow_cells.append((i, y))
        elif arrow_direction == 'west':
            for i in range(y - 1, -1, -1):
                arrow_cells.append((x, i))

        # Check if the arrow hits the wumpus
        for cell in arrow_cells:
            if self.board[cell[0]][cell[1]].get_wumpus():
                self.kill_wumpus(cell[0], cell[1])
                return

    # Kill wumpus and remove stench from surrounding cells
    def kill_wumpus(self, x, y):
        # Check if the cell has a wumpus
        if self.board[x][y].get_wumpus():
            self.board[x][y].set_wumpus(False)
            self.sensors['scream'] = True

            # Increase score by 1000
            self.player.set_score(
                self.player.get_score() + REWARD_FOR_KILLING_WUMPUS)

            # Remove the stench from the surrounding cells
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i < self.size_of_cave and j >= 0 and j < self.size_of_cave:
                        self.board[i][j].set_stench(False)

    # Functions for the AI agent
    def get_fitness(self):
        fitness = self.player.get_score()
        # if player died but still has gold, increase fitness by 2000 for effort
        if self.player.get_has_gold() and not self.player.get_alive():
            fitness += 2000

        # if player died after only 2 moves, decrease fitness by 1000
        if not self.player.get_alive() and self.player.get_num_moves() < 2:
            fitness -= 1000

        # if player died but still has arrow, decrease fitness by 800
        if not self.player.get_alive() and self.player.get_has_arrow():
            fitness -= 800

        # if player sees gold but doesn't pick it up, decrease fitness by 500
        if self.sensors['glitter'] and not self.player.get_has_gold():
            fitness -= 500

        # If less than 5 cells have been visited, then decrease score by 800
        def count_visited_cells():
            count = 0
            for i in range(self.size_of_cave):
                for j in range(self.size_of_cave):
                    if self.board[i][j].get_visited():
                        count += 1
            return count

        if count_visited_cells() < 5:
            fitness -= 800
        elif count_visited_cells() > 7:
            fitness += 500

        # If player has gold and is close to the exit, increase fitness by a function of the distance to the exit
        if self.player.get_has_gold():
            x, y = self.player.get_player_position()
            dist = abs(x - 0) + abs(y - 0) + 1
            fitness += 1000 / dist

        # Reward player for every move it has gold
        if self.player.has_gold:
            fitness += 50 * self.player.get_num_moves()

        return (fitness * 100) // self.player.get_num_moves()

    def get_state(self):
        # Convert sensors's dictionary to a list of true/false values
        sensors = [self.sensors[key] for key in self.sensors]
        # Conver to float for the neural network
        sensors = [float(i) for i in sensors]

        inputs = []

        # Add the sensors to the inputs
        inputs.extend(sensors)

        # Add the player's position to the inputs
        inputs.extend(self.player.get_player_position())

        # Add the player's direction to the inputs
        inputs.append(self.player.get_player_direction())

        # Add the player's score to the inputs
        inputs.append(self.player.get_score())

        # Add the player's number of moves to the inputs
        inputs.append(self.player.get_num_moves())

        return inputs

    def run_game_with_ai(self, ai_agent, step_by_step=False):
        # Run the game until it is over
        self.set_initial_state()

        if step_by_step:
            # Print the board
            self.print_board()

            # Print the score
            self.print_score()

        if step_by_step:
            # Print the sensors
            self.print_sensors()

            # Sleep for 0.5
            time.sleep(0.5)

            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')

        while not self.game_over:
            # Get the current state of the game and pass it to the AI agent
            state = self.get_state()

            # Get the action from the AI agent
            action = ai_agent.get_action(state, self.game_over)

            # Update the game state
            self.update_game_state(action, step_by_step)

            if step_by_step:
                # Print the board
                self.print_board()

                # Print the action
                print('Action: ' + action)

                # Print the score
                self.print_score()

            # Restrict to a certain number of moves using player's get_num_moves()
            if self.player.get_num_moves() >= 100 or self.player.get_score() < 0:
                self.game_over = True
                self.game_won = False
                print('Game over! You ran out of moves.') if step_by_step else None

            if step_by_step:
                # Print the sensors
                self.print_sensors()

                # Sleep for 0.5
                time.sleep(1)

                # Clear the screen
                os.system('cls' if os.name == 'nt' else 'clear')

            # Reset the sensors
            self.previous_sensors = self.sensors.copy()
            self.reset_sensors()

        if step_by_step:
            # Print the board
            self.print_board()

            # Print the action
            print('Action: ' + action)

            # Print the final score
            self.print_score()

            # Print the game over message
            if self.game_won:
                print('You won!')
            else:
                print('You lost!')

    # Functions for the human player
    def print_score(self):
        print('Score: ' + str(self.player.get_score()))

    def print_sensors(self):
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

    def print_previous_sensors(self):
        print(self.previous_sensors)

    def game_loop(self):
        instructions.display_concise_instructions()
        print('-' * 50)
        self.print_board()
        print('-' * 50)
        self.get_state()
        print('-' * 50)
        self.print_score()
        print('-' * 50)
        self.update_sensors()
        self.print_sensors()
        print('-' * 50)
        self.previous_sensors = self.sensors.copy()
        self.reset_sensors()

    def start_game(self):
        self.set_initial_state()
        self.game_loop()


if __name__ == '__main__':
    print('game.py test')
    game = Game()

    game.get_state()
