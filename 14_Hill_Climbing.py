# ============================================================
#  TOPIC 14: HILL CLIMBING
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Improve crowd distribution across exits by
#            continuously moving toward lower congestion
#            Only accepts improvements — no backtracking
# ============================================================

import random

random.seed(42)

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
EXIT_CAPACITIES = {'E1': 500, 'E2': 400, 'E3': 300}
TOTAL_CROWD     = 1000
SAFE_THRESHOLD  = 0.80


# ------------------------------------------------------------------
# Cost Function — total congestion penalty
# ------------------------------------------------------------------
def congestion_cost(routes):
    """
    Penalty for exits above 80% capacity.
    Lower cost = safer, better balanced distribution.
    """
    penalty = 0.0
    for exit_name, load in routes.items():
        cap   = EXIT_CAPACITIES[exit_name]
        ratio = load / cap
        if ratio > SAFE_THRESHOLD:
            penalty += (ratio - SAFE_THRESHOLD) * 1000
    return penalty


# ------------------------------------------------------------------
# Hill Climbing — Basic
# ------------------------------------------------------------------
def hill_climbing(initial_routes, max_steps=500):
    """
    Iteratively moves to a better neighbor.
    Only accepts moves that REDUCE congestion cost.
    Stops when no neighbor improves — local optimum.
    """
    current     = initial_routes.copy()
    best        = current.copy()
    steps_taken = 0

    for step in range(max_steps):
        # Generate all neighbors
        neighbors  = []
        exit_names = list(current.keys())
        for i in range(len(exit_names)):
            for j in range(len(exit_names)):
                if i != j:
                    amount = 20
                    if current[exit_names[i]] >= amount:
                        neighbor = current.copy()
                        neighbor[exit_names[i]] -= amount
                        neighbor[exit_names[j]] += amount
                        neighbors.append(neighbor)

        # Find best neighbor
        best_neighbor = min(neighbors, key=congestion_cost)

        # Only move if improvement exists
        if congestion_cost(best_neighbor) < congestion_cost(current):
            current     = best_neighbor
            steps_taken = step + 1
            if congestion_cost(current) < congestion_cost(best):
                best = current.copy()
        else:
            break  # Local optimum

    return best, steps_taken, congestion_cost(best)


# ------------------------------------------------------------------
# Hill Climbing — with Random Restarts
# ------------------------------------------------------------------
def hill_climbing_restarts(n_restarts=5, max_steps=500):
    """
    Runs Hill Climbing from multiple random starting points.
    Overcomes local optima limitation of basic Hill Climbing.
    Returns the best solution across all restarts.
    """
    global_best      = None
    global_best_cost = float('inf')

    for restart in range(n_restarts):
        # Random starting distribution
        splits = sorted([random.randint(0, TOTAL_CROWD) for _ in range(2)])
        initial = {
            'E1': splits[0],
            'E2': splits[1] - splits[0],
            'E3': TOTAL_CROWD - splits[1]
        }

        result, steps, final_cost = hill_climbing(initial, max_steps)

        if final_cost < global_best_cost:
            global_best      = result.copy()
            global_best_cost = final_cost

    return global_best, global_best_cost


# ------------------------------------------------------------------
# Display routing
# ------------------------------------------------------------------
def display_routing(label, routes):
    print(f"\n  [{label}]")
    for ex, load in sorted(routes.items()):
        cap    = EXIT_CAPACITIES[ex]
        ratio  = load / cap * 100
        bar    = '█' * int(ratio / 5)
        status = "✓ SAFE" if ratio <= 80 else "✗ OVER"
        print(f"    {ex}: {load:4d} people  |  "
              f"{ratio:5.1f}%  {bar:<16}  {status}")
    print(f"    Cost: {congestion_cost(routes):.1f}")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — HILL CLIMBING")
    print("=" * 62)

    print("\n[TEST 1] Basic Hill Climbing — Three Scenarios")
    scenarios = [
        ("Overloaded E1",   {'E1': 700, 'E2': 200, 'E3': 100}),
        ("Heavy E1 & E2",   {'E1': 500, 'E2': 400, 'E3': 100}),
        ("Near Optimal",    {'E1': 380, 'E2': 320, 'E3': 300}),
    ]

    for label, initial in scenarios:
        print(f"\n  Scenario: {label}")
        display_routing("Initial", initial)
        best, steps, final_cost = hill_climbing(initial)
        display_routing(f"After Hill Climbing ({steps} steps)", best)

    print("\n[TEST 2] Hill Climbing with Random Restarts (5 restarts)")
    best, best_cost = hill_climbing_restarts(n_restarts=5)
    display_routing("Best across 5 Restarts", best)

    print("\n[TEST 3] Hill Climbing vs Simulated Annealing Comparison")
    print("  Hill Climbing:")
    print("    ✓ Faster — fewer iterations needed")
    print("    ✓ Simple — always move to better neighbor")
    print("    ✗ Can get stuck at local optima")
    print("    ✗ No exploration — purely exploitative")
    print()
    print("  Simulated Annealing:")
    print("    ✓ Escapes local optima via probabilistic acceptance")
    print("    ✓ Finds globally better solutions")
    print("    ✗ Slower — needs many iterations to cool")

    print("\n" + "=" * 62)
    print("  Hill Climbing: always move to better neighbor.")
    print("  Stops at LOCAL optimum — may miss global best.")
    print("  Use random restarts to overcome this limitation.")
    print("=" * 62)
