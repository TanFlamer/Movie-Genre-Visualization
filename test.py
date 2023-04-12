# Import the required Libraries
from tkinter import *
from tkinter import ttk


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
    entry = Entry(root, textvariable=string_var, font=("Arial", 10), width=10)
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


def create_option_menu(root, string_var, options_list, column, row):
    option_menu = OptionMenu(root, string_var, *options_list)
    option_menu.grid(column=column, row=row)
    return string_var


def create_spinbox(root, from_, to, increment, double_var, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    spinbox = Spinbox(root, from_=from_, to=to, increment=increment, textvariable=double_var, width=5)
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
    def inverse(string): return 100 - int(string)

    var1 = IntVar(value=50)
    var2 = IntVar(value=50)

    spinbox1 = create_spinbox(root, 0, 100, 1, var1, column + 1, row)
    spinbox1.configure(command=lambda: [scale.set(var1.get()), var2.set(inverse(var1.get()))])

    scale = create_scale(root, 0, 100, IntVar(value=50), column + 2, row)
    scale.configure(command=lambda val: [var1.set(val), var2.set(inverse(val))])

    spinbox2 = create_spinbox(root, 0, 100, 1, var2, column + 4, row)
    spinbox2.configure(command=lambda: [scale.set(inverse(var2.get())), var1.set(inverse(var2.get()))])

    return spinbox1


def parameter_tuning(root, column, row):
    labels = ["Initial", "Final", "Step"]
    rows = [row - 1, row, row + 1]
    place_labels(root, labels, column, rows)

    spinbox1 = single_spinbox_scale(root, 0, 1000, 500, 10, column + 1, row - 1)
    spinbox2 = single_spinbox_scale(root, 0, 1000, 500, 10, column + 1, row)
    spinbox3 = single_spinbox_scale(root, 0, 10, 5, 10, column + 1, row + 1)

    return [spinbox1, spinbox2, spinbox3]


def get_values(var_list):
    return [var.get() for var in var_list]


def initial_settings():
    # Create an instance of Tkinter frame
    win = Tk()

    # Set the geometry of Tkinter frame
    win.title("Experiment Settings")
    win.geometry("600x450")
    win.grid()

    for x in range(5): win.grid_columnconfigure(x, weight=1)
    for y in range(32): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Game Settings", 2, 0)
    create_label(win, "Parameter Settings", 2, 14)

    vertical_lines(win, 1, 4, 13)
    vertical_lines(win, 15, 4, 15)

    horizontal_lines(win, range(1, 14, 2), 5)
    horizontal_lines(win, range(15, 30, 2), 5)

    game_labels = ["Ball Speed", "Paddle Speed", "Brick Rows", "Bricks in Row", "Brick Placement", "Game Mode"]
    place_labels(win, game_labels, 1, range(2, 13, 2))

    parameter_labels = ["Seed", "Q-Table", "State", "Action", "Random", "Opposition", "Reward"]
    place_labels(win, parameter_labels, 1, range(16, 29, 2))

    # Option Lists
    option_list_0 = ["Test", "Test1"]
    option_list = ["Test", "Test1"]

    # Game Settings
    ball_speed = create_spinbox(win, 1, 10, 1, StringVar(value="5"), 3, 2)
    paddle_speed = create_spinbox(win, 1, 10, 1, StringVar(value="5"), 3, 4)
    brick_rows = create_spinbox(win, 1, 10, 1, StringVar(value="3"), 3, 6)
    bricks_in_row = create_spinbox(win, 1, 15, 1, StringVar(value="8"), 3, 8)
    brick_placement = create_option_menu(win, StringVar(value="Test"), option_list_0, 3, 10)
    game_mode = create_checkbutton(win, "Inverted", IntVar(value=0), 3, 12)
    game_settings = [ball_speed, paddle_speed, brick_rows, bricks_in_row, brick_placement, game_mode]

    # Parameter Settings
    seed = create_entry(win, StringVar(value="20313854"), 3, 16)
    q_table = create_spinbox(win, 1, 10, 1, StringVar(value="1"), 3, 18)
    state = create_spinbox(win, 1, 10, 1, StringVar(value="2"), 3, 20)
    action = create_checkbutton(win, "Empty Move", IntVar(value=0), 3, 22)
    random = create_spinbox(win, 0, 10, 1, StringVar(value="0"), 3, 24)
    opposition = create_checkbutton(win, "Include", IntVar(value=0), 3, 26)
    reward = create_option_menu(win, StringVar(value="Test"), option_list, 3, 28)
    parameter_settings = [seed, q_table, state, action, random, opposition, reward]

    # Buttons
    total_settings = game_settings + parameter_settings
    tuning_button = create_button(win, "Tuning", 1, 30)
    experiment_button = create_button(win, "Experiment", 3, 30)

    win.mainloop()


def experiment_settings():
    # Create an instance of Tkinter frame
    win = Tk()

    # Set the geometry of Tkinter frame
    win.title("Experiment Settings")
    win.geometry("600x450")
    win.grid()

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
    confidence = single_spinbox_scale(win, 500, 999, 900, 10, 4, 14, "Confidence")
    mean = create_entry(win, StringVar(value="0.00"), 4, 15, "Mean")
    std = create_entry(win, StringVar(value="0.00"), 6, 15, "STD")
    runs = create_spinbox(win, 30, 100, 1, StringVar(value="30"), 4, 16, "Runs")
    episodes = create_spinbox(win, 1, 200, 1, StringVar(value="100"), 6, 16, "Episodes")
    other_settings = [confidence, mean, std, runs, episodes]

    # Buttons
    total_settings = hyper_parameters + other_settings
    back_button = create_button(win, "Back", 3, 18)
    start_button = create_button(win, "Start", 4, 18)

    win.mainloop()


def experiment_tuning():
    # Create an instance of Tkinter frame
    win = Tk()

    # Set the geometry of Tkinter frame
    win.title("Experiment Settings")
    win.geometry("600x450")
    win.grid()

    for x in range(8): win.grid_columnconfigure(x, weight=1)
    for y in range(15): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Hyperparameter Tuning", 3, 0, 2)
    vertical_lines(win, 1, 7, 12)
    horizontal_lines(win, list(range(1, 10, 2)) + [12], 8)

    labels = ["Single/Double", "Tournament/Roulette", "Crossover", "Mutation", "Experiment", "Settings"]
    place_labels(win, labels, 1, list(range(2, 11, 2)) + [11])

    # Scale Settings
    crossover_scale = double_spinbox_scale(win, 2, 2)
    selection_scale = double_spinbox_scale(win, 2, 4)
    crossover_rate = single_spinbox_scale(win, 0, 100, 50, 1, 4, 6, "Rate")
    mutation_rate = single_spinbox_scale(win, 0, 100, 50, 1, 4, 8, "Rate")
    scale_settings = [crossover_scale, selection_scale, crossover_rate, mutation_rate]

    # Experiment Settings
    population = create_spinbox(win, 30, 100, 1, StringVar(value="30"), 4, 10, "Population")
    generation = create_spinbox(win, 1, 200, 1, StringVar(value="100"), 6, 10, "Generation")
    episodes = create_spinbox(win, 100, 200, 1, StringVar(value="100"), 4, 11, "Episodes")
    best = create_spinbox(win, 1, 10, 1, StringVar(value="10"), 6, 11, "Best")
    other_settings = [population, generation, episodes, best]

    # Buttons
    total_settings = scale_settings + other_settings
    back_button = create_button(win, "Back", 3, 13)
    start_button = create_button(win, "Start", 4, 13)

    win.mainloop()


# Seed, Max Episode, Confidence interval, Sample size
if __name__ == "__main__":
    experiment_tuning()
