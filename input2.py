# Import the required Libraries
from tkinter import *
from tkinter import ttk


def create_label(root, text, column, row, span=None):
    label = Label(root, anchor="center", text=text, font=("Arial", 10, "bold"))
    label.grid(column=column, row=row, columnspan=1 if span is None else span)
    return label


def create_spinbox(root, from_, to, increment, string_var, column, row):
    spinbox = Spinbox(root, from_=from_, to=to, increment=increment, textvariable=string_var, width=5)
    spinbox.grid(column=column, row=row)
    return spinbox


def create_scale(root, int_var, from_, to, column, row):
    scale = Scale(root, variable=int_var, from_=from_, to=to, orient=HORIZONTAL, showvalue=False, length=100)
    scale.grid(column=column, row=row, columnspan=2)
    return scale


def create_button(root, text, column, row):
    button = Button(root, text=text)
    button.grid(column=column, row=row)
    return button


def create_entry(root, string_var, column, row):
    entry = Entry(root, textvariable=string_var, font=("Arial", 10), width=10)
    entry.grid(column=column, row=row)
    return entry


def create_checkbutton(root, text, variable, column, row):
    checkbutton = Checkbutton(root, text=text, variable=variable)
    checkbutton.grid(column=column, row=row)
    return checkbutton


def create_option_menu(root, string_var, options_list, column, row):
    option_menu = OptionMenu(root, string_var, *options_list)
    option_menu.grid(column=column, row=row)
    return option_menu


def line_horizontal(root, column, row, span):
    line = ttk.Separator(root, orient=HORIZONTAL)
    line.grid(column=column, row=row, columnspan=span, sticky="EW")
    return line


def line_vertical(root, column, row, span):
    line = ttk.Separator(root, orient=VERTICAL)
    line.grid(column=column, row=row, rowspan=span, sticky="NS")
    return line


def spinbox_to_scale(root, from_, to, increment, string_var, scale, column, row):
    spinbox = create_spinbox(root, from_, to, increment, string_var, column, row)
    spinbox.configure(command=lambda: scale.set(float(string_var.get()) * 10))
    return spinbox


def scale_to_spinbox(root, int_var, from_, to, string_var, column, row):
    scale = create_scale(root, int_var, from_, to, column, row)
    scale.configure(command=lambda val: string_var.set(str(int(val) / 10)))
    return scale


class Hyperparameter:
    def __init__(self, root, row, text):
        self.root = root
        self.row = row
        create_label(root, text, 0, row)
        self.initial = self.fill_dict(1000, 2)
        self.final = self.fill_dict(1000, 6)
        self.step = self.add_spinbox()

    def add_spinbox(self):
        return create_spinbox(self.root, 0.0, 1.0, 0.1, StringVar(value="0.5"), 10, self.row)

    def fill_dict(self, value, column):
        dict_ = {}
        int_var = IntVar(value=value / 2)
        string_var = StringVar(value=str(value / 20))
        scale = scale_to_spinbox(self.root, int_var, 0, value, string_var, column, self.row)
        dict_['scale'] = scale
        spinbox = spinbox_to_scale(self.root, 0.0, value / 10, 0.1, string_var, scale, column + 2, self.row)
        dict_['spinbox'] = spinbox
        return dict_


# Seed, Max Episode, Confidence interval, Sample size
if __name__ == "__main__":
    # Create an instance of Tkinter frame
    win = Tk()

    # Set the geometry of Tkinter frame
    win.title("Experiment Settings")
    win.geometry("750x500")
    win.grid()

    for x in range(11): win.grid_columnconfigure(x, weight=1)
    for y in range(20): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Parameters", 5, 0)
    line_horizontal(win, 0, 1, 11)

    # Seed
    create_label(win, "Seed", 0, 2)
    create_entry(win, StringVar(value="20313854"), 1, 2)

    line_vertical(win, 2, 1, 3)

    # Q-table
    create_label(win, "Q-Table", 3, 2)
    create_spinbox(win, 1, 10, 1, StringVar(value="1"), 4, 2)

    line_vertical(win, 5, 1, 3)

    # State Space
    create_label(win, "State", 6, 2)
    create_spinbox(win, 1, 10, 1, StringVar(value="2"), 7, 2)

    line_vertical(win, 8, 1, 3)

    # Action Space
    create_label(win, "Action", 9, 2)
    create_checkbutton(win, "Empty Move", IntVar(value=0), 10, 2)

    line_horizontal(win, 0, 3, 11)

    # Random
    create_label(win, "Random", 0, 4)
    create_spinbox(win, -10, 0, 1, StringVar(value="0"), 1, 4)
    create_label(win, "-", 2, 4)
    create_spinbox(win, 0, 10, 1, StringVar(value="0"), 3, 4)
    create_checkbutton(win, "Randomise", IntVar(value=0), 4, 4)

    line_vertical(win, 5, 3, 3)

    # Opposition Learning
    create_label(win, "Opposition", 6, 4)
    create_checkbutton(win, "Include", IntVar(value=0), 7, 4)

    line_vertical(win, 8, 3, 3)

    # Reward Function
    create_label(win, "Reward", 9, 4)
    option_list = ["Test", "Test1"]
    create_option_menu(win, StringVar(value="Test"), option_list, 10, 4)

    line_horizontal(win, 0, 5, 11)

    # Hyper parameters
    create_label(win, "Hyperparameters", 4, 6, 2)
    create_checkbutton(win, "Tuning", IntVar(value=0), 6, 6)

    line_horizontal(win, 0, 7, 11)

    create_label(win, "Population", 0, 8)
    create_spinbox(win, 1, 20, 1, StringVar(value="10"), 1, 8)

    line_vertical(win, 2, 7, 3)

    create_label(win, "Generations", 3, 8)
    create_spinbox(win, 1, 1000, 1, StringVar(value="100"), 4, 8)

    line_vertical(win, 5, 7, 3)

    create_label(win, "Episodes", 6, 8)
    create_spinbox(win, 1, 200, 1, StringVar(value="100"), 7, 8)

    line_vertical(win, 8, 7, 3)

    create_label(win, "Best", 9, 8)
    create_spinbox(win, 1, 20, 1, StringVar(value="10"), 10, 8)

    line_horizontal(win, 0, 9, 11)

    create_label(win, "Crossover", 0, 10)
    crossover_str = StringVar(value="50")

    crossover_scale = create_scale(win, IntVar(value=50), 0, 100, 1, 10)
    crossover_scale.configure(command=lambda val: crossover_str.set(val))

    crossover_spinbox = create_spinbox(win, 0, 100, 1, crossover_str, 3, 10)
    crossover_spinbox.configure(command=lambda: crossover_scale.set(crossover_str.get()))

    line_vertical(win, 4, 9, 3)

    single_str = StringVar(value="50")
    double_str = StringVar(value="50")

    create_label(win, "Single", 5, 10)

    single_spinbox = create_spinbox(win, 0, 100, 1, single_str, 6, 10)
    single_spinbox.configure(command=lambda: [combined_scale.set(single_str.get()), double_str.set(str(100 - int(single_str.get())))])

    combined_scale = create_scale(win, IntVar(value=50), 0, 100, 7, 10)
    combined_scale.configure(command=lambda val:[single_str.set(val), double_str.set(str(100 - int(val)))])

    double_spinbox = create_spinbox(win, 0, 100, 1, double_str, 9, 10)
    double_spinbox.configure(command=lambda: [combined_scale.set(100 - int(double_str.get())), single_str.set(str(100 - int(double_str.get())))])

    create_label(win, "Double", 10, 10)

    line_horizontal(win, 0, 11, 11)

    create_label(win, "Mutation", 0, 12)
    mutation_str = StringVar(value="50")

    mutation_scale = create_scale(win, IntVar(value=50), 0, 100, 1, 12)
    mutation_scale.configure(command=lambda val: mutation_str.set(val))
    mutation_spinbox = create_spinbox(win, 0, 100, 1, mutation_str, 3, 12)
    mutation_spinbox.configure(command=lambda: mutation_scale.set(mutation_str.get()))

    line_vertical(win, 4, 11, 3)

    tournament_str = StringVar(value="50")
    roulette_str = StringVar(value="50")

    create_label(win, "Tournament", 5, 12)

    tournament_spinbox = create_spinbox(win, 0, 100, 1, tournament_str, 6, 12)
    tournament_spinbox.configure(
        command=lambda: [combined2_scale.set(tournament_str.get()), roulette_str.set(str(100 - int(tournament_str.get())))])

    combined2_scale = create_scale(win, IntVar(value=50), 0, 100, 7, 12)
    combined2_scale.configure(command=lambda val: [tournament_str.set(val), roulette_str.set(str(100 - int(val)))])

    roulette_spinbox = create_spinbox(win, 0, 100, 1, roulette_str, 9, 12)
    roulette_spinbox.configure(command=lambda: [combined2_scale.set(100 - int(roulette_str.get())),
                                              tournament_str.set(str(100 - int(roulette_str.get())))])

    create_label(win, "Roulette", 10, 12)

    line_horizontal(win, 0, 13, 11)

    create_button(win, "Enter", 5, 14)

    win.mainloop()

# Hyperparameters
# learning_rate = Hyperparameter(win, 0, "Learning Rate")
# discount_factor = Hyperparameter(win, 1, "Discount Factor")
# explore_rate = Hyperparameter(win, 2, "Explore Rate")
