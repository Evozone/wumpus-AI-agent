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
        # Get the game state as a list of inputs
        score, sensors, playerX, playerY, playerGold, playerArrow, last_sensor, cave = game_state

        # Map last sensor to a number
        last_sensor_map = {None: 0, 'bump': 1, 'scream': 2}

        last_sensor = last_sensor_map[last_sensor]

        # Flatten cave (4x4) to a list of 16
        cave = [c for row in cave for c in row]

        # Inputs are score is a number, sensors are boolean, game_over is boolean
        # Convert boolean sensors to 0 or 1 and score to float
        inputs = [float(game_over)] + [float(s)
                                       for s in sensors] + [float(score)] + [float(playerX)] + [float(playerY)] + [float(playerGold)] + [float(playerArrow)] + [float(last_sensor)] + [float(c) for c in cave]
        return inputs

    def output_to_action(self, output):
        # Convert the output from the neural network to an action
        # The output is a list of 9 values, one for each action
        # The action with the highest value is the one that is chosen
        action_index = output.index(max(output))

        # Convert the action index to an action
        action_map = {0: 'g', 1: 'w', 2: 'a', 3: 's', 4: 'd',
                      5: 'xw', 6: 'xa', 7: 'xs', 8: 'xd'}

        action = action_map[action_index]

        return action
