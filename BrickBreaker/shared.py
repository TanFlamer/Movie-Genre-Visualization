import random
import numpy as np

from Coursework.BrickBreaker import result
from Coursework.BrickBreaker.algo import QLearning
from Coursework.BrickBreaker.game import Game


def get_bricks(initial_settings):
    # Set seed
    seed = initial_settings[0]
    random.seed(seed)
    np.random.seed(seed)
    # Get bricks
    brick_settings = initial_settings[1:4]
    return Bricks(brick_settings).bricks


def run_brick_breaker(root, initial_settings, hyper_parameters, bricks, runs, dimensions):
    # Unpack settings
    game_settings, parameter_settings = initial_settings[:4], initial_settings[4:]
    # Save results
    results = []
    # Load Q-Learning
    qLearning = QLearning(parameter_settings, hyper_parameters, dimensions)
    # Create game
    game = Game(root, game_settings, bricks, qLearning, runs, results, dimensions)
    game.pack(fill='both', expand=1)
    # Start game
    game.mainloop()
    # Return results
    return results


def run_experiment(root, initial_settings, experiment_settings, dimensions):
    # Unpack settings
    [hyper_parameters, result_settings] = [experiment_settings[:9], experiment_settings[9:]]
    # Load bricks
    bricks = get_bricks(initial_settings)
    # Get data
    [runs, episodes] = [result_settings[0], initial_settings[7]]
    # Run Brick Breaker
    results = run_brick_breaker(root, initial_settings[4:], hyper_parameters, bricks, runs, dimensions)
    # Print results
    result.Results(results, episodes, result_settings[1:])
    # Close program
    root.destroy()


class Bricks:
    def __init__(self, bricks_data):
        # Unpack data
        [self.brick_placement, self.brick_rows, self.bricks_in_row] = bricks_data
        self.bricks = []
        self.generate_bricks()

    def generate_bricks(self):
        for y in range(self.brick_rows):
            brick_row = []
            for x in range(self.bricks_in_row):
                brick_row.append(self.brick_type(x, y))
            self.bricks.append(brick_row)

    def brick_type(self, x, y):
        if self.brick_placement == "Random":
            return random.randint(1, 3)
        else:
            point = y if self.brick_placement == "Row" else x
            return 3 - (point % 3)
