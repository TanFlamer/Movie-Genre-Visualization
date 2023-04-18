# Import the required Libraries
from tkinter import *
from tkinter import ttk
import game


def vertical_lines(root, first_row, last_column, length):
    for col in [0, 2, last_column]:
        ttk.Separator(root, orient=VERTICAL).grid(column=col, row=first_row, rowspan=length, sticky="NS")


def horizontal_lines(root, row_list, length):
    for row in row_list:
        ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=row, columnspan=length, sticky="EW")


def create_label(root, text, column, row, span=None):
    Label(root, anchor="center", text=text, font=("Arial", 10, "bold"))\
        .grid(column=column, row=row, columnspan=1 if span is None else span)


def place_labels(root, text_list, column, row_list):
    for (text, row) in zip(text_list, row_list):
        create_label(root, text, column, row)


def create_entry(root, string_var, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    entry = Entry(root, textvariable=string_var, font=("Arial", 10), width=15)
    entry.grid(column=column, row=row)
    return entry


def create_button(root, text, column, row):
    button = Button(root, text=text)
    button.grid(column=column, row=row)
    return button


def create_checkbutton(root, text, int_var, column, row):
    checkbutton = Checkbutton(root, text=text, variable=int_var)
    checkbutton.grid(column=column, row=row)
    return int_var


def create_option_menu(root, var, options_list, column, row):
    option_menu = OptionMenu(root, var, *options_list)
    option_menu.grid(column=column, row=row)
    return var


def create_spinbox(root, from_, to, increment, num_var, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    spinbox = Spinbox(root, from_=from_, to=to, increment=increment, textvariable=num_var, width=5)
    spinbox.grid(column=column, row=row)
    return spinbox


def create_scale(root, from_, to, int_var, column, row):
    scale = Scale(root, from_=from_, to=to, variable=int_var, orient=HORIZONTAL, showvalue=False, length=100)
    scale.grid(column=column, row=row, columnspan=2)
    return scale


def single_spinbox_scale(root, from_, to, initial, factor, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    double_var = DoubleVar(value=initial / factor)

    scale = create_scale(root, from_, to, IntVar(value=initial), column, row)
    scale.configure(command=lambda val: double_var.set(int(val) if factor == 1 else int(val) / factor))

    spinbox = create_spinbox(root, from_ / factor, to / factor, 1 / factor, double_var, column + 2, row)
    spinbox.configure(command=lambda: scale.set(double_var.get() * factor))

    return spinbox


def double_spinbox_scale(root, column, row):
    def inverse_string(string): return 100 - int(string)
    def inverse_num(double): return 1 - double

    var1 = DoubleVar(value=0.5)
    var2 = DoubleVar(value=0.5)

    spinbox1 = create_spinbox(root, 0, 1, 0.01, var1, column + 1, row)
    spinbox1.configure(command=lambda: [scale.set(var1.get() * 100), var2.set(inverse_num(var1.get()))])

    scale = create_scale(root, 0, 100, IntVar(value=50), column + 2, row)
    scale.configure(command=lambda val: [var1.set(int(val) / 100), var2.set(inverse_string(val) / 100)])

    spinbox2 = create_spinbox(root, 0, 1, 0.01, var2, column + 4, row)
    spinbox2.configure(command=lambda: [scale.set(inverse_num(var2.get()) * 100), var1.set(inverse_num(var2.get()))])

    return spinbox1


def parameter_tuning(root, column, row):
    labels = ["Initial", "Final", "Step"]
    rows = [row - 1, row, row + 1]
    place_labels(root, labels, column, rows)

    spinbox1 = single_spinbox_scale(root, 0, 100, 50, 100, column + 1, row - 1)
    spinbox2 = single_spinbox_scale(root, 0, 100, 50, 100, column + 1, row)
    spinbox3 = single_spinbox_scale(root, 0, 10, 5, 1000, column + 1, row + 1)

    return [spinbox1, spinbox2, spinbox3]


def get_values(var_list):
    values = [var.get() for var in var_list]
    return [process_value(value) for value in values]


def process_value(value):
    # Value is already int or string
    if isinstance(value, int) or not value.replace(".", "").isnumeric():
        return value
    else:
        return int(value) if value.isnumeric() else float(value)


def initial_settings(root):
    win = Frame(root)

    for x in range(5): win.grid_columnconfigure(x, weight=1)
    for y in range(36): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Game Settings", 2, 0)
    create_label(win, "Parameter Settings", 2, 18)

    vertical_lines(win, 1, 4, 17)
    vertical_lines(win, 19, 4, 15)

    horizontal_lines(win, range(1, 18, 2), 5)
    horizontal_lines(win, range(19, 34, 2), 5)

    game_labels = ["Seed", "Ball Speed", "Paddle Speed", "Rows", "Columns", "Brick Placement", "Game Mode", "Episodes"]
    place_labels(win, game_labels, 1, range(2, 17, 2))

    parameter_labels = ["Q-Table", "State Type", "State Num", "Action", "Random", "Opposition", "Reward"]
    place_labels(win, parameter_labels, 1, range(20, 33, 2))

    # Option Lists
    brick_types = ["Row", "Column", "Random"]
    state_types = ["-", "Paddle", "Ball", "Paddle + Ball"]
    reward_types = ["X-Distance", "X-Distance (Center)", "XY-Distance", "Time-Based", "Constant Reward"]
    factors_list = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]

    # Game Settings
    seed = create_entry(win, StringVar(value="20313854"), 3, 2)
    ball_speed = create_spinbox(win, 1, 10, 1, IntVar(value=5), 3, 4)
    paddle_speed = create_spinbox(win, 1, 20, 1, IntVar(value=10), 3, 6)
    brick_rows = create_spinbox(win, 1, 10, 1, IntVar(value=5), 3, 8)
    bricks_in_row = create_option_menu(win, IntVar(value=8), factors_list, 3, 10)
    brick_placement = create_option_menu(win, StringVar(value="Row"), brick_types, 3, 12)
    game_mode = create_checkbutton(win, "Inverted", IntVar(value=0), 3, 14)
    episodes = create_spinbox(win, 100, 500, 1, IntVar(value=200), 3, 16)
    game_settings = [seed, ball_speed, paddle_speed, brick_rows, bricks_in_row, brick_placement, game_mode, episodes]

    # Parameter Settings
    q_table = create_spinbox(win, 1, 10, 1, IntVar(value=1), 3, 20)
    state_type = create_option_menu(win, StringVar(value="-"), state_types, 3, 22)
    state_num = create_spinbox(win, 1, 10, 1, IntVar(value=2), 3, 24)
    action = create_spinbox(win, 2, 3, 1, IntVar(value=2), 3, 26)
    random = create_spinbox(win, 0, 10, 1, IntVar(value=0), 3, 28)
    opposition = create_checkbutton(win, "Include", IntVar(value=0), 3, 30)
    reward = create_option_menu(win, StringVar(value="X-Distance"), reward_types, 3, 32)
    parameter_settings = [q_table, state_type, state_num, action, random, opposition, reward]

    # Buttons
    total_settings = game_settings + parameter_settings
    tuning_button = create_button(win, "Tuning", 1, 34)
    experiment_button = create_button(win, "Experiment", 3, 34)

    return win, total_settings, tuning_button, experiment_button


def experiment_settings(root):
    win = Frame(root)

    for x in range(8): win.grid_columnconfigure(x, weight=1)
    for y in range(20): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Experiment Settings", 3, 0, 2)
    vertical_lines(win, 1, 7, 17)
    horizontal_lines(win, range(1, 18, 4), 8)

    labels = ["Learning Rate", "Explore Rate", "Discount Factor", "Settings"]
    place_labels(win, labels, 1, range(3, 16, 4))

    # Hyper-parameters
    learning_rate = parameter_tuning(win, 3, 3)
    explore_rate = parameter_tuning(win, 3, 7)
    discount_factor = parameter_tuning(win, 3, 11)
    hyper_parameters = learning_rate + explore_rate + discount_factor

    # Other Settings
    confidence = single_spinbox_scale(win, 500, 999, 900, 1000, 4, 14, "Confidence")
    new_runs = create_spinbox(win, 30, 100, 1, IntVar(value=30), 4, 15, "New Runs")
    mean = create_entry(win, StringVar(value="0.00"), 6, 15, "Mean")
    old_runs = create_spinbox(win, 30, 100, 1, IntVar(value=30), 4, 16, "Old Runs")
    std = create_entry(win, StringVar(value="0.00"), 6, 16, "STD")
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

    create_label(win, "Hyperparameter Tuning", 3, 0, 2)
    vertical_lines(win, 1, 7, 12)
    horizontal_lines(win, list(range(1, 10, 2)) + [12], 8)

    labels = ["Crossover", "Mutation", "Single/Double", "Tournament/Roulette", "Experiment", "Settings"]
    place_labels(win, labels, 1, list(range(2, 11, 2)) + [11])

    # Scale Settings
    crossover_rate = single_spinbox_scale(win, 0, 100, 50, 100, 4, 2, "Rate")
    mutation_rate = single_spinbox_scale(win, 0, 100, 50, 100, 4, 4, "Rate")
    single_double = double_spinbox_scale(win, 2, 6)
    roulette_tournament = double_spinbox_scale(win, 2, 8)
    scale_settings = [crossover_rate, mutation_rate, single_double, roulette_tournament]

    # Experiment Settings
    population = create_spinbox(win, 2, 100, 2, IntVar(value=10), 4, 10, "Population")
    tour_size = create_spinbox(win, 1, 100, 1, IntVar(value=3), 6, 10, "Tournament")
    generation = create_spinbox(win, 1, 1000, 1, IntVar(value=100), 4, 11, "Generation")
    best = create_spinbox(win, 1, 10, 1, IntVar(value=10), 6, 11, "Best")
    other_settings = [population, tour_size, generation, best]

    # Buttons
    total_settings = scale_settings + other_settings
    back_button = create_button(win, "Back", 3, 13)
    start_button = create_button(win, "Start", 4, 13)

    return win, total_settings, back_button, start_button


if __name__ == "__main__":
    # Create an instance of Tkinter frame
    main = Tk()

    # Set the geometry of Tkinter frame
    main.title("Settings")
    main.geometry("600x450")
    main.grid()

    # Get frames and data
    init_frame, init_settings, tune_button, exp_button = initial_settings(main)
    exp_frame, exp_settings, exp_back, exp_start = experiment_settings(main)
    tune_frame, tune_settings, tune_back, tune_start = experiment_tuning(main)

    # Link buttons
    tune_button.configure(command=lambda: [tune_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    exp_button.configure(command=lambda: [exp_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    exp_back.configure(command=lambda: [init_frame.pack(fill='both', expand=1), exp_frame.pack_forget()])
    tune_back.configure(command=lambda: [init_frame.pack(fill='both', expand=1), tune_frame.pack_forget()])
    exp_start.configure(command=lambda: [game.brick_breaker(main).pack(fill='both', expand=1), exp_frame.pack_forget()])
    tune_start.configure(command=lambda: [print(get_values(exp_settings)), print(get_values(tune_settings))])

    # Load frame and run
    init_frame.pack(fill='both', expand=1)
    main.mainloop()
    print("lol")
