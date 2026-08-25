from tsp.problem import tour_length, random_tour
from tsp.neighborhood import all_swap_neighbors


def run_local_search(distance_matrix, num_cities, accept_fn, max_iterations=1000,
                      starting_tour=None, seed=None):
    import random
    if seed is not None:
        random.seed(seed)

    current_tour = starting_tour if starting_tour is not None else random_tour(num_cities)
    current_length = tour_length(current_tour, distance_matrix)

    best_tour = current_tour
    best_length = current_length
    history = [best_length]

    for iteration in range(max_iterations):
        neighbors = all_swap_neighbors(current_tour)

        current_tour, current_length, should_stop = accept_fn(
            current_tour, current_length, neighbors, distance_matrix, iteration
        )

        if current_length < best_length:
            best_length = current_length
            best_tour = current_tour

        history.append(best_length)

        if should_stop:
            break

    return {
        "method": None,
        "best_tour": best_tour,
        "best_length": best_length,
        "history": history,
    }


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    def _always_take_first_neighbor(current_tour, current_length, neighbors, distance_matrix, iteration):
        next_tour = neighbors[0]
        next_length = tour_length(next_tour, distance_matrix)
        return next_tour, next_length, False

    result = run_local_search(
        distance_matrix, len(cities), _always_take_first_neighbor,
        max_iterations=50, seed=42,
    )

    print("Testing generic local search engine with a trivial accept_fn:")
    print(f"Best length found: {result['best_length']:.2f} km")
    print(f"History length: {len(result['history'])} (expected 51: 1 initial + 50 iterations)")

    is_non_increasing = all(
        result["history"][i] >= result["history"][i + 1]
        for i in range(len(result["history"]) - 1)
    )
    print(f"History is non-increasing: {is_non_increasing}")