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
    win.geometry("600x450")
    win.grid()

    for x in range(3): win.grid_columnconfigure(x, weight=1)
    #win.grid_columnconfigure(0, weight=1)
    #win.grid_columnconfigure(2, weight=1)
    for y in range(28): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Game Settings", 1, 0)
    line_vertical(win, 1, 1, 9)

    line_horizontal(win, 0, 1, 11)

    create_label(win, "Ball Speed", 0, 2).grid(sticky="E")
    create_spinbox(win, 1, 10, 1, StringVar(value="5"), 2, 2).grid(sticky="W")

    line_horizontal(win, 0, 3, 11)

    create_label(win, "Paddle Speed", 0, 4)
    create_spinbox(win, 1, 10, 1, StringVar(value="5"), 2, 4)

    line_horizontal(win, 0, 5, 11)

    create_label(win, "Brick Rows", 0, 6)
    create_spinbox(win, 1, 10, 1, StringVar(value="3"), 2, 6)

    line_horizontal(win, 0, 7, 11)

    create_label(win, "Bricks in Row", 0, 8)
    create_spinbox(win, 1, 15, 1, StringVar(value="8"), 2, 8)

    line_horizontal(win, 0, 9, 11)

    # Parameters
    create_label(win, "Parameter Settings", 1, 10)
    line_vertical(win, 1, 11, 15)

    line_horizontal(win, 0, 11, 11)

    create_label(win, "Seed", 0, 12)
    create_entry(win, StringVar(value="20313854"), 2, 12)

    line_horizontal(win, 0, 13, 11)

    create_label(win, "Q-Table", 0, 14)
    create_spinbox(win, 1, 10, 1, StringVar(value="1"), 2, 14)

    line_horizontal(win, 0, 15, 11)

    create_label(win, "State", 0, 16)
    create_spinbox(win, 1, 10, 1, StringVar(value="2"), 2, 16)

    line_horizontal(win, 0, 17, 11)

    create_label(win, "Action", 0, 18)
    create_checkbutton(win, "Empty Move", IntVar(value=0), 2, 18)

    line_horizontal(win, 0, 19, 11)

    create_label(win, "Random", 0, 20)
    create_spinbox(win, 0, 10, 1, StringVar(value="0"), 2, 20)

    line_horizontal(win, 0, 21, 11)

    create_label(win, "Opposition", 0, 22)
    create_checkbutton(win, "Include", IntVar(value=0), 2, 22)

    line_horizontal(win, 0, 23, 11)

    create_label(win, "Reward", 0, 24)
    option_list = ["Test", "Test1"]
    create_option_menu(win, StringVar(value="Test"), option_list, 2, 24)

    line_horizontal(win, 0, 25, 11)

    create_button(win, "Tuning", 0, 26).grid(sticky="E")
    create_button(win, "Experiment", 2, 26).grid(sticky="W")

    win.mainloop()

# Ball Speed, Paddle Speed, Row Count, Block Count
