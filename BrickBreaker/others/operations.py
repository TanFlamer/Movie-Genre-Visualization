from BrickBreaker.gui.results_gui import display_exp_results
from BrickBreaker.main.brick_breaker import Game
from BrickBreaker.main.q_learning import QLearning
from BrickBreaker.main.result import Results
from BrickBreaker.others.bricks import get_bricks


def run_brick_breaker(root, initial_settings, hyper_parameters, bricks, runs, dimensions, exclude_failure=False):
    # Unpack settings
    game_settings, parameter_settings = initial_settings[:4], initial_settings[4:]
    # Save results
    results = []
    # Load Q-Learning
    qLearning = QLearning(parameter_settings, hyper_parameters, dimensions)
    # Other settings
    other_settings = [dimensions, bricks, runs, exclude_failure]
    # Create game
    game = Game(root, game_settings, other_settings, qLearning, results)
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
    exp_results = Results(results, runs, result_settings[1:]).exp_results
    # Display results
    display_exp_results(root, initial_settings, experiment_settings, exp_results)