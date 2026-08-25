from collections import deque

from tsp.problem import tour_length
from algorithms.local_search import run_local_search


def _make_tabu_accept(tabu_tenure):
    tabu_list = deque(maxlen=tabu_tenure)

    def _accept(current_tour, current_length, neighbors, distance_matrix, iteration):
        n = len(current_tour)

        best_move = None       # (i, j) of the best allowed swap found
        best_neighbor = None
        best_neighbor_length = float("inf")

        idx = 0
        for i in range(n):
            for j in range(i + 1, n):
                neighbor = neighbors[idx]
                idx += 1

                move = (i, j)
                length = tour_length(neighbor, distance_matrix)

                is_tabu = move in tabu_list
                is_improving_on_current_best = length < current_length

                if is_tabu and not is_improving_on_current_best:
                    continue

                if length < best_neighbor_length:
                    best_neighbor_length = length
                    best_neighbor = neighbor
                    best_move = move

        if best_neighbor is None:
            return current_tour, current_length, False

        tabu_list.append(best_move)
        return best_neighbor, best_neighbor_length, False
    
    return _accept


def run_tabu_search(distance_matrix, num_cities, max_iterations=500, tabu_tenure=15,
                     starting_tour=None, seed=None):
    accept_fn = _make_tabu_accept(tabu_tenure)
    result = run_local_search(
        distance_matrix, num_cities, accept_fn,
        max_iterations=max_iterations, starting_tour=starting_tour, seed=seed,
    )
    result["method"] = "Tabu Search"
    return result


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    result = run_tabu_search(distance_matrix, len(cities), max_iterations=500, tabu_tenure=15, seed=42)

    print(f"Method: {result['method']}")
    print(f"Best length found: {result['best_length']:.2f} km")
    print(f"Best tour: {[cities[i][0] for i in result['best_tour']]}")

    from algorithms.random_search import run_random_search
    from algorithms.hill_climbing import run_hill_climbing
    from algorithms.simulated_annealing import run_simulated_annealing

    random_result = run_random_search(distance_matrix, len(cities), num_iterations=10000, seed=42)
    hc_result = run_hill_climbing(distance_matrix, len(cities), max_iterations=1000, seed=42)
    sa_result = run_simulated_annealing(distance_matrix, len(cities), max_iterations=5000, seed=42)

    print()
    print(f"Random search:        {random_result['best_length']:.2f} km")
    print(f"Hill climbing:         {hc_result['best_length']:.2f} km")
    print(f"Simulated annealing:    {sa_result['best_length']:.2f} km")
    print(f"Tabu search:             {result['best_length']:.2f} km")