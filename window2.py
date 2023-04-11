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


def spinbox_scale(root, column, row):
    str_var = StringVar(value="50.0")

    scale = create_scale(root, IntVar(value=500), 0, 1000, column, row)
    scale.configure(command=lambda val: str_var.set(str(int(val) / 10)))

    spinbox = create_spinbox(root, 0.0, 100.0, 0.1, str_var, column + 2, row)
    spinbox.configure(command=lambda: scale.set(float(str_var.get()) * 10))

    return scale, spinbox


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

    for x in range(8): win.grid_columnconfigure(x, weight=1)
    for y in range(28): win.grid_rowconfigure(y, weight=1)

    create_label(win, "Hyperparameter Tuning", 1, 0)
    line_vertical(win, 0, 1, 9)
    line_vertical(win, 2, 1, 9)
    line_vertical(win, 7, 1, 9)

    line_horizontal(win, 0, 1, 11)

    create_label(win, "Learning Rate", 1, 3)

    create_label(win, "Initial", 3, 2)
    spinbox_scale(win, 4, 2)

    create_label(win, "Final", 3, 3)
    spinbox_scale(win, 4, 3)

    create_label(win, "Step", 3, 4)
    spinbox_scale(win, 4, 4)

    line_horizontal(win, 0, 5, 11)

    create_label(win, "Mean", 3, 7)
    create_entry(win, StringVar(value="20313854"), 4, 7)

    create_label(win, "STD", 5, 7)
    create_entry(win, StringVar(value="20313854"), 6, 7)




    win.mainloop()

# Ball Speed, Paddle Speed, Row Count, Block Count
