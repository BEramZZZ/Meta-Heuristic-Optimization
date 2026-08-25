import csv
import math
import random

DEFAULT_CSV_PATH = "data/algeria_20_cities_xy.csv"


def load_cities(csv_path=DEFAULT_CSV_PATH):
    cities = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["city"].strip()
            x = float(row["x_km"])
            y = float(row["y_km"])
            cities.append((name, x, y))

    algiers_index = next((i for i, c in enumerate(cities) if c[0] == "Algiers"), None)
    if algiers_index is None:
        raise ValueError("No city named 'Algiers' found in the CSV -- check the 'city' column.")

    if algiers_index != 0:
        cities[0], cities[algiers_index] = cities[algiers_index], cities[0]

    return cities


def build_distance_matrix(cities):
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = cities[i][1], cities[i][2]
        for j in range(i + 1, n):
            xj, yj = cities[j][1], cities[j][2]
            d = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def tour_length(tour, distance_matrix):
    total = 0.0
    n = len(tour)
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]  # wraps last city back to the first -- closes the loop
        total += distance_matrix[a][b]
    return total


def random_tour(num_cities):
    indices = list(range(num_cities))
    random.shuffle(indices)
    return indices


if __name__ == "__main__":
    cities = load_cities()
    print(f"Loaded {len(cities)} cities. Index 0 is: {cities[0][0]}")
    print()
    for i, (name, x, y) in enumerate(cities):
        print(f"{i:2d}  {name:<20s} x={x:10.3f}  y={y:10.3f}")

    distance_matrix = build_distance_matrix(cities)
    
    print()
    print(f"Algiers -> Annaba distance: {distance_matrix[0][[c[0] for c in cities].index('Annaba')]:.2f} km")
    print(f"Algiers -> Oran distance:   {distance_matrix[0][[c[0] for c in cities].index('Oran')]:.2f} km")

    random.seed(42)
    tour = random_tour(len(cities))
    length = tour_length(tour, distance_matrix)
    print()
    print(f"Random tour (seed=42): {[cities[i][0] for i in tour]}")
    print(f"Random tour length: {length:.2f} km")