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


def single_spinbox_scale(root, text, column, row):
    label = create_label(root, text, column, row)
    str_var = StringVar(value="50")

    scale = create_scale(root, IntVar(value=50), 0, 100, column + 1, row)
    scale.configure(command=lambda val: str_var.set(val))

    spinbox = create_spinbox(root, 0, 100, 1, str_var, column + 3, row)
    spinbox.configure(command=lambda: scale.set(str_var.get()))

    return label, scale, spinbox


def double_spinbox_scale(root, text1, text2, column, row):

    def reciprocal(string): return str(100 - int(string))

    label1 = create_label(root, text1, column, row)
    label2 = create_label(root, text2, column + 5, row)

    str1 = StringVar(value="50")
    str2 = StringVar(value="50")

    spinbox1 = create_spinbox(root, 0, 100, 1, str1, column + 1, row)
    spinbox1.configure(command=lambda: [scale.set(str1.get()), str2.set(reciprocal(str1.get()))])

    scale = create_scale(root, IntVar(value=50), 0, 100, column + 2, row)
    scale.configure(command=lambda val: [str1.set(val), str2.set(reciprocal(val))])

    spinbox2 = create_spinbox(root, 0, 100, 1, str2, column + 4, row)
    spinbox2.configure(command=lambda: [scale.set(reciprocal(str2.get())), str1.set(reciprocal(str2.get()))])

    return label1, label2, scale, spinbox1, spinbox2


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
        string_var = StringVar(value=str(value / 20))

        scale = create_scale(self.root, IntVar(value=value / 2), 0, value, column, self.row)
        scale.configure(command=lambda val: string_var.set(str(int(val) / 10)))
        dict_['scale'] = scale

        spinbox = create_spinbox(self.root, 0, value, 0.1, string_var, column + 2, self.row)
        spinbox.configure(command=lambda: scale.set(float(string_var.get()) * 10))
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

    create_label(win, "Max", 6, 8)
    create_spinbox(win, 1, 200, 1, StringVar(value="100"), 7, 8)

    line_vertical(win, 8, 7, 3)

    create_label(win, "Best", 9, 8)
    create_spinbox(win, 1, 20, 1, StringVar(value="10"), 10, 8)

    line_horizontal(win, 0, 9, 11)

    single_spinbox_scale(win, "Crossover", 0, 10)

    line_vertical(win, 4, 9, 3)

    double_spinbox_scale(win, "Single", "Double", 5, 10)

    line_horizontal(win, 0, 11, 11)

    single_spinbox_scale(win, "Mutation", 0, 12)

    line_vertical(win, 4, 11, 3)

    double_spinbox_scale(win, "Tournament", "Roulette", 5, 12)

    line_horizontal(win, 0, 13, 11)

    create_button(win, "Enter", 5, 14)

    win.mainloop()
