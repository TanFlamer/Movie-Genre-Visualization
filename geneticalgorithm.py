import random

# Boundary of rates
MAX_RATE = 0.99
UPPER_MID = 0.75
LOWER_MID = 0.35
MIN_RATE = 0.01

# Size of steps
MAX_STEP = 0.01
MIN_STEP = 0.001

# Genetic algorithm parameters
CROSSOVER_RATE = 1
MUTATION_RATE = 0.1


# Generate initial chromosomes
def generate_initial_population():
    initial_population = []
    for x in range(10):
        new_chromosome = []
        for y in range(3):
            new_chromosome.append(random.uniform(MIN_RATE, LOWER_MID))
            new_chromosome.append(random.uniform(UPPER_MID, MAX_RATE))
            new_chromosome.append(random.uniform(MIN_STEP, MAX_STEP))
        initial_population.append(new_chromosome)
    return initial_population


def mutation(chromosome):
    for x in range(9):
        if random.random() < MUTATION_RATE:
            print("mutation")
            gene_position = x % 3
            if gene_position == 0:
                chromosome[x] = random.uniform(MIN_RATE, LOWER_MID)
            elif gene_position == 1:
                chromosome[x] = random.uniform(UPPER_MID, MAX_RATE)
            else:
                chromosome[x] = random.uniform(MIN_STEP, MAX_STEP)
