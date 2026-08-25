import random

from tsp.problem import tour_length, random_tour
from tsp.neighborhood import swap_neighbor


def initialize_population(num_cities, population_size):
    return [random_tour(num_cities) for _ in range(population_size)]


def evaluate_population(population, distance_matrix):
    lengths = [tour_length(individual, distance_matrix) for individual in population]
    fitness = [1.0 / (1.0 + length) for length in lengths]
    return lengths, fitness


def roulette_wheel_selection(population, fitness, num_to_select):
    total_fitness = sum(fitness)
    probabilities = [f / total_fitness for f in fitness]

    cumulative = []
    running_total = 0.0
    for p in probabilities:
        running_total += p
        cumulative.append(running_total)

    selected = []
    for _ in range(num_to_select):
        r = random.random()
        for i, cumulative_p in enumerate(cumulative):
            if r <= cumulative_p:
                selected.append(population[i])
                break
        else:
            selected.append(population[-1])

    return selected


def order_crossover(parent1, parent2):
    n = len(parent1)
    i, j = sorted(random.sample(range(n), 2))

    child = [None] * n
    child[i:j + 1] = parent1[i:j + 1]
    kept = set(child[i:j + 1])

    fill_values = [city for city in parent2 if city not in kept]

    fill_idx = 0
    for pos in range(n):
        if child[pos] is None:
            child[pos] = fill_values[fill_idx]
            fill_idx += 1

    return child


def mutate(tour, mutation_rate):
    if random.random() < mutation_rate:
        return swap_neighbor(tour)
    return tour


def run_genetic_algorithm(distance_matrix, num_cities, population_size=50,
                           num_generations=300, crossover_rate=0.8, mutation_rate=0.15,
                           elitism_count=2, stagnation_limit=60, seed=None):
    if seed is not None:
        random.seed(seed)

    population = initialize_population(num_cities, population_size)

    best_tour = None
    best_length = float("inf")
    generations_since_improvement = 0
    history = []

    for generation in range(num_generations):
        # Phase 2: Evaluation
        lengths, fitness = evaluate_population(population, distance_matrix)

        generation_best_idx = min(range(population_size), key=lambda i: lengths[i])
        generation_best_length = lengths[generation_best_idx]

        if generation_best_length < best_length:
            best_length = generation_best_length
            best_tour = population[generation_best_idx][:]
            generations_since_improvement = 0
        else:
            generations_since_improvement += 1

        history.append(best_length)

        if generations_since_improvement >= stagnation_limit:
            break  # "si pas d'evolution" -- no improvement in a while, stop

        # Elitism: carry the current best few unchanged into next generation.
        sorted_indices = sorted(range(population_size), key=lambda i: lengths[i])
        new_population = [population[i][:] for i in sorted_indices[:elitism_count]]

        # Phase 3: Selection (roulette wheel)
        selected = roulette_wheel_selection(population, fitness, population_size)

        # Phase 4: Reproduction (crossover + mutation) to fill the rest
        while len(new_population) < population_size:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)

            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]

            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        # Phase 5: loop back to Evaluation (top of the for loop)

    return {
        "method": "Genetic Algorithm",
        "best_tour": best_tour,
        "best_length": best_length,
        "history": history,
    }


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    # Sanity check on the crossover operator alone, before running the
    # full algorithm: confirm OX always produces a valid permutation,
    # since that's the one thing the course's cut-point example CAN'T
    # guarantee for TSP and the whole reason OX replaces it.
    random.seed(0)
    p1 = list(range(10))
    p2 = list(range(10))
    random.shuffle(p2)
    for _ in range(200):
        child = order_crossover(p1, p2)
        assert sorted(child) == list(range(10)), f"Invalid child produced: {child}"
    print("Order crossover sanity check: 200/200 children were valid permutations.\n")

    result = run_genetic_algorithm(
        distance_matrix, len(cities),
        population_size=50, num_generations=300, crossover_rate=0.8,
        mutation_rate=0.15, elitism_count=2, stagnation_limit=60, seed=42,
    )

    print(f"Method: {result['method']}")
    print(f"Best length found: {result['best_length']:.2f} km")
    print(f"Best tour: {[cities[i][0] for i in result['best_tour']]}")
    print(f"Stopped after {len(result['history'])} generations (out of max 300)")

    from algorithms.random_search import run_random_search
    from algorithms.hill_climbing import run_hill_climbing
    from algorithms.simulated_annealing import run_simulated_annealing
    from algorithms.tabu_search import run_tabu_search

    random_result = run_random_search(distance_matrix, len(cities), num_iterations=10000, seed=42)
    hc_result = run_hill_climbing(distance_matrix, len(cities), max_iterations=1000, seed=42)
    sa_result = run_simulated_annealing(distance_matrix, len(cities), max_iterations=5000, seed=42)
    ts_result = run_tabu_search(distance_matrix, len(cities), max_iterations=500, seed=42)

    print()
    print(f"Random search:        {random_result['best_length']:.2f} km")
    print(f"Hill climbing:         {hc_result['best_length']:.2f} km")
    print(f"Simulated annealing:    {sa_result['best_length']:.2f} km")
    print(f"Tabu search:              {ts_result['best_length']:.2f} km")
    print(f"Genetic algorithm:          {result['best_length']:.2f} km")