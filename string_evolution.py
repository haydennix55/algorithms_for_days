import random
"""
This is my first attempt at implementing a evolutionary algorithm. The
goal is to start with a population of 30 strings, all the same length as a
target string, made of completely random characters. Then, using natural selection
over 5000 generations, we crossover and mutate the most likely survivors of
each generation, add in the potential for random genetic mutation, and repeat to
generationally arrive at the target string. Most likely survivors are determined
by a strings fitness, which in this case is how similar to the target string it is.
"""

#Global Vars
TARGET_GENOME = "Made via Natural Selection :)"
POP_SIZE = 30
MAX_GEN = 5000

def random_character():
    """
    Returns random character (symbols, spaces, letters, digits)
    """
    return chr(int(random.randrange(32, 126, 1)))

def init_population(pop_size, genome_length):
    """
    Create and returns a population of strings made of random chars
    """
    population = []
    for i in xrange(pop_size):
        indiv = ""
        for j in xrange(genome_length):
            indiv += random_character()
        population.append(indiv)
    return population

def fitness(indiv, target_genome):
    """
    Return a float value between 0 and 1 of the fitness of the given individual.
    Fitness is 1 / the summation of the distances between the Unicode char representations
    of the characters in the individual and the characters in the target.
    """
    fitness_inv = 0
    for x in xrange(len(target_genome)):
        fitness_inv += abs(ord(indiv[x]) - ord(target_genome[x]))

    if fitness_inv == 0:
        return 2.0
    else:
        return 1.0/float(fitness_inv)

def natural_selection(items):
    """
    Returns a single individual from a List of (individual, fitness) pairs.
    This is determined by the individuals fitnesses; The greater the fitness of
    the individual, the greater the chance of selection
    """
    weight_total = sum((item[1] for item in items))
    n = random.uniform(0, weight_total)
    for item, weight in items:
        if n < weight:
            return item
        n = n - weight
    return item

def crossover(ind1, ind2):
    """
    Returns the two given individuals crossed over at a random point.
    """
    pos = int(random.random()*len(TARGET_GENOME))
    return (ind1[:pos]+ind2[pos:], ind2[:pos]+ind1[pos:])

def mutate(indiv):
    """
    Returns a potentially mutated individual. For every individual, there is a
    chance of random genetic mutation. For every character, there is 1/100 chance
    it will be replaced with a random character
    """
    mutated = ""
    selection_odds = 100
    for c in xrange(len(TARGET_GENOME)):
        if int(random.random()*selection_odds) == 1:
          mutated += random_character()
        else:
          mutated += indiv[c]
    return mutated

if __name__ == "__main__":
    # create random population
    population = init_population(POP_SIZE, len(TARGET_GENOME))
    pop_fitness = []

    # loop through generations
    for gen in xrange(MAX_GEN):
        print "Generation %s, Example Genome: '%s'" % (gen, population[0])
        pop_fitness = []

        for indiv in population:
            # Assess fitness
            pop_fitness.append((indiv,fitness(indiv,TARGET_GENOME)))

        population = []

        for _ in xrange(POP_SIZE):
            # Natural Selection
            survivor1 = natural_selection(pop_fitness)
            survivor2 = natural_selection(pop_fitness)

            # Crossover
            crossed1, crossed2 = crossover(survivor1, survivor2)

            # Mutate and create new population
            population.append(mutate(crossed1))
            population.append(mutate(crossed2))

    # Find closest individual (fitness is 2 if perfect match)
    maximum_fitness = 0;
    for individual in population:
        ind_fitness = fitness(individual, TARGET_GENOME)
        if ind_fitness >= maximum_fitness:
          fittest_indiv = individual
          maximum_fitness = ind_fitness

    print "Best Genome: \'%s\', Fitness: %s" % (fittest_indiv, maximum_fitness)
    exit(0)
