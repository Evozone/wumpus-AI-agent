import neat
import os
import pickle

import ai.ai_agent as ai_agent
import game.game as WuGame


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
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            agent = ai_agent.MyAgent(net)
            game = WuGame.Game()
            game.run_game_with_ai(agent)

            # Calculate the fitness based on the game score, for example
            score = game.get_state()[0]

            # Fitness is some function of the score and the number of moves
            # It's good to have a fitness function that is always positive
            # and increases as the score increases

            genome.fitness = game.get_fitness()

    # Run the NEAT evolution process
    winner = population.run(eval_genomes, 1000)

    # Save the winning genome
    with open('winner_genome.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "ai", "config", "neat_config.txt")
    run_neat(config_path)
