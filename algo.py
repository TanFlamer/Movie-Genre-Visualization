import math
import random

import numpy as np

# State and Action space
NUM_BUCKETS = (2,)

# Hyper parameters
MIN_LEARNING_RATE = 0.1
MIN_EXPLORE_RATE = 0.01
DISCOUNT_FACTOR = 0.99


class QLearning:
    def __init__(self, parameter_settings):
        # Parameter settings
        [self.seed, self.num_q_table, self.state_type, self.num_state, self.num_action,
         self.random_num, self.opposition, self.reward_type] = parameter_settings
        # Set seed
        random.seed(self.seed)
        np.random.seed(self.seed)
        # Canvas dimensions
        self.width = 600
        self.height = 450
        # Episodes
        self.turn = 0
        self.episode = 0
        # Variables
        self.q_tables = []
        self.state_0 = None
        self.state = None
        self.action = None
        self.buckets = None
        self.reward_function = None
        self.constant = 1
        # Generate tables
        self.generate_buckets()
        self.generate_tables()
        self.assign_reward()

    def new_episode(self, obv):
        # Reset turn
        self.turn = 0
        # Increment episode
        self.episode += 1
        # Get initial states
        self.state_0 = self.state_to_bucket(obv)

    def generate_buckets(self):
        # Get bucket length
        def add_bucket(string): return self.num_state if string in self.state_type else 1
        # Set bucket length
        self.buckets = (add_bucket("Paddle"), add_bucket("Ball"), 2)

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
        if self.random_num == 0:
            # Generate arrays of 0s
            return np.zeros(NUM_BUCKETS + (self.num_action,))
        elif self.random_num > 0:
            # Generate arrays with normal distribution
            temp_table = np.random.randn(*NUM_BUCKETS, self.num_action) * (self.random_num / 3)
            # Bound arrays to range
            return np.clip(temp_table, -self.random_num, self.random_num)
        else:
            # Generate arrays with uniform distribution
            return np.random.uniform(self.random_num, -self.random_num, NUM_BUCKETS + (self.num_action,))

    # Get bucket from state
    def state_to_bucket(self, obv):
        # State indices
        bucket_indices = []

        # Midpoints
        [paddle_x, _, ball_x, _] = get_midpoints(obv)
        midpoints_x = [paddle_x, ball_x]

        # Paddle and ball state
        for index in range(2):
            x = midpoints_x[index]
            bucket = self.assign_bucket(x, index)
            bucket_indices.append(bucket)

        # Position state
        bucket_indices.append(0 if paddle_x <= ball_x else 1)

        # Return tuple
        return tuple(bucket_indices)

    def assign_bucket(self, x, index):
        num_buckets = self.buckets[index]
        if x < 0:
            return 0
        elif x >= self.width:
            return num_buckets - 1
        else:
            bucket_length = self.width / num_buckets
            return math.floor(x / bucket_length)

    # Select action based on sum of Q-tables or randomly
    def select_action(self):
        # Get explore rate
        explore_rate = get_explore_rate(self.episode)
        # Check for random action
        explore_action = random.random() < explore_rate
        # Random action
        random_action = random.randint(0, self.num_action - 1)
        # Best action
        best_action = np.argmax(sum(self.q_tables)[self.state_0])
        # Select action
        self.action = random_action if explore_action else best_action
        # Return action
        return self.action

    def update_table(self, obv, terminated):
        # Increment turn
        self.turn += 1

        # Get learning rate
        learning_rate = get_learning_rate(self.episode)

        # Get Q-Tables
        [main_q, secondary_q] = random.sample(self.q_tables, 2) if len(self.q_tables) > 1 else [self.q_tables[0]] * 2

        # Get state
        self.state = self.state_to_bucket(obv)

        # Get opposite action
        opposite_action = self.action if self.action == 2 else 1 - self.action

        # Get reward
        reward = self.reward_function(obv)

        # Update Q-table
        best_q = secondary_q[self.state + (np.argmax(main_q[self.state]),)]
        main_q[self.state_0 + (action,)] += learning_rate * (
                reward + DISCOUNT_FACTOR * best_q - main_q[self.state_0 + (action,)])

        # Save old state
        self.state_0 = self.state

    def assign_reward(self):
        if self.reward_type == "X-Distance":
            self.reward_function = self.x_distance
        elif self.reward_type == "X-Distance (Center)":
            self.reward_function = self.x_distance_center
        elif self.reward_type == "XY-Distance":
            self.reward_function = self.xy_distance
        elif self.reward_type == "Constant Reward":
            self.reward_function = self.constant_reward
        else:  # Time-Based
            self.reward_function = self.time_based

    def x_distance(self, obv):
        [paddle_x, _, ball_x, _] = get_midpoints(obv)
        dist = math.dist(paddle_x, ball_x)
        return (self.width - dist) / 100

    def x_distance_center(self, obv):
        [x1, _, x2, _] = obv[0]  # Paddle x
        [_, _, ball_x, _] = get_midpoints(obv)
        if x1 <= ball_x <= x2:
            return 0
        else:
            dist = x1 - ball_x if ball_x < x1 else ball_x - x2
            return (self.width - dist) / 100

    def xy_distance(self, obv):
        # Get midpoints
        [paddle_x, paddle_y, ball_x, ball_y] = get_midpoints(obv)
        paddle_mid = [paddle_x, paddle_y]
        ball_mid = [ball_x, ball_y]
        # Calculate distance
        max_dist = math.dist([0, 0], [self.width / 100, self.height / 100])
        dist = math.dist(paddle_mid, ball_mid) / 100
        return max_dist - dist

    def constant_reward(self, _):
        return self.constant

    def time_based(self, _):
        return self.turn / 10


def get_midpoints(obv):
    return get_midpoint(obv[0]) + get_midpoint(obv[1])


def get_midpoint(coords):
    return [(coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2]


# Get explore rate based on episode
def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(1.0, 1.0 - math.log10((t + 1) / 10)))


# Get learning rate based on episode
def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t + 1) / 10)))
