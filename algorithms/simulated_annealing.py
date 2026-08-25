import math
import random
from collections import deque

from tsp.problem import tour_length, random_tour
from tsp.neighborhood import swap_neighbor
from algorithms.local_search import run_local_search


def estimate_initial_temperature(distance_matrix, starting_tour, num_samples=50,
                                  target_acceptance=0.8):
    current_length = tour_length(starting_tour, distance_matrix)
    worsening_deltas = []

    for _ in range(num_samples):
        candidate = swap_neighbor(starting_tour)
        candidate_length = tour_length(candidate, distance_matrix)
        delta = candidate_length - current_length
        if delta > 0:
            worsening_deltas.append(delta)

    if not worsening_deltas:
        return 1.0

    avg_delta = sum(worsening_deltas) / len(worsening_deltas)
    T0 = -avg_delta / math.log(target_acceptance)
    return T0


def build_temperature_schedule(T0, alpha, num_iterations):
    schedule = []
    T = T0
    for _ in range(num_iterations):
        schedule.append(T)
        T *= alpha
    return schedule


def _make_annealing_accept(schedule, epsilon, min_temperature, window_size=100):
    recent_lengths = deque(maxlen=window_size)

    def _accept(current_tour, current_length, neighbors, distance_matrix, iteration):
        temperature = schedule[iteration] if iteration < len(schedule) else schedule[-1]

        candidate = swap_neighbor(current_tour)
        candidate_length = tour_length(candidate, distance_matrix)

        delta = candidate_length - current_length

        if delta < 0:
            accept = True  # improvement -- always taken, matches "Si delta > 0" branch (their delta, opposite sign)
        elif temperature < 1e-12:
            accept = False  # avoid dividing by ~0
        else:
            probability = math.exp(-delta / temperature)
            accept = random.random() < probability

        new_current_length = candidate_length if accept else current_length
        recent_lengths.append(new_current_length)

        should_stop = (
            temperature < min_temperature
            and len(recent_lengths) == window_size
            and (max(recent_lengths) - min(recent_lengths)) < epsilon
        )

        if accept:
            return candidate, candidate_length, should_stop
        else:
            return current_tour, current_length, should_stop

    return _accept


def run_simulated_annealing(distance_matrix, num_cities, max_iterations=5000, alpha=0.995,
                             target_acceptance=0.8, num_samples=50,
                             epsilon=15.0, min_temperature=1.0, window_size=100,
                             starting_tour=None, seed=None):
    if seed is not None:
        random.seed(seed)

    starting_tour = starting_tour if starting_tour is not None else random_tour(num_cities)
    T0 = estimate_initial_temperature(distance_matrix, starting_tour, num_samples, target_acceptance)
    schedule = build_temperature_schedule(T0, alpha, max_iterations)
    accept_fn = _make_annealing_accept(schedule, epsilon, min_temperature, window_size)

    # seed=None here on purpose: we already seeded above (if requested),
    # and estimate_initial_temperature's own sampling already consumed
    # some random numbers -- reseeding now would just discard that state
    # rather than continue it.
    result = run_local_search(
        distance_matrix, num_cities, accept_fn,
        max_iterations=max_iterations, starting_tour=starting_tour, seed=None,
    )
    result["method"] = "Simulated Annealing"
    result["initial_temperature"] = T0
    return result


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    result = run_simulated_annealing(
        distance_matrix, len(cities),
        max_iterations=5000, alpha=0.995, target_acceptance=0.8, seed=42,
    )

    print(f"Method: {result['method']}")
    print(f"Estimated T0: {result['initial_temperature']:.2f}")
    print(f"Best length found: {result['best_length']:.2f} km")
    print(f"Best tour: {[cities[i][0] for i in result['best_tour']]}")
    print(f"Stopped after {len(result['history']) - 1} iterations (out of max 5000)")

    from algorithms.random_search import run_random_search
    from algorithms.hill_climbing import run_hill_climbing

    random_result = run_random_search(distance_matrix, len(cities), num_iterations=10000, seed=42)
    hc_result = run_hill_climbing(distance_matrix, len(cities), max_iterations=1000, seed=42)

    print()
    print(f"Random search:        {random_result['best_length']:.2f} km")
    print(f"Hill climbing:         {hc_result['best_length']:.2f} km")
    print(f"Simulated annealing:    {result['best_length']:.2f} km")