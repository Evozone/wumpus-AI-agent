# Wumpus AI Agent

<details>
  <summary>Table of Contents</summary> 

  This is a Wumpus World game with an AI agent that plays it. The game is based on the classic Wumpus World game, where the player navigates a maze-like cave system to find gold while avoiding deadly pits and the Wumpus monster.

- [Wumpus AI Agent](#wumpus-ai-agent)
  - [Specifications](#specifications)
  - [Installation](#installation)
  - [Usage](#usage)
      - [Playing the game yourself](#playing-the-game-yourself)
      - [Watching the AI play](#watching-the-ai-play)
      - [Training the AI](#training-the-ai)
  - [Contributing](#contributing)
  - [Project Contributors](#project-contributors)
</details>

## Specifications

- The game is played on a 4x4 grid of rooms (traditional Wumpus World is 4x4, but you can change this if you want).
- This project has both a human playable version and an AI agent that plays the game.
- Currently only a CLI version is available, but a GUI version is planned for the future.

## Installation
To install the game, follow these steps:
1. Fork the repository
2. Clone the repository: `git clone https://github.com/your-username/wumpus_AI_agent.git`
3. Navigate to the project directory: `cd wumpus_AI_agent`
4. Install the dependencies: `pip install -r requirements.txt`

To learn more about forking and cloning repositories, see [this article](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) on GitHub.

## Usage

- Run the command `python.exe main.py` in the project root to start the application.
- Follow the on-screen instructions to either
  1. Play the game yourself
  2. Watch the AI agent play the game
  3. Train the AI agent according to your own specifications

#### Playing the game yourself

- The instructions for playing the game are displayed on-screen, and are pretty self-explanatory.

#### Watching the AI play

- The AI agent cannot be watched until it has been trained.
- If there is a trained AI agent available, then a `winner_genome.pkl` file will be present in the root directory.
- If there is no trained AI agent available, then read [Training the AI](#training-the-ai) to learn how to train the AI agent, and generate a `winner_genome.pkl` file.

#### Training the AI

- The AI agent is trained using [NEAT](https://neat-python.readthedocs.io/en/latest/).
- The training parameters can be changed in the `ai/config/neat_config.txt` file.
- More information about the NEAT configuration file can be found [here](https://neat-python.readthedocs.io/en/latest/config_file.html).
- To change the number of generations the AI agent is trained for, change the `GENERATIONS` parameter in the `ai/neat_evo_process.py` file.
```python
...agent as ai_agent
import game.game as WuGame

# Number of generations to run the NEAT evolution process
GENERATIONS = 300

def run_neat(config_f...
```
- To train the AI agent, run the command `python.exe main.py` in the project root.
  - Then select the option to train the AI agent.
  - Depending on the number of generations specified, the training process may take a while.
  - Here's an example of what the training process looks like:

```
   ****** Running generation 10 ******

Population's average fitness: -1103.15000 stdev: 64.57411
Best fitness: -1010.00000 - size: (10, 4) - species 1 - id 4994
Average adjusted fitness: 0.810
Mean genetic distance 2.058, standard deviation 0.305
Population of 500 members in 1 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1   10   500  -1010.0    0.810    10
Total extinctions: 0
Generation time: 0.098 sec (0.102 average)

 ****** Running generation 11 ******

Population's average fitness: -1196.99000 stdev: 203.35683
Best fitness: -1010.00000 - size: (10, 4) - species 1 - id 4994
Average adjusted fitness: 0.635
Mean genetic distance 2.114, standard deviation 0.216
Population of 500 members in 1 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1   11   500  -1010.0    0.635    11
Total extinctions: 0
Generation time: 0.130 sec (0.105 average)

  ****** Running generation 12 ******
  (And so on...)
```

At the end of the training process, a `winner_genome.pkl` file will be generated in the root directory. You may then proceed to [Watching the AI play](#watching-the-ai-play).

## Contributing
If you would like to contribute to the project, please follow these steps:
1. Fork the repository
2. Create a new branch: `git checkout -b my-new-feature`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

To learn more about forking and cloning repositories, see [this article](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) on GitHub.

To learn more about creating pull requests, see [this article](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) on GitHub.

## Project Contributors

| <a href="https://github.com/TheBrahmnicBoy"><img alt="Bhargav Modak" src="https://avatars.githubusercontent.com/u/82528318?v=4" width="130px;"><br><sub><b>Bhargav Modak</b></sub></a> | <a href="https://github.com/vishal-codes"><img alt="Vishal Shinde" src="https://avatars.githubusercontent.com/u/79784161" width="130px;"><br><sub><b>Vishal Shinde</b></sub></a> |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                 <a href="mailto:thebrahmnicboy@gmail.com">E-Mail ↗️</a>                                                                 |                                                                 <a href="mailto:itsvishal2417.com">E-Mail ↗️</a>                                                                  |
|           [![Twitter](https://img.shields.io/badge/twitter-%2300acee.svg?&style=for-the-badge&logo=twitter&logoColor=white&alt=twitter)](https://twitter.com/thebrahmnicboy)           |          [![Twitter](https://img.shields.io/badge/twitter-%2300acee.svg?&style=for-the-badge&logo=twitter&logoColor=white&alt=twitter)](https://twitter.com/vishaltwts)          |