import matplotlib.pyplot as plt

from tsp.problem import tour_length


def plot_tour(tour, cities, distance_matrix, title=None, save_path=None, show=True):
    n = len(tour)

    # tour is a list of indices, e.g. [0, 5, 3, ...]. To draw the closed
    # loop we need the x,y of each city in visiting order, PLUS the first
    # city repeated at the end -- that's what actually closes the line
    # back to the start on the plot (matplotlib won't do it for you).
    ordered_x = [cities[tour[i]][1] for i in range(n)] + [cities[tour[0]][1]]
    ordered_y = [cities[tour[i]][2] for i in range(n)] + [cities[tour[0]][2]]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Path first, so city markers/labels sit on top of it, not under it.
    ax.plot(ordered_x, ordered_y, "-", color="steelblue", linewidth=1.5, zorder=1)

    # All cities as dots.
    all_x = [c[1] for c in cities]
    all_y = [c[2] for c in cities]
    ax.scatter(all_x, all_y, color="steelblue", s=60, zorder=2)

    # Algiers (index 0) drawn separately, on top, so it's visually distinct
    # as the fixed start/end point of the loop.
    ax.scatter([cities[0][1]], [cities[0][2]], color="crimson", s=140,
               zorder=3, label="Algiers (start/end)")

    for name, x, y in cities:
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, 6), fontsize=8)

    length = tour_length(tour, distance_matrix)
    plot_title = title if title is not None else "TSP Tour"
    ax.set_title(f"{plot_title} — {length:.2f} km")
    ax.set_xlabel("x (km)")
    ax.set_ylabel("y (km)")
    ax.legend()
    ax.set_aspect("equal", adjustable="datalim")

    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    plt.close(fig)


if __name__ == "__main__":
    from tsp.problem import load_cities, build_distance_matrix
    from algorithms.hill_climbing import run_hill_climbing

    cities = load_cities()
    distance_matrix = build_distance_matrix(cities)

    result = run_hill_climbing(distance_matrix, len(cities), max_iterations=1000, seed=42)

    plot_tour(
        result["best_tour"], cities, distance_matrix,
        title="Hill Climbing", save_path="results/hill_climbing_tour.png", show=False,
    )
    print(f"Saved plot to results/hill_climbing_tour.png ({result['best_length']:.2f} km)")