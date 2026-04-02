# ============================================================
#  TOPIC 6: GENETIC ALGORITHM (GA)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Evolve optimal crowd distribution plans across
#            exits through Selection, Crossover, and Mutation
# ============================================================

import random

random.seed(42)

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
EXIT_NAMES      = ['E1', 'E2', 'E3']
EXIT_CAPACITIES = {'E1': 500, 'E2': 400, 'E3': 300}
TOTAL_CROWD     = 1000
SAFE_RATIO      = 0.80
POP_SIZE        = 10
GENERATIONS     = 50
MUTATION_RATE   = 0.3


# ------------------------------------------------------------------
# Chromosome: [n_E1, n_E2, n_E3]  — must sum to TOTAL_CROWD
# ------------------------------------------------------------------
def random_chromosome():
    splits = sorted([random.randint(0, TOTAL_CROWD) for _ in range(2)])
    return [splits[0], splits[1] - splits[0], TOTAL_CROWD - splits[1]]


# ------------------------------------------------------------------
# Fitness — higher (less negative) = better
# ------------------------------------------------------------------
def fitness(chromosome):
    penalty = 0
    for i, exit_name in enumerate(EXIT_NAMES):
        load     = chromosome[i]
        capacity = EXIT_CAPACITIES[exit_name]
        ratio    = load / capacity
        if ratio > SAFE_RATIO:
            penalty += (ratio - SAFE_RATIO) * 1000
        if ratio > 1.0:
            penalty += (ratio - 1.0) * 5000
        if ratio < 0.3:
            penalty += (0.3 - ratio) * 50
    return -penalty


# ------------------------------------------------------------------
# SELECTION — Tournament Selection (k=3)
# ------------------------------------------------------------------
def tournament_select(population, k=3):
    """
    Pick k random candidates. Return the one with highest fitness.
    Mimics natural selection — better plans win more often.
    """
    candidates = random.sample(population, k)
    return max(candidates, key=fitness)


# ------------------------------------------------------------------
# CROSSOVER — Single Point Crossover
# ------------------------------------------------------------------
def crossover(parent1, parent2):
    """
    Cut both parents at a random point.
    Child = parent1[:point] + parent2[point:]
    Adjust to maintain TOTAL_CROWD.
    """
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    total = sum(child)
    if total != TOTAL_CROWD:
        diff     = TOTAL_CROWD - total
        child[0] += diff
    return child


# ------------------------------------------------------------------
# MUTATION — Random Gene Shift
# ------------------------------------------------------------------
def mutate(chromosome, mutation_rate=MUTATION_RATE):
    """
    With mutation_rate probability, shift 5-50 people
    between two random exits. Maintains TOTAL_CROWD.
    """
    chromosome = chromosome[:]
    if random.random() < mutation_rate:
        i, j  = random.sample(range(len(chromosome)), 2)
        shift = random.randint(5, 50)
        if chromosome[i] >= shift:
            chromosome[i] -= shift
            chromosome[j] += shift
    return chromosome


# ------------------------------------------------------------------
# GENETIC ALGORITHM — Main Loop
# ------------------------------------------------------------------
def genetic_algorithm(pop_size=POP_SIZE, generations=GENERATIONS):
    """
    Full GA:
    1. Initialize random population
    2. Sort by fitness
    3. Keep top 2 (elitism)
    4. Fill rest via selection + crossover + mutation
    5. Repeat for N generations
    """
    population      = [random_chromosome() for _ in range(pop_size)]
    best_chromosome = max(population, key=fitness)
    history         = []

    for gen in range(generations):
        population.sort(key=fitness, reverse=True)

        current_best = population[0]
        if fitness(current_best) > fitness(best_chromosome):
            best_chromosome = current_best[:]

        history.append({
            'gen':       gen + 1,
            'best_fit':  fitness(current_best),
            'best_plan': current_best[:]
        })

        # Elitism: keep top 2
        new_population = population[:2]

        # Fill rest
        while len(new_population) < pop_size:
            parent1 = tournament_select(population)
            parent2 = tournament_select(population)
            child   = crossover(parent1, parent2)
            child   = mutate(child)
            new_population.append(child)

        population = new_population

    return best_chromosome, history


# ------------------------------------------------------------------
# Display plan
# ------------------------------------------------------------------
def display_plan(label, chromosome):
    print(f"\n  [{label}]")
    for i, exit_name in enumerate(EXIT_NAMES):
        load   = chromosome[i]
        cap    = EXIT_CAPACITIES[exit_name]
        ratio  = load / cap * 100
        bar    = '█' * int(ratio / 5)
        status = "✓ SAFE" if ratio <= 80 else "✗ OVER"
        print(f"    {exit_name}: {load:4d} people  |  "
              f"{ratio:5.1f}%  {bar:<16}  {status}")
    print(f"    Fitness: {fitness(chromosome):.2f}  (0 = no congestion)")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 65)
    print("  CROWD CONTROL — GENETIC ALGORITHM")
    print("  Operators: Selection + Crossover + Mutation")
    print("=" * 65)

    print("\n[INITIAL POPULATION — 5 Random Plans]")
    for i, chrom in enumerate([random_chromosome() for _ in range(5)], 1):
        print(f"  Plan {i}: {dict(zip(EXIT_NAMES, chrom))}  "
              f"Fitness: {fitness(chrom):.2f}")

    print("\n[RUNNING GA FOR 50 GENERATIONS ...]")
    best, history = genetic_algorithm()

    print("\n[EVOLUTION PROGRESS]")
    print(f"  {'Gen':>4}  {'Best Fitness':>14}  Plan")
    for snap in history[::10]:
        print(f"  {snap['gen']:>4}  {snap['best_fit']:>14.2f}  "
              f"{snap['best_plan']}")
    print(f"  {history[-1]['gen']:>4}  {history[-1]['best_fit']:>14.2f}  "
          f"{history[-1]['best_plan']}")

    display_plan("BEST ROUTING PLAN", best)

    print(f"\n[VERIFICATION]")
    print(f"  Total crowd routed : {sum(best)}")
    print(f"  Expected           : {TOTAL_CROWD}")

    print("\n" + "=" * 65)
    print("  GA evolves solutions over generations.")
    print("  Selection → Crossover → Mutation → Repeat")
    print("=" * 65)
