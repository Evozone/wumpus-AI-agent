import pickle
import neat
import os

import ai.ai_agent as ai_agent
import game.game as WuGame


def run_game_with_trained_ai(winner_genome_path, config_file):
    # Load the winner genome
    with open(winner_genome_path, 'rb') as input_file:
        winner_genome = pickle.load(input_file)

    # Load the NEAT configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create a neural network from the winner genome
    net = neat.nn.FeedForwardNetwork.create(winner_genome, config)

    # Create the AI agent with the trained neural network
    agent = ai_agent.MyAgent(net)

    # Run the game with the trained AI agent
    seed = WuGame.generate_seed()
    game = WuGame.Game(seed)
    game.run_game_with_ai(agent, step_by_step=True)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    winner_genome_path = os.path.join(local_dir, "winner_genome.pkl")
    config_path = os.path.join(
        local_dir, "ai", "config", "neat_config.txt")
    run_game_with_trained_ai(winner_genome_path, config_path)
