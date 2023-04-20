from ai.neat_evo_process import run_neat
from ai.wumpus_world_ai import run_game_with_trained_ai
import os

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(
        local_dir, "ai", "config", "neat_config.txt")

    winner_genome_path = os.path.join(
        local_dir, "winner_genome.pkl")

    run_neat(config_path)
    # run_game_with_trained_ai(winner_genome_path, config_path)
