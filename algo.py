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
         self.random_num, self.opposition, self.reward_func] = parameter_settings
        # Set seed
        random.seed(self.seed)
        np.random.seed(self.seed)
        # Episodes
        self.episode = 0
        # Variables
        self.q_tables = []
        self.state_0 = None
        self.state = None
        self.action = None
        self.buckets = None
        # Generate tables
        self.generate_buckets()
        self.generate_tables()

    def new_episode(self, obv):
        # Increment count
        self.episode += 1
        # Get initial states
        self.state_0 = state_to_bucket(obv)

    def generate_buckets(self):
        if self.state_type == "-":
            print("lol")

    def generate_reward(self):
        # X-Distance, X-Distance -Center, XY-Distance, Constant 1
        # Time-Based (Linear, Log, Exp)
        if self.reward_func == "":
            print("lol")

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
            q_table = np.random.randn(*NUM_BUCKETS, self.num_action) * (self.random_num / 3)
            return np.clip(q_table, -self.random_num, self.random_num)
        else:
            # Generate arrays with uniform distribution
            return np.random.uniform(self.random_num, -self.random_num, NUM_BUCKETS + (self.num_action,))

    # Select action based on sum of Q-tables or randomly
    def select_action(self):
        # Get explore rate
        explore_rate = get_explore_rate(self.episode)
        # Check for random action
        rand_action = random.random() < explore_rate
        # Get available actions
        action_pool = [0, 1, 2] if self.num_action else [0, 2]
        # Select an action
        self.action = random.choice(action_pool) if rand_action else np.argmax(sum(self.q_tables)[self.state_0])
        # Return action
        return self.action

    def update_table(self, obv, reward=None):
        # Get learning rate
        learning_rate = get_learning_rate(self.episode)

        # Get Q-Tables
        [main_q, secondary_q] = random.sample(self.q_tables, 2) if len(self.q_tables) > 1 else [self.q_tables[0]] * 2

        # Get state
        self.state = state_to_bucket(obv)

        # Get reward
        if reward is None:
            reward = get_reward(obv)
        else:
            reward = reward

        # Update Q-table
        best_q = secondary_q[self.state + (np.argmax(main_q[self.state]),)]
        main_q[self.state_0 + (self.action,)] += learning_rate * (
                reward + DISCOUNT_FACTOR * best_q - main_q[self.state_0 + (self.action,)])

        # Save old state
        self.state_0 = self.state


def get_reward(obv):
    # Paddle and ball coordinates
    [paddle_x, paddle_y, ball_x, ball_y] = obv

    # Rewards
    horizontal_reward = 6 - abs(paddle_x - ball_x) / 100

    # Return absolute distance of ball and paddle
    return horizontal_reward


# Get explore rate based on episode
def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(1.0, 1.0 - math.log10((t + 1) / 10)))


# Get learning rate based on episode
def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t + 1) / 10)))


# Get bucket from state
def state_to_bucket(obv):
    # State indices
    bucket_indices = []

    # Paddle and ball coordinates
    [paddle_x, paddle_y, ball_x, ball_y] = obv

    # First state
    bucket_indices.append(0 if paddle_x >= ball_x else 1)

    # Horizontal
    # bucket_indices.append(math.floor(paddle_x / 100))
    # bucket_indices.append(math.floor(ball_x / 100))

    return tuple(bucket_indices)
