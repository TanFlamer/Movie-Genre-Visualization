import math
import random

import numpy as np

# Random seed
RANDOM_SEED = 20313854

# State and Action space
NUM_BUCKETS = (2,)
NUM_ACTIONS = 2

# Defining the simulation related constants
NUM_TRAIN_EPISODES = 500
MAX_TRAIN_T = 200

# Hyper parameters
MIN_LEARNING_RATE = 0.1
MIN_EXPLORE_RATE = 0.01
DISCOUNT_FACTOR = 0.99


class QLearning:
    def __init__(self):
        # Episodes
        self.episode = 0
        # Horizontal actions
        self.horizontal_q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))
        self.horizontal_state_0 = None
        self.horizontal_state = None
        self.horizontal_action = None
        # Vertical actions
        self.vertical_q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))
        self.vertical_state_0 = None
        self.vertical_state = None
        self.vertical_action = None

    def new_episode(self):
        self.episode += 1

    def get_initial_state(self, obv):
        self.horizontal_state_0, self.vertical_state_0 = state_to_bucket(obv)

    def get_state(self, obv):
        self.horizontal_state, self.vertical_state = state_to_bucket(obv)

    def get_action(self):
        # Get explore rate
        explore_rate = get_explore_rate(self.episode)

        # Select an action
        self.horizontal_action = select_action(self.horizontal_state_0, self.horizontal_q_table, explore_rate)
        self.vertical_action = select_action(self.vertical_state_0, self.vertical_q_table, explore_rate)

        # Return action
        return self.horizontal_action, self.vertical_action

    def update_table(self, obv):
        # Get learning rate
        learning_rate = get_learning_rate(self.episode)

        # Get reward
        horizontal_reward, vertical_reward = get_reward(obv)

        # Update horizontal Q-table
        best_q = np.amax(self.horizontal_q_table[self.horizontal_state])
        self.horizontal_q_table[self.horizontal_state_0 + (self.horizontal_action,)] += learning_rate * (
                horizontal_reward + DISCOUNT_FACTOR * best_q - self.horizontal_q_table[
                    self.horizontal_state_0 + (self.horizontal_action,)])

        # Update vertical Q-table
        best_q = np.amax(self.vertical_q_table[self.vertical_state])
        self.vertical_q_table[self.vertical_state_0 + (self.vertical_action,)] += learning_rate * (
                vertical_reward + DISCOUNT_FACTOR * best_q - self.vertical_q_table[
                    self.vertical_state_0 + (self.vertical_action,)])

        # Save old state
        self.horizontal_state_0 = self.horizontal_state
        self.vertical_state_0 = self.vertical_state


# Select action based on sum of Q-tables or randomly
def select_action(state, q_table, explore_rate):
    # Select a random action
    if random.random() < explore_rate:
        action = random.randint(0, 1)
    # Select the action with the highest q
    else:
        action = np.argmax(q_table[state])
    return action


def get_reward(obv):
    # Paddle and ball coordinates
    paddle_coords, ball_coords = obv
    paddle_x = (paddle_coords[0] + paddle_coords[2]) * 0.5
    paddle_y = (paddle_coords[1] + paddle_coords[3]) * 0.5
    ball_x = (ball_coords[0] + ball_coords[2]) * 0.5
    ball_y = (ball_coords[1] + ball_coords[3]) * 0.5

    # Rewards
    horizontal_reward = 6 - abs(paddle_x - ball_x) / 100
    vertical_reward = 6 - abs(abs(paddle_y - ball_y) - 100) / 100

    # Return absolute distance of ball and paddle
    return horizontal_reward, vertical_reward


# Get explore rate based on episode
def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(1.0, 1.0 - math.log10((t + 1) / 10)))


# Get learning rate based on episode
def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t + 1) / 10)))


# Get bucket from state
def state_to_bucket(obv):
    # State indices
    horizontal_bucket_indices = []
    vertical_bucket_indices = []

    # Paddle and ball coordinates
    paddle_coords, ball_coords = obv
    paddle_x = (paddle_coords[0] + paddle_coords[2]) * 0.5
    paddle_y = (paddle_coords[1] + paddle_coords[3]) * 0.5
    ball_x = (ball_coords[0] + ball_coords[2]) * 0.5
    ball_y = (ball_coords[1] + ball_coords[3]) * 0.5

    # First state
    horizontal_bucket_indices.append(0 if paddle_x >= ball_x else 1)
    vertical_bucket_indices.append(0 if paddle_y - ball_y <= 100 else 1)
    return tuple(horizontal_bucket_indices), tuple(vertical_bucket_indices)


# Initialise all random number generator with give seed
def random_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
