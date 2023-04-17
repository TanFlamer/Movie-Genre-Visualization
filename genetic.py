import math
import random
from operator import itemgetter


# Generate random value
def get_rand_val(val):
    return random.randint(0, val) / 100


# Get correct sign
def check_sign(chromosome):
    for x in range(3):
        [first, second, third] = [chromosome[x * 3], chromosome[x * 3 + 1], chromosome[x * 3 + 2]]
        if first > second:
            chromosome[3 * x + 2] = -abs(third)


# Generate initial chromosomes
def generate_initial_population(population_size):
    initial_population = []
    for x in range(population_size):
        new_chromosome = []
        for y in range(3):
            new_chromosome.append(get_rand_val(100))
            new_chromosome.append(get_rand_val(100))
            new_chromosome.append(get_rand_val(10))
        initial_population.append(new_chromosome)
    return initial_population


# Evaluate fitness of chromosome
def evaluate_chromosome(chromosome, episodes):
    # Fix chromosome sign
    check_sign(chromosome)
    # Get chromosome fitness
    fitness = sum(chromosome)
    # Return chromosome fitness
    return fitness


# Evaluate fitness of population
def evaluate_population(population, episodes):
    evaluated_population = []
    for chromosome in population:
        fitness = evaluate_chromosome(chromosome, episodes)
        evaluated_population.append((chromosome, fitness))
    return evaluated_population


# Save top 10 fittest chromosome
def evaluate_fittest(old_list, new_list, best):
    # Make new list from old list
    improved_list = list(old_list)
    # Add to new list if not already present
    improved_list.extend(x for x in new_list if x not in improved_list)
    # Sort list
    improved_list.sort(key=lambda x: x[1], reverse=True)
    # Return top chromosomes
    return improved_list[:best]


# Tournament selection for parents
def tournament_selection(evaluated_population):
    new_parents = []
    population_size = len(evaluated_population)
    for x in range(population_size):
        tournament_size = math.ceil(population_size / 4)
        random_sample = random.sample(evaluated_population, tournament_size)
        new_parent = min(random_sample, key=itemgetter(1))[0]
        new_parents.append(new_parent)
    return new_parents


# Roulette selection for parents
def roulette_selection(evaluated_population):
    new_parents = []
    total_fitness = sum(x[1] for x in evaluated_population)
    probability = [1 - (x[1] / total_fitness) for x in evaluated_population]
    population_size = len(evaluated_population)
    for x in range(population_size):
        new_parent = random.choices(evaluated_population, weights=probability)[0][0]
        new_parents.append(new_parent)
    return new_parents


# Parent selection
def selection(evaluated_population, roulette_tournament):
    func = tournament_selection if random.random() < roulette_tournament else roulette_selection
    new_parents = func(evaluated_population)
    return new_parents


# Single-point crossover
def single_crossover(first_parent, second_parent):
    # Get crossover point
    crossover_point = random.randint(1, 7)
    # Perform crossover
    first_chromosome = first_parent[:crossover_point] + second_parent[crossover_point:]
    second_chromosome = second_parent[:crossover_point] + first_parent[crossover_point:]
    # Return chromosomes
    return [first_chromosome, second_chromosome]


# Two-point crossover
def double_crossover(first_parent, second_parent):
    # Get crossover points
    first_point = random.randint(1, 3)
    second_point = random.randint(5, 7)
    # Perform crossover
    first_chromosome = first_parent[:first_point] + second_parent[first_point:second_point] + first_parent[
                                                                                              second_point:]
    second_chromosome = second_parent[:first_point] + first_parent[first_point:second_point] + second_parent[
                                                                                               second_point:]
    # Return chromosomes
    return [first_chromosome, second_chromosome]


# Chromosome crossover
def crossover(first_parent, second_parent, crossover_rate, single_double):
    if random.random() < crossover_rate:
        # No crossover occurs
        chromosomes = [first_parent.copy(), second_parent.copy()]
    else:
        # Single or double crossover
        func = single_crossover if random.random() < single_double else double_crossover
        chromosomes = func(first_parent, second_parent)
    return chromosomes


# Mutate chromosome
def mutate_chromosome(chromosome, mutation_rate):
    for x in range(9):
        if random.random() < mutation_rate:
            gene_position = x % 3
            max_val = 10 if gene_position == 2 else 100
            chromosome[x] = get_rand_val(max_val)


# Genetic algorithm
def genetic_algorithm(tuning_settings):
    # Get tuning settings
    [single_double, roulette_tournament, crossover_rate, mutation_rate,
     population_size, generation_size, episodes, best] = tuning_settings

    # Generate initial population
    population = generate_initial_population(population_size)

    # Top 10 fittest chromosomes
    fittest_chromosomes = []

    # Run for 100 generations
    for generation in range(generation_size):
        # Evaluate population
        evaluated_population = evaluate_population(population, episodes)

        # Reevaluate fittest chromosome
        fittest_chromosomes = evaluate_fittest(fittest_chromosomes, evaluated_population, best)
        # print([x[1] for x in fittest_chromosomes])

        # Get new parents
        new_parents = selection(evaluated_population, roulette_tournament)

        # New population
        new_population = []

        # Generate new population
        for x in range(0, 10, 2):
            # Get new parents
            first_parent, second_parent = new_parents[x], new_parents[x + 1]

            # Mutate new chromosomes
            for chromosome in crossover(first_parent, second_parent, crossover_rate, single_double):
                # Mutate chromosome
                mutate_chromosome(chromosome, mutation_rate)

                # Get mutated chromosome
                new_population.append(chromosome)

        # Replace population
        population = new_population

    # Return top 10 fittest chromosomes
    return fittest_chromosomes


if __name__ == '__main__':
    tuning_settings = [0.5, 0.5, 0.5, 0.5, 10, 100, 200, 10]
    genetic_algorithm(tuning_settings)