import neat
from neat.checkpoint import Checkpointer
# from ai import visualize
import os
import pickle

import ai.ai_agent as ai_agent
import game.game as WuGame

# Number of generations to run the NEAT evolution process
GENERATIONS = 300

# This function is called when the NEAT evolution process is run
def run_neat(config_file):
    # Load the NEAT configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population
    population = neat.Population(config)

    # Add a reporter to show progress in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Define the fitness function
    def eval_genomes(genomes, config):

        # Create a game instance for each generation
        seed = WuGame.generate_seed()

        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            agent = ai_agent.MyAgent(net)

            # Run the game with the agent
            game = WuGame.Game(seed)
            game.run_game_with_ai(agent)

            # Fitness is some function of the score and the number of moves
            # It's good to have a fitness function that is always positive
            # and increases as the score increases

            genome.fitness = game.get_fitness()

    # Run the NEAT evolution process
    winner = population.run(eval_genomes, GENERATIONS)

    # Visualize the winning genome
    # visualize_genome(winner, config)

    # Save the winning genome
    with open('winner_genome.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)


# Function to visualize the network
# def visualize_genome(genome, config):

#     # Name the nodes
#     node_names = {-1: 'game_over', -2: 'breeze', -3: 'stench', -4: 'glitter', -5: 'bump', -6: 'scream', -7: 'x', -8: 'y', -9: 'direction', -10: 'score', -11: 'num_moves',
#                   0: 'move_forward', 1: 'move_backward', 2: 'turn_left', 3: 'turn_right', 4: 'grab', 5: 'shoot'}

#     visualize.draw_net(config, genome, view=True,
#                        filename="neural_network.png", node_names=node_names)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(
        local_dir, "ai", "config", "neat_config.txt")
    run_neat(config_path)
