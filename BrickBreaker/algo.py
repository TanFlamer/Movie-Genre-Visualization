import math
import random
import numpy as np


def get_midpoints(obv):
    return get_midpoint(obv[0]) + get_midpoint(obv[1])


def get_midpoint(coords):
    return [(coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2]


class QLearning:
    def __init__(self, parameter_settings, hyper_parameters, dimensions):
        # Parameter settings
        [self.num_q_table, self.num_state, self.num_action,
         self.random_num, self.opposition, self.reward_type] = parameter_settings

        # Hyper-parameters settings
        [self.learning_initial, self.learning_final, self.learning_step,
         self.explore_initial, self.explore_final, self.explore_step,
         self.discount_initial, self.discount_final, self.discount_step] = hyper_parameters

        # Canvas dimensions
        [self.width, self.height] = dimensions

        # Episodes
        self.turn = 0
        self.episode = 0
        self.runs = 0

        # Variables
        self.q_tables = []
        self.state_0 = None
        self.buckets = None
        self.reward_function = None
        self.constant = 1

        # Generate tables
        self.generate_buckets()
        self.generate_tables()
        self.check_step_sign()
        self.assign_reward()

    def new_run(self):
        # Reset Q-tables
        self.generate_tables()
        # Increment run
        self.runs += 1
        # Reset episode
        self.episode = 0

    def new_episode(self, obv):
        # Increment episode
        self.episode += 1
        # Reset turn
        self.turn = 0
        # Get initial states
        self.state_0 = self.state_to_bucket(obv)

    def generate_buckets(self):
        # Set bucket length
        self.buckets = (self.num_state * 2, self.num_action)

    def generate_tables(self):
        # Clear old tables
        self.q_tables.clear()
        # Loop to create Q-tables
        for x in range(self.num_q_table):
            # Generate Q-Table
            q_table = self.single_table()
            # Append to Q-table list
            self.q_tables.append(q_table)

    def single_table(self):
        rand_num = int(self.random_num)
        if rand_num == 0:
            # Generate arrays of 0s
            return np.zeros(self.buckets)
        elif rand_num > 0:
            # Generate arrays with normal distribution
            temp_table = np.random.randn(*self.buckets) / 3
            # Bound arrays to range
            return np.clip(temp_table, -1, 1)
        else:
            # Generate arrays with uniform distribution
            return np.random.uniform(-1, 1, self.buckets)

    # Get bucket from state
    def state_to_bucket(self, obv):
        # Midpoints
        [paddle_x, _, ball_x, _] = get_midpoints(obv)
        # Get difference
        diff_x = paddle_x - ball_x
        # Get bucket
        bucket = self.assign_bucket(abs(diff_x))
        # Get index
        bucket_index = self.num_state + bucket if diff_x >= 0 else (self.num_state - 1) - bucket
        # Return tuple
        return tuple([bucket_index])

    def assign_bucket(self, x):
        if x < 0:
            return 0
        elif x >= self.width:
            return self.num_state - 1
        else:
            bucket_length = self.width / self.num_state
            return math.floor(x / bucket_length)

    # Select action based on sum of Q-tables or randomly
    def select_action(self):
        # Get explore rate
        explore_rate = self.get_explore_rate()
        # Check for random action
        explore_action = random.random() < explore_rate
        # Random action
        random_action = random.randint(0, self.num_action - 1)
        # Best action
        best_action = np.argmax(sum(self.q_tables)[self.state_0])
        # Select action
        return random_action if explore_action else best_action

    def update_policy(self, obv, opposite_obv, action, terminated):
        # Increment turn
        self.turn += 1
        # Get Q-Tables
        [main_q, secondary_q] = random.sample(self.q_tables, 2) if len(self.q_tables) > 1 else [self.q_tables[0]] * 2
        # Update table
        self.update_table(main_q, secondary_q, obv, action, terminated)
        # Update opposite table
        if self.opposition and action <= 1:
            # Get opposite action
            opposite_action = 1 - action
            # Update table
            self.update_table(main_q, secondary_q, opposite_obv, opposite_action, terminated)
        # Save old state
        self.state_0 = self.state_to_bucket(obv)

    def update_table(self, main_table, secondary_table, obv, action, terminated):
        # Get learning rate
        learning_rate = self.get_learning_rate()
        # Get discount factor
        discount_factor = self.get_discount_factor()
        # Get state
        state = self.state_to_bucket(obv)
        # Get reward
        reward = self.reward_function(obv, terminated)
        # Update Q-table
        best_q = secondary_table[state + (np.argmax(main_table[state]),)]
        main_table[self.state_0 + (action,)] += learning_rate * (
                reward + discount_factor * best_q - main_table[self.state_0 + (action,)])

    def get_learning_rate(self):
        [func, new_step] = self.get_new_step(self.learning_step)
        return func(self.learning_initial + new_step, self.learning_final)

    def get_explore_rate(self):
        [func, new_step] = self.get_new_step(self.explore_step)
        return func(self.explore_initial + new_step, self.explore_final)

    def get_discount_factor(self):
        [func, new_step] = self.get_new_step(self.discount_step)
        return func(self.discount_initial + new_step, self.discount_final)

    def get_new_step(self, step):
        func = min if step >= 0 else max
        next_step = step * self.episode
        return [func, next_step]

    def check_step_sign(self):
        if self.learning_initial > self.learning_final: self.learning_step = -abs(self.learning_step)
        if self.explore_initial > self.explore_final: self.explore_step = -abs(self.explore_step)
        if self.discount_initial > self.discount_final: self.discount_step = -abs(self.discount_step)

    def assign_reward(self):
        if self.reward_type == "X-Distance":
            self.reward_function = self.x_distance
        elif self.reward_type == "X-Distance(Center)":
            self.reward_function = self.x_distance_center
        elif self.reward_type == "Time-Based":
            self.reward_function = self.time_based
        else:  # Constant
            self.reward_function = self.constant_reward

    def x_distance(self, obv, _):
        [paddle_x, _, ball_x, _] = get_midpoints(obv)
        dist = math.dist([paddle_x], [ball_x])
        return (self.width - dist) / 100

    def x_distance_center(self, obv, _):
        [x1, _, x2, _] = obv[0]  # Paddle x
        [_, _, ball_x, _] = get_midpoints(obv)
        if x1 <= ball_x <= x2:
            return self.width / 100
        else:
            dist = x1 - ball_x if ball_x < x1 else ball_x - x2
            return (self.width - dist) / 100

    def time_based(self, _, terminated):
        return 0 if terminated else self.turn / 10

    def constant_reward(self, _, terminated):
        return 0 if terminated else self.constant
