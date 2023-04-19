from ai.neat_evo_process import run_neat
import os

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(
        local_dir, "ai", "config", "neat_config.txt")
    run_neat(config_path)
