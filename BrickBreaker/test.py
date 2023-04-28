# Import the required Libraries
from Coursework.BrickBreaker.gene import Genetic
from Coursework.BrickBreaker.shared import run_experiment
from widgets import *


def initial_settings(root):
    win = Frame(root)

    for x in range(5): win.grid_columnconfigure(x, weight=1)
    for y in range(34): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Game Settings", 2, 0)
    create_label(win, "Parameter Settings", 2, 18)

    vertical_lines(win, 1, [0, 2, 4], 17)
    vertical_lines(win, 19, [0, 2, 4], 13)

    horizontal_lines(win, range(1, 18, 2), 5)
    horizontal_lines(win, range(19, 32, 2), 5)

    game_labels = ["Seed", "Brick Placement", "Rows", "Columns", "Ball Speed", "Paddle Speed", "Game Mode", "Episodes"]
    place_labels(win, game_labels, 1, range(2, 17, 2))

    parameter_labels = ["Q-Table", "State", "Action", "Random", "Opposition", "Reward"]
    place_labels(win, parameter_labels, 1, range(20, 31, 2))

    # Option Lists
    brick_types = ["Row", "Column", "Random"]
    random_types = ["None", "Normal", "Uniform"]
    reward_types = ["Constant", "Time-Based", "X-Distance", "X-Distance(Center)", "XY-Distance"]
    factors_list = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]

    # Game Settings
    seed = create_entry(win, StringVar(value="20313854"), 3, 2)
    brick_placement = create_option_menu(win, StringVar(value="Row"), brick_types, 3, 4)
    brick_rows = create_spinbox(win, 1, 6, 1, IntVar(value=3), 3, 6)
    bricks_in_row = create_option_menu(win, IntVar(value=8), factors_list, 3, 8)
    ball_speed = create_spinbox(win, 1, 10, 1, IntVar(value=5), 3, 10)
    paddle_speed = create_spinbox(win, 5, 15, 1, IntVar(value=10), 3, 12)
    game_mode = create_checkbutton(win, "Inverted", IntVar(value=0), 3, 14)
    episodes = create_spinbox(win, 100, 200, 1, IntVar(value=100), 3, 16)
    game_settings = [seed, brick_placement, brick_rows, bricks_in_row, ball_speed, paddle_speed, game_mode, episodes]

    # Parameter Settings
    q_table = create_spinbox(win, 1, 5, 1, IntVar(value=1), 3, 20)
    state = create_spinbox(win, 1, 10, 1, IntVar(value=8), 3, 22)
    action = create_spinbox(win, 2, 3, 1, IntVar(value=2), 3, 24)
    random = create_option_menu(win, StringVar(value="None"), random_types, 3, 26)
    opposition = create_checkbutton(win, "Include", IntVar(value=0), 3, 28)
    reward = create_option_menu(win, StringVar(value="X-Distance(Center)"), reward_types, 3, 30)
    parameter_settings = [q_table, state, action, random, opposition, reward]

    # Buttons
    total_settings = game_settings + parameter_settings
    tuning_button = create_button(win, "Tuning", 1, 32)
    experiment_button = create_button(win, "Experiment", 3, 32)

    return win, total_settings, tuning_button, experiment_button


def experiment_settings(root):
    win = Frame(root)

    for x in range(8): win.grid_columnconfigure(x, weight=1)
    for y in range(20): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Experiment Settings", 3, 0, 2)
    vertical_lines(win, 1, [0, 2, 7], 17)
    horizontal_lines(win, range(1, 18, 4), 8)

    labels = ["Learning Rate", "Explore Rate", "Discount Factor", "Settings"]
    place_labels(win, labels, 1, range(3, 16, 4))

    # Hyper-parameters
    learning_rate = parameter_tuning(win, 90, 10, 10, 3, 3)
    explore_rate = parameter_tuning(win, 50, 1, 10, 3, 7)
    discount_factor = parameter_tuning(win, 90, 99, 1, 3, 11)
    hyper_parameters = learning_rate + explore_rate + discount_factor

    # Other Settings
    confidence = single_spinbox_scale(win, 500, 999, 990, 1000, 4, 14, "Confidence")
    new_runs = create_spinbox(win, 30, 100, 1, IntVar(value=30), 4, 15, "New Runs")
    mean = create_entry(win, StringVar(value="45.63"), 6, 15, "Mean")
    old_runs = create_spinbox(win, 30, 100, 1, IntVar(value=30), 4, 16, "Old Runs")
    std = create_entry(win, StringVar(value="1.40"), 6, 16, "STD")
    other_settings = [new_runs, confidence, mean, std, old_runs]

    # Buttons
    total_settings = hyper_parameters + other_settings
    back_button = create_button(win, "Back", 3, 18)
    start_button = create_button(win, "Start", 4, 18)

    return win, total_settings, back_button, start_button


def experiment_tuning(root):
    win = Frame(root)

    for x in range(8): win.grid_columnconfigure(x, weight=1)
    for y in range(15): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Hyperparameter Settings", 3, 0, 2)
    vertical_lines(win, 1, [0, 2, 7], 12)
    horizontal_lines(win, list(range(1, 10, 2)) + [12], 8)

    labels = ["Crossover", "Mutation", "Single / Double", "Tournament / Roulette", "Other", "Settings"]
    place_labels(win, labels, 1, list(range(2, 11, 2)) + [11])

    # Scale Settings
    crossover_rate = single_spinbox_scale(win, 0, 100, 75, 100, 4, 2, "Rate")
    mutation_rate = single_spinbox_scale(win, 0, 100, 5, 100, 4, 4, "Rate")
    single_double = double_spinbox_scale(win, 2, 6)
    roulette_tournament = double_spinbox_scale(win, 2, 8)
    scale_settings = [crossover_rate, mutation_rate, single_double, roulette_tournament]

    # Experiment Settings
    population = create_spinbox(win, 10, 100, 2, IntVar(value=10), 4, 10, "Population")
    elite = create_spinbox(win, 0, 10, 2, IntVar(value=2), 6, 10, "Elite")
    generation = create_spinbox(win, 1, 100, 1, IntVar(value=50), 4, 11, "Generation")
    best = create_spinbox(win, 1, 10, 1, IntVar(value=10), 6, 11, "Best")
    other_settings = [population, elite, generation, best]

    # Buttons
    total_settings = scale_settings + other_settings
    back_button = create_button(win, "Back", 3, 13)
    start_button = create_button(win, "Start", 4, 13)

    return win, total_settings, back_button, start_button


def run_main():
    # Create an instance of Tkinter frame
    main = Tk()

    # Set the geometry of Tkinter frame
    main.title("Brick Breaker")
    main.geometry("600x450")

    # Set dimensions
    dimensions = [600, 450]

    # Get frames and data
    init_frame, init_settings, tune_button, exp_button = initial_settings(main)
    exp_frame, exp_settings, exp_back, exp_start = experiment_settings(main)
    tune_frame, tune_settings, tune_back, tune_start = experiment_tuning(main)

    # Link buttons
    tune_button.configure(command=lambda: [tune_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    exp_button.configure(command=lambda: [exp_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    exp_back.configure(command=lambda: [init_frame.pack(fill='both', expand=1), exp_frame.pack_forget()])
    tune_back.configure(command=lambda: [init_frame.pack(fill='both', expand=1), tune_frame.pack_forget()])
    exp_start.configure(command=lambda: [exp_frame.pack_forget(), run_experiment(
        main, get_values(init_settings), get_values(exp_settings), dimensions)])
    tune_start.configure(command=lambda: [tune_frame.pack_forget(), Genetic(
        main, get_values(init_settings), get_values(tune_settings), dimensions)])

    # Load frame and run
    init_frame.pack(fill='both', expand=1)
    main.mainloop()
