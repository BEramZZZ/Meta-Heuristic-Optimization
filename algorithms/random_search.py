from tsp.problem import random_tour, tour_length


def run_random_search(distance_matrix, num_cities, num_iterations=10000, seed=None):
    import random
    if seed is not None:
        random.seed(seed)

    best_tour = None
    best_length = float("inf")
    history = []

    for _ in range(num_iterations):
        candidate = random_tour(num_cities)
        candidate_length = tour_length(candidate, distance_matrix)

        if candidate_length < best_length:
            best_length = candidate_length
            best_tour = candidate

        history.append(best_length)

    return {
        "method": "Random Search",
        "best_tour": best_tour,
        "best_length": best_length,
        "history": history,
    }


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    result = run_random_search(distance_matrix, len(cities), num_iterations=10000, seed=42)

    print(f"Method: {result['method']}")
    print(f"Best length found: {result['best_length']:.2f} km")
    print(f"Best tour: {[cities[i][0] for i in result['best_tour']]}")
    print()
    print(f"History length: {len(result['history'])} (one entry per iteration)")
    print(f"First 5 best-so-far values: {[round(v, 1) for v in result['history'][:5]]}")
    print(f"Last 5 best-so-far values:  {[round(v, 1) for v in result['history'][-5:]]}")

    # Sanity check: history must be non-increasing -- "best so far" can
    # only stay the same or improve, it should never get worse.
    is_non_increasing = all(
        result["history"][i] >= result["history"][i + 1]
        for i in range(len(result["history"]) - 1)
    )
    print(f"\nHistory is non-increasing (best-so-far never gets worse): {is_non_increasing}")