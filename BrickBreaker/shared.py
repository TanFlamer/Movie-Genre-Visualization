import random
import numpy as np

import result
from widgets import *
from algo import QLearning
from game import Game


def display_init_settings(root, init_settings):
    win = Frame(root)

    for x in range(7): win.grid_columnconfigure(x, weight=1)
    for y in range(22): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Game Settings", 3, 0)
    create_label(win, "Parameter Settings", 3, 11)

    vertical_lines(win, 1, range(0, 7, 2), 10)
    vertical_lines(win, 12, range(0, 7, 2), 7)

    horizontal_lines(win, range(1, 11, 3), 7)
    horizontal_lines(win, range(12, 19, 3), 7)

    game_settings, parameter_settings = init_settings[:8], init_settings[8:]

    game_labels = ["Seed", "Brick Placement", "Rows", "Columns", "Ball Speed", "Paddle Speed", "Game Mode", "Episodes"]
    game_data = zip(game_labels, game_settings)

    for index, data in enumerate(game_data):
        place_labels(win, list(data), get_col(index), get_row(index, 2))

    parameter_labels = ["Q-Table", "State", "Action", "Random", "Opposition", "Reward"]
    parameter_data = zip(parameter_labels, parameter_settings)

    for index, data in enumerate(parameter_data):
        place_labels(win, list(data), get_col(index), get_row(index, 13))

    next_button = create_button(win, "Next", 3, 19)

    return win, next_button


def display_exp_settings(root, exp_settings, results):
    win = Frame(root)

    for x in range(7): win.grid_columnconfigure(x, weight=1)
    for y in range(24): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Experiment Settings", 3, 0)
    create_label(win, "Results", 3, 11)

    vertical_lines(win, 1, range(0, 7, 2), 10)
    vertical_lines(win, 12, range(0, 7, 2), 10)

    horizontal_lines(win, range(1, 11, 3), 7)
    horizontal_lines(win, range(12, 22, 3), 7)

    exp_labels = ["Learning Rate", "Explore Rate", "Discount Factor", "New Run", "Confidence", "Mean", "STD", "Old Run"]
    exp_settings = join_parameters(exp_settings[:9]) + exp_settings[9:]
    exp_data = zip(exp_labels, exp_settings)

    for index, data in enumerate(exp_data):
        place_labels(win, list(data), get_col(index), get_row(index, 2))

    results_label = ["Mean", "STD", "Median", "IQR", "Max", "Min", "Difference", "Failed"]
    results_data = zip(results_label, results)

    for index, data in enumerate(results_data):
        place_labels(win, list(data), get_col(index), get_row(index, 13))

    back_button = create_button(win, "Back", 1, 22)
    done_button = create_button(win, "Done", 5, 22)

    return win, back_button, done_button


def display_tune_settings(root, tune_settings, best_chromosomes):
    win = Frame(root)

    length = len(best_chromosomes)

    for x in range(7): win.grid_columnconfigure(x, weight=1)
    for y in range(length + 18): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Tuning Settings", 3, 0)
    create_label(win, "Hyper-parameters", 3, 11)

    vertical_lines(win, 1, range(0, 7, 2), 10)
    vertical_lines(win, 12, range(0, 7, 2), length + 4)

    horizontal_lines(win, range(1, 11, 3), 7)
    horizontal_lines(win, [12, 14, length + 15], 7)

    tune_labels = ["Crossover Rate", "Mutation Rate", "Single / Double", "Tournament / Roulette",
                   "Population", "Elite", "Generation", "Best"]
    tune_settings[2:4] = get_inverse(tune_settings[2:4])
    tune_data = zip(tune_labels, tune_settings)

    for index, data in enumerate(tune_data):
        place_labels(win, list(data), get_col(index), get_row(index, 2))

    hyper_parameters = ["Learning Rate", "Explore Rate", "Discount Factor"]
    place_columns(win, 13, hyper_parameters)

    joined_chromosomes = [join_parameters(chromosome) for chromosome in best_chromosomes]
    for index, chromosome in enumerate(joined_chromosomes):
        place_columns(win, index + 15, chromosome)

    back_button = create_button(win, "Back", 1, length + 16)
    done_button = create_button(win, "Done", 5, length + 16)

    return win, back_button, done_button


def display_exp_results(root, init_settings, exp_settings, results):
    # Load frames
    init_frame, next_button = display_init_settings(root, init_settings)
    exp_frame, back_button, done_button = display_exp_settings(root, exp_settings, results)

    # Load buttons
    next_button.configure(command=lambda: [exp_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    back_button.configure(command=lambda: [init_frame.pack(fill='both', expand=1), exp_frame.pack_forget()])
    done_button.configure(command=lambda: root.destroy())

    # Load frame and run
    init_frame.pack(fill='both', expand=1)
    root.mainloop()


def display_tune_results(root, init_settings, tune_settings, best_chromosomes):
    # Load frames
    init_frame, next_button = display_init_settings(root, init_settings)
    tune_frame, back_button, done_button = display_tune_settings(root, tune_settings, best_chromosomes)

    # Load buttons
    next_button.configure(command=lambda: [tune_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    back_button.configure(command=lambda: [init_frame.pack(fill='both', expand=1), tune_frame.pack_forget()])
    done_button.configure(command=lambda: root.destroy())

    # Load frame and run
    init_frame.pack(fill='both', expand=1)
    root.mainloop()


def run_brick_breaker(root, initial_settings, hyper_parameters, bricks, runs, dimensions, exclude_failure=False):
    # Unpack settings
    game_settings, parameter_settings = initial_settings[:4], initial_settings[4:]
    # Save results
    results = []
    # Load Q-Learning
    qLearning = QLearning(parameter_settings, hyper_parameters, dimensions)
    # Create game
    game = Game(root, game_settings, bricks, qLearning, runs, results, dimensions, exclude_failure)
    game.pack(fill='both', expand=1)
    # Start game
    game.mainloop()
    # Return results
    return results


def run_experiment(root, initial_settings, experiment_settings, dimensions):
    # Unpack settings
    hyper_parameters, result_settings = experiment_settings[:9], experiment_settings[9:]
    # Load bricks
    bricks = get_bricks(initial_settings)
    # Get data
    runs = result_settings[0]
    # Run Brick Breaker
    results = run_brick_breaker(root, initial_settings[4:], hyper_parameters, bricks, runs, dimensions, True)
    # Print results
    exp_results = result.Results(results, runs, result_settings[1:]).exp_results
    # Display results
    display_exp_results(root, initial_settings, experiment_settings, exp_results)


def get_bricks(initial_settings):
    # Set seed
    seed = initial_settings[0]
    random.seed(seed)
    np.random.seed(seed)
    # Get bricks
    brick_settings = initial_settings[1:4]
    return Bricks(brick_settings).bricks


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
