# Class for AI agent that is trained using NEAT

import random
import game as WuGame

class MyAgent:

    def __init__(self, net):
        self.net = net

    def __del__(self):
        pass

    def Initialize(self):
        # Add any initialization code to reset the agent for a new game
        pass

    def get_action(self, game_state, game_over):

        # Get the inputs from the game state
        inputs = self.percept_to_inputs(game_state, game_over)
        # Get the output from the neural network
        output = self.net.activate(inputs)
        # Convert the output to an action
        action = self.output_to_action(output)

        return action

    def percept_to_inputs(self, game_state, game_over):

        inputs = []

        # Add the game over flag
        inputs.append(float(game_over))

        # Add the player position
        inputs.append(game_state[5])
        inputs.append(game_state[6])

        # Add the sensor values
        inputs.append(game_state[0])
        inputs.append(game_state[1])
        inputs.append(game_state[2])
        inputs.append(game_state[3])
        inputs.append(game_state[4])

        # Add the player direction
        # north = 0, east = 1, south = 2, west = 3
        # game_state[7] is the direction the player is facing in string format
        if game_state[7] == 'north':
            inputs.append(0.0)
        elif game_state[7] == 'east':
            inputs.append(1.0)
        elif game_state[7] == 'south':
            inputs.append(2.0)
        elif game_state[7] == 'west':
            inputs.append(3.0)

        # Add the player score
        inputs.append(float(game_state[8]))

        # Add the number of move
        inputs.append(float(game_state[9]))

        return inputs

    def output_to_action(self, output):
        # Convert the output from the neural network to an action
        # The output is a list of 9 values, one for each action
        # The action with the highest value is the one that is chosen
        action_index = output.index(max(output))

        # Convert the action index to an action
        action_map = {0: 'w', 1: 's', 2: 'a', 3: 'd', 4: 'g', 5: 'x'}

        action = action_map[action_index]

        return action
