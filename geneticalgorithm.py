import random
from operator import itemgetter

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


# Evaluate fitness of chromosome
def evaluate_chromosome(chromosome):
    fitness = sum(chromosome)
    return fitness


# Evaluate fitness of population
def evaluate_population(population):
    evaluated_population = []
    for chromosome in population:
        fitness = evaluate_chromosome(chromosome)
        evaluated_population.append((chromosome, fitness))
    return evaluated_population


# Save top 10 fittest chromosome
def evaluate_fittest(old_list, new_list):
    # Adds all data to same list
    improved_list = list(old_list)
    improved_list.extend(x for x in new_list if x not in improved_list)
    # Sort list
    improved_list.sort(key=lambda x: x[1], reverse=True)
    # Return top 10 chromosomes only
    return improved_list[:10]


# Tournament selection for parents
def tournament_selection(evaluated_population):
    new_parents = []
    for x in range(10):
        random_sample = random.sample(evaluated_population, 3)
        new_parent = max(random_sample, key=itemgetter(1))[0]
        new_parents.append(new_parent)
    return new_parents


# Single-point crossover
def single_crossover(first_parent, second_parent):
    # Get crossover point
    crossover_point = random.randint(1, 7)
    # Perform crossover
    first_chromosome = first_parent[:crossover_point] + second_parent[crossover_point:]
    second_chromosome = second_parent[:crossover_point] + first_parent[crossover_point:]
    return [first_chromosome, second_chromosome]


# Two-point crossover
def double_crossover(first_parent, second_parent):
    # Get crossover points
    first_point = random.randint(1, 3)
    second_point = random.randint(5, 7)
    # Perform crossover
    first_chromosome = first_parent[:first_point] + second_parent[first_point:second_point] + first_parent[second_point:]
    second_chromosome = second_parent[:first_point] + first_parent[first_point:second_point] + second_parent[second_point:]
    return [first_chromosome, second_chromosome]


# Chromosome crossover
def crossover(first_parent, second_parent):
    # No crossover occurs
    if random.random() < CROSSOVER_RATE:
        chromosomes = [first_parent.copy(), second_parent.copy()]
    else:
        if random.random() < 0.5:
            # Single crossover
            chromosomes = single_crossover(first_parent, second_parent)
        else:
            # Double crossover
            chromosomes = double_crossover(first_parent, second_parent)
    return chromosomes


# Mutate chromosome
def mutate_chromosome(chromosome):
    for x in range(9):
        if random.random() < MUTATION_RATE:
            gene_position = x % 3
            if gene_position == 0:
                chromosome[x] = random.uniform(MIN_RATE, LOWER_MID)
            elif gene_position == 1:
                chromosome[x] = random.uniform(UPPER_MID, MAX_RATE)
            else:
                chromosome[x] = random.uniform(MIN_STEP, MAX_STEP)


# Genetic algorithm
def genetic_algorithm():
    # Generate initial population
    population = generate_initial_population()
    # Top 10 fittest chromosomes
    fittest_chromosomes = []
    # Run for 100 generations
    for generation in range(100):
        # Evaluate population
        evaluated_population = evaluate_population(population)
        # Reevaluate fittest chromosome
        fittest_chromosomes = evaluate_fittest(fittest_chromosomes, evaluated_population)
        # Get new parents
        new_parents = tournament_selection(evaluated_population)
        # New population
        new_population = []
        # Generate new population
        for x in range(0, 10, 2):
            # Get new parents
            first_parent, second_parent = new_parents[x], new_parents[x + 1]
            # Mutate new chromosomes
            for chromosome in crossover(first_parent, second_parent):
                # Mutate chromosome
                mutate_chromosome(chromosome)
                # Get mutated chromosome
                new_population.append(chromosome)
        # Replace population
        population = new_population
    # Return top 10 fittest chromosomes
    return fittest_chromosomes


genetic_algorithm()
