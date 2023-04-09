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

    create_label(win, "Hyperparameters", 4, 6, 2)
    create_checkbutton(win, "Tuning", IntVar(value=0), 6, 6)

    line_horizontal(win, 0, 7, 11)

    line_vertical(win, 1, 7, 9)
    create_label(win, "Initial", 3, 8)
    line_vertical(win, 5, 7, 9)
    create_label(win, "Final", 7, 8)
    line_vertical(win, 9, 7, 9)
    create_label(win, "Step", 10, 8)

    line_horizontal(win, 0, 9, 11)

    learning_rate = Hyperparameter(win, 10, "Learning")

    line_horizontal(win, 0, 11, 11)

    explore_rate = Hyperparameter(win, 12, "Explore")

    line_horizontal(win, 0, 13, 11)

    discount_factor = Hyperparameter(win, 14, "Discount")

    line_horizontal(win, 0, 15, 11)

    create_button(win, "Enter", 5, 16)

    win.mainloop()

# Hyperparameters
# learning_rate = Hyperparameter(win, 0, "Learning Rate")
# discount_factor = Hyperparameter(win, 1, "Discount Factor")
# explore_rate = Hyperparameter(win, 2, "Explore Rate")
