from tsp.problem import load_cities, build_distance_matrix
from algorithms.random_search import run_random_search
from algorithms.hill_climbing import run_hill_climbing
from algorithms.simulated_annealing import run_simulated_annealing
from algorithms.tabu_search import run_tabu_search
from algorithms.genetic_algorithm import run_genetic_algorithm
from visualization.plot_tour import plot_tour
from visualization.plot_comparison import plot_comparison_bars, plot_convergence

SEED = 40


def run_all_methods(distance_matrix, num_cities):
    # Iteration budgets differ on purpose -- see the note in
    # plot_comparison.py about iteration cost not being comparable
    # across methods. These are the same budgets used in each
    # algorithm's own __main__ block, kept here so main.py is the
    # single source of truth for the final comparison run.
    return [
        run_random_search(distance_matrix, num_cities, num_iterations=10000, seed=SEED),
        run_hill_climbing(distance_matrix, num_cities, max_iterations=1000, seed=SEED),
        run_simulated_annealing(distance_matrix, num_cities, max_iterations=5000, seed=SEED),
        run_tabu_search(distance_matrix, num_cities, max_iterations=500, seed=SEED),
        run_genetic_algorithm(distance_matrix, num_cities, population_size=50,
                               num_generations=300, seed=SEED),
    ]


def print_summary(results):
    best = min(results, key=lambda r: r["best_length"])

    print(f"{'Method':<22s} {'Best length (km)':>18s}")
    print("-" * 42)
    for r in results:
        marker = "  <-- best" if r["method"] == best["method"] else ""
        print(f"{r['method']:<22s} {r['best_length']:>18.2f}{marker}")

    worst = max(results, key=lambda r: r["best_length"])
    improvement = (1 - best["best_length"] / worst["best_length"]) * 100
    print(f"\nBest method: {best['method']} "
          f"({improvement:.1f}% shorter than worst method, {worst['method']})")


def save_all_plots(results, cities, distance_matrix):
    for r in results:
        # Filenames from method name: "Simulated Annealing" -> "simulated_annealing_tour.png"
        slug = r["method"].lower().replace(" ", "_")
        plot_tour(
            r["best_tour"], cities, distance_matrix,
            title=r["method"], save_path=f"results/{slug}_tour.png", show=False,
        )

    plot_comparison_bars(results, save_path="results/comparison_bars.png", show=False)
    plot_convergence(results, save_path="results/convergence.png", show=False)


def main():
    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)
    num_cities = len(cities)

    print(f"Loaded {num_cities} Algerian cities. Running all 5 metaheuristics (seed={SEED})...\n")

    results = run_all_methods(distance_matrix, num_cities)
    print_summary(results)

    save_all_plots(results, cities, distance_matrix)
    print(f"\nSaved {len(results)} tour plots, comparison_bars.png, and convergence.png to results/")


if __name__ == "__main__":
    main()