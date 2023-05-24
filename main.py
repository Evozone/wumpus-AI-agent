from ai.neat_evo_process import run_neat
from ai.wumpus_world_ai import run_game_with_trained_ai
from game.wumpus_world import run_game_with_human

import os

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(
        local_dir, "ai", "config", "neat_config.txt")

    winner_genome_path = os.path.join(
        local_dir, "winner_genome.pkl")

    # Choose one of the following to run
    print("Choose one of the following to run:")
    print("1. Human play")
    print("2. AI play")
    print("3. Train AI")

    choice = -1

    while choice < 1 or choice > 3:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please try again.")

    if choice == 1:
        run_game_with_human()
    elif choice == 2:
        run_game_with_trained_ai(winner_genome_path, config_path)
    elif choice == 3:
        run_neat(config_path)
