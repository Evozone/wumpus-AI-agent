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
        score, sensors = game_state

        # Inputs are score is a number, sensors are boolean, game_over is boolean
        # Convert boolean sensors to 0 or 1 and score to float
        inputs = [float(game_over)] + [float(s)
                                       for s in sensors] + [float(score)]

        return inputs

    def output_to_action(self, output):
        # Convert the output from the neural network to an action
        # The output is a list of 9 values, one for each action
        # The action with the highest value is the one that is chosen
        action_index = output.index(max(output))

        # Convert the action index to an action
        action_map = {0: 's', 1: 'd', 2: 'w', 3: 'a',
                      4: 'g', 5: 'xs', 6: 'xd', 7: 'xw', 8: 'xa'}

        action = action_map[action_index]

        return action
