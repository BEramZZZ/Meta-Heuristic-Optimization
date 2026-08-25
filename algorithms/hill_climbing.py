from tsp.problem import tour_length
from algorithms.local_search import run_local_search


def _hill_climbing_accept(current_tour, current_length, neighbors, distance_matrix, iteration):
    best_neighbor = None
    best_neighbor_length = float("inf")

    for neighbor in neighbors:
        length = tour_length(neighbor, distance_matrix)
        if length < best_neighbor_length:
            best_neighbor_length = length
            best_neighbor = neighbor

    if best_neighbor_length < current_length:
        return best_neighbor, best_neighbor_length, False  # improved -- keep climbing
    else:
        return current_tour, current_length, True  # local optimum reached -- stop


def run_hill_climbing(distance_matrix, num_cities, max_iterations=1000, starting_tour=None, seed=None):
    result = run_local_search(
        distance_matrix, num_cities, _hill_climbing_accept,
        max_iterations=max_iterations, starting_tour=starting_tour, seed=seed,
    )
    result["method"] = "Hill Climbing"
    return result


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    result = run_hill_climbing(distance_matrix, len(cities), max_iterations=1000, seed=42)

    print(f"Method: {result['method']}")
    print(f"Best length found: {result['best_length']:.2f} km")
    print(f"Best tour: {[cities[i][0] for i in result['best_tour']]}")
    print(f"Stopped after {len(result['history']) - 1} iterations (out of max 1000)")

    # Compare against random search's baseline from step 3, to confirm
    # hill climbing is actually doing its job.
    from algorithms.random_search import run_random_search
    random_result = run_random_search(distance_matrix, len(cities), num_iterations=10000, seed=42)
    print()
    print(f"Random search (10000 tries): {random_result['best_length']:.2f} km")
    print(f"Hill climbing:                {result['best_length']:.2f} km")
    improvement = (1 - result["best_length"] / random_result["best_length"]) * 100
    print(f"Hill climbing improvement over random search: {improvement:.1f}%")