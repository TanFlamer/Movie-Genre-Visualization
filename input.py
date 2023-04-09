# Import the required Libraries
from tkinter import *


def label_text(root, text, column, row):
    Label(root, anchor="center", text=text, font=("Arial", 12, "bold")).grid(column=column, row=row, columnspan=2)


def spinbox_to_scale(root, from_, to, increment, string_var, scale, column, row):
    spinbox = Spinbox(root, from_=from_, to=to, increment=increment, textvariable=string_var, width=5,
                      command=lambda: scale.set(float(string_var.get()) * 10))
    spinbox.grid(column=column, row=row)
    return spinbox


def scale_to_spinbox(root, int_var, from_, to, string_var, column, row):
    scale = Scale(root, variable=int_var, from_=from_, to=to, orient=HORIZONTAL, showvalue=False,
                  command=lambda val: string_var.set(str(int(val) / 10)))
    scale.grid(column=column, row=row, columnspan=2, sticky='EW')
    return scale


class Hyperparameter:
    def __init__(self, root, row, text):
        label_text(root, text, 0, row)
        self.root = root
        self.row = row
        self.initial = self.fill_dict(1000, 2)
        self.final = self.fill_dict(1000, 5)
        self.step = self.fill_dict(10, 8)

    def fill_dict(self, value, column):
        dict_ = {}
        int_var = IntVar(value=value / 2)
        dict_['int_var'] = int_var
        string_var = StringVar(value=str(value / 20))
        dict_['string_var'] = string_var
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

    for x in range(12): win.grid_columnconfigure(x, weight=1)
    for y in range(12): win.grid_rowconfigure(y, weight=1)

    # Seed
    label_text(win, "Seed", 0, 0)
    seed = StringVar(value="20313854")
    Entry(win, textvariable=seed, font=("Arial", 12), width=10).grid(column=2, row=0)

    # Q-table
    label_text(win, "Q-Table", 3, 0)
    q_table = StringVar(value="1")
    Spinbox(win, from_=1, to=10, increment=1, textvariable=q_table, width=5).grid(column=5, row=0)

    # State Space
    label_text(win, "State Space", 6, 0)
    state_space = StringVar(value="2")
    Spinbox(win, from_=1, to=20, increment=1, textvariable=state_space, width=5).grid(column=8, row=0)

    # Action Space
    label_text(win, "Action Space", 9, 0)
    action_space = IntVar(value=0)
    Checkbutton(win, text="Empty Move", variable=action_space).grid(column=11, row=0)

    # Random
    label_text(win, "Random", 0, 1)

    include = IntVar(value=0)
    Checkbutton(win, text="Randomise", variable=include).grid(column=2, row=1)

    low = StringVar(value="0")
    Spinbox(win, from_=-10, to=0, increment=1, textvariable=low, width=5).grid(column=3, row=1)

    Label(win, anchor="center", text="to", font=("Arial", 12, "bold")).grid(column=4, row=1)

    high = StringVar(value="0")
    Spinbox(win, from_=0, to=10, increment=1, textvariable=high, width=5).grid(column=5, row=1)

    # Opposition Learning
    label_text(win, "Opposition", 6, 1)
    opposition = IntVar(value=0)
    Checkbutton(win, text="Include", variable=opposition).grid(column=8, row=1)

    # Reward Function
    label_text(win, "Reward Function", 9, 1)
    option_list = ["Test", "Test1"]
    option = StringVar(value="Test")
    OptionMenu(win, option, *option_list).grid(column=11, row=1)

    win.mainloop()


# Hyperparameters
# learning_rate = Hyperparameter(win, 0, "Learning Rate")
# discount_factor = Hyperparameter(win, 1, "Discount Factor")
# explore_rate = Hyperparameter(win, 2, "Explore Rate")
