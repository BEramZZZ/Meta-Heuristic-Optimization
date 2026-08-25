import random


def swap_neighbor(tour):
    new_tour = tour[:]
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour


def all_swap_neighbors(tour):
    neighbors = []
    n = len(tour)
    for i in range(n):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            neighbors.append(new_tour)
    return neighbors


def two_opt_neighbor(tour):
    new_tour = tour[:]
    i, j = sorted(random.sample(range(len(tour)), 2))
    new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
    return new_tour


def all_two_opt_neighbors(tour):
    neighbors = []
    n = len(tour)
    for i in range(n):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
            neighbors.append(new_tour)
    return neighbors


if __name__ == "__main__":
    random.seed(0)
    tour = list(range(6))  # a small fake tour: [0, 1, 2, 3, 4, 5]
    print(f"Original tour: {tour}")

    swapped = swap_neighbor(tour)
    print(f"One random swap neighbor: {swapped}")
    print(f"Original unchanged (not mutated)? {tour == [0, 1, 2, 3, 4, 5]}")

    reversed_tour = two_opt_neighbor(tour)
    print(f"One random 2-opt neighbor: {reversed_tour}")

    all_swaps = all_swap_neighbors(tour)
    print(f"\nTotal swap neighbors for a 6-city tour: {len(all_swaps)} (expected {6 * 5 // 2})")

    all_2opt = all_two_opt_neighbors(tour)
    print(f"Total 2-opt neighbors for a 6-city tour: {len(all_2opt)} (expected {6 * 5 // 2})")

    # Sanity check: every neighbor must still be a valid permutation of the
    # same 6 cities -- no city lost, none duplicated, by any operator.
    all_valid_swaps = all(sorted(n) == sorted(tour) for n in all_swaps)
    all_valid_2opt = all(sorted(n) == sorted(tour) for n in all_2opt)
    print(f"\nAll swap neighbors are valid permutations: {all_valid_swaps}")
    print(f"All 2-opt neighbors are valid permutations: {all_valid_2opt}")