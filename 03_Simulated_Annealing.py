# ============================================================
#  TOPIC 3: SIMULATED ANNEALING (SA)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Optimally distribute crowd flow across exits
#            to minimize congestion — P = e^(-ΔE/T)
# ============================================================

import math
import random

random.seed(42)

# ------------------------------------------------------------------
# Venue Configuration
# ------------------------------------------------------------------
EXIT_CAPACITIES = {'E1': 500, 'E2': 400, 'E3': 300}
TOTAL_CROWD     = 1000
SAFE_THRESHOLD  = 0.80


# ------------------------------------------------------------------
# Cost Function
# ------------------------------------------------------------------
def cost(routes):
    """
    Calculates congestion penalty. Lower = better distribution.
    Penalty triggers when exit exceeds 80% of capacity.
    """
    penalty = 0.0
    for exit_name, load in routes.items():
        capacity = EXIT_CAPACITIES[exit_name]
        ratio    = load / capacity
        if ratio > SAFE_THRESHOLD:
            penalty += (ratio - SAFE_THRESHOLD) * 1000
        if ratio > 1.0:
            penalty += (ratio - 1.0) * 5000
    return penalty


# ------------------------------------------------------------------
# Perturbation — generate neighboring solution
# ------------------------------------------------------------------
def perturb(routes):
    """
    Shifts a small random number of people between two exits.
    Maintains total crowd count = TOTAL_CROWD.
    """
    new_routes = routes.copy()
    exits      = list(new_routes.keys())
    a, b       = random.sample(exits, 2)
    amount     = random.randint(5, 40)
    if new_routes[a] >= amount:
        new_routes[a] -= amount
        new_routes[b] += amount
    return new_routes


# ------------------------------------------------------------------
# Simulated Annealing
# ------------------------------------------------------------------
def simulated_annealing(initial_routes, T=1000.0, cooling=0.95,
                         min_T=0.1, max_iter=5000):
    """
    SA optimization loop.
    Acceptance probability: P = e^(-delta/T)
    Cooling schedule      : T = T * cooling
    """
    current   = initial_routes.copy()
    best      = current.copy()
    history   = []
    iteration = 0

    while T > min_T and iteration < max_iter:
        neighbor = perturb(current)
        delta    = cost(neighbor) - cost(current)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor

        if cost(current) < cost(best):
            best = current.copy()

        history.append(cost(current))
        T         *= cooling
        iteration += 1

    return best, history


# ------------------------------------------------------------------
# Utility: Print routing summary
# ------------------------------------------------------------------
def print_routing(label, routes):
    print(f"\n  [{label}]")
    for exit_name, load in sorted(routes.items()):
        cap    = EXIT_CAPACITIES[exit_name]
        ratio  = load / cap * 100
        bar    = '█' * int(ratio / 5)
        status = "✓ SAFE" if ratio <= 80 else "✗ OVER"
        print(f"    {exit_name}: {load:4d} people  |  {ratio:5.1f}%  {bar:<16}  {status}")
    print(f"    Cost : {cost(routes):.2f}")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 65)
    print("  CROWD CONTROL — SIMULATED ANNEALING")
    print("  Acceptance Probability : P = e^(-ΔE / T)")
    print("  Cooling Schedule       : T = T × 0.95")
    print("=" * 65)

    scenarios = [
        ("Unbalanced",   {'E1': 600, 'E2': 300, 'E3': 100}),
        ("All One Exit", {'E1': 900, 'E2':  60, 'E3':  40}),
        ("Near Optimal", {'E1': 390, 'E2': 310, 'E3': 300}),
    ]

    for label, initial in scenarios:
        print(f"\n{'='*40}")
        print(f"  SCENARIO: {label}")
        print_routing("Initial", initial)
        best, hist = simulated_annealing(initial)
        print_routing("After SA Optimization", best)
        print(f"  Improvement: {cost(initial):.1f} → {min(hist):.1f}  "
              f"({round((1-min(hist)/cost(initial))*100)}% better)")

    print("\n" + "=" * 65)
    print("  SA escapes local optima by accepting worse solutions")
    print("  probabilistically — controlled by temperature T.")
    print("=" * 65)
