import matplotlib.pyplot as plt


METHOD_COLORS = {
    "Random Search": "gray",
    "Hill Climbing": "darkorange",
    "Simulated Annealing": "seagreen",
    "Tabu Search": "steelblue",
    "Genetic Algorithm": "crimson",
}


def plot_comparison_bars(results, save_path=None, show=True):
    methods = [r["method"] for r in results]
    lengths = [r["best_length"] for r in results]
    colors = [METHOD_COLORS.get(m, "black") for m in methods]

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(methods, lengths, color=colors)

    # Label each bar with its value directly above it -- easier to read
    # exact numbers off the chart than to eyeball bar heights.
    for bar, length in zip(bars, lengths):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                 f"{length:.0f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylabel("Best tour length (km)")
    ax.set_title("Best distance found per method")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def plot_convergence(results, save_path=None, show=True):
    fig, ax = plt.subplots(figsize=(9, 6))

    for r in results:
        method = r["method"]
        history = r["history"]
        # x-axis is just "how many steps has this method taken" -- not
        # directly comparable across methods (one iteration of random
        # search costs one tour evaluation; one iteration of hill
        # climbing costs up to 190 -- see note below), but it still shows
        # each method's OWN improvement curve clearly.
        ax.plot(range(len(history)), history, label=method,
                 color=METHOD_COLORS.get(method, "black"), linewidth=1.5)

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best-so-far length (km)")
    ax.set_title("Convergence: best-so-far length over iterations")
    ax.legend()
    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix
    from algorithms.random_search import run_random_search
    from algorithms.hill_climbing import run_hill_climbing
    from algorithms.simulated_annealing import run_simulated_annealing
    from algorithms.tabu_search import run_tabu_search
    from algorithms.genetic_algorithm import run_genetic_algorithm

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)
    n = len(cities)

    results = [
        run_random_search(distance_matrix, n, num_iterations=10000, seed=42),
        run_hill_climbing(distance_matrix, n, max_iterations=1000, seed=42),
        run_simulated_annealing(distance_matrix, n, max_iterations=5000, seed=42),
        run_tabu_search(distance_matrix, n, max_iterations=500, seed=42),
        run_genetic_algorithm(distance_matrix, n, population_size=50, num_generations=300, seed=42),
    ]

    for r in results:
        print(f"{r['method']:<22s} {r['best_length']:.2f} km")

    plot_comparison_bars(results, save_path="results/comparison_bars.png", show=False)
    plot_convergence(results, save_path="results/convergence.png", show=False)
    print("\nSaved results/comparison_bars.png and results/convergence.png")