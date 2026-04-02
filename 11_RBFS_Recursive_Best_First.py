# ============================================================
#  TOPIC 11: RECURSIVE BEST FIRST SEARCH (RBFS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Memory-efficient heuristic search
#            Formula: f(n) = max(g(n) + h(n), f_parent)
# ============================================================

# ------------------------------------------------------------------
# Venue Graph
# ------------------------------------------------------------------
graph = {
    'G1': ['C1'],
    'G2': ['C2'],
    'G3': ['C3'],
    'C1': ['G1', 'H1', 'C2'],
    'C2': ['G2', 'C1', 'H2', 'C3'],
    'C3': ['G3', 'C2', 'H2'],
    'H1': ['C1', 'E1', 'S1'],
    'H2': ['C2', 'C3', 'E2', 'S1'],
    'S1': ['H1', 'H2', 'E3'],
    'E1': ['H1'],
    'E2': ['H2'],
    'E3': ['S1']
}

# Heuristic h(n)
heuristic = {
    'G1': 5, 'G2': 5, 'G3': 4,
    'C1': 3, 'C2': 4, 'C3': 3,
    'H1': 2, 'H2': 2,
    'S1': 1,
    'E1': 0, 'E2': 0, 'E3': 0
}

RBFS_INF = float('inf')
exits    = ['E1', 'E2', 'E3']


# ------------------------------------------------------------------
# RBFS — Recursive Best First Search
# ------------------------------------------------------------------
def rbfs(graph, node, goal, g, f_limit, visited=None):
    """
    RBFS: Like A* but memory-efficient.
    Only stores current path — not entire frontier.
    Backtracks when a better alternative exists elsewhere.
    f(n) = max(g(n) + h(n), f_parent) prevents underestimation.
    """
    if visited is None:
        visited = set()

    f = g + heuristic.get(node, 0)

    if f > f_limit:
        return None, f

    if node == goal:
        return [node], f

    visited.add(node)
    successors = []
    for nb in graph.get(node, []):
        if nb not in visited:
            nb_f = g + 1 + heuristic.get(nb, 0)
            successors.append((nb_f, nb))

    if not successors:
        visited.discard(node)
        return None, RBFS_INF

    successors.sort(key=lambda x: x[0])

    while True:
        best_f, best = successors[0]
        if best_f > f_limit:
            visited.discard(node)
            return None, best_f

        alt_f  = successors[1][0] if len(successors) > 1 else RBFS_INF
        result, new_f = rbfs(graph, best, goal, g + 1,
                             min(f_limit, alt_f), visited)
        successors[0] = (new_f, best)
        successors.sort(key=lambda x: x[0])

        if result:
            return [node] + result, new_f


# ------------------------------------------------------------------
# Simplified RBFS — score-based selection
# ------------------------------------------------------------------
def rbfs_simple(scores):
    """
    Simple RBFS: pick corridor with best (lowest) heuristic score.
    """
    best = min(scores, key=scores.get)
    return best, scores[best]


# ------------------------------------------------------------------
# RBFS to nearest exit
# ------------------------------------------------------------------
def rbfs_nearest_exit(graph, start, exits):
    best_result = None
    best_cost   = RBFS_INF

    for ex in exits:
        result, cost = rbfs(graph, start, ex, 0, RBFS_INF)
        if result and cost < best_cost:
            best_result = result
            best_cost   = cost

    return best_result, best_cost


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — RECURSIVE BEST FIRST SEARCH (RBFS)")
    print("  Formula: f(n) = max(g(n) + h(n), f_parent)")
    print("=" * 62)

    print("\n[TEST 1] Simple RBFS — Corridor Scores")
    scores = {
        'C1_to_E1': 2, 'H1_to_E1': 3,
        'H2_to_E2': 4, 'C2_to_E2': 5,
        'S1_to_E3': 7
    }
    print("  Corridor heuristic scores:")
    for corridor, score in sorted(scores.items(), key=lambda x: x[1]):
        bar = '▓' * score
        print(f"    {corridor:15s}  h={score}  [{bar}]")
    best, score = rbfs_simple(scores)
    print(f"\n  Best corridor: {best}  (h={score})")

    print("\n[TEST 2] Full RBFS Paths")
    for src, dst in [('G1','E1'), ('G3','E3'), ('G2','E2'), ('H2','E3')]:
        result, cost = rbfs(graph, src, dst, 0, RBFS_INF)
        if result:
            print(f"  {src} → {dst}: {' → '.join(result)}  f={cost}")
        else:
            print(f"  {src} → {dst}: No path found")

    print("\n[TEST 3] RBFS Nearest Exit")
    for start in ['G1', 'G2', 'G3', 'H1', 'S1']:
        result, cost = rbfs_nearest_exit(graph, start, exits)
        if result:
            print(f"  From {start}: → {result[-1]}  "
                  f"Path: {' → '.join(result)}  f={cost}")

    print("\n[TEST 4] Memory Comparison: A* vs RBFS")
    print("  At depth d with branching b:")
    for b, d in [(3,6),(4,8),(5,10)]:
        astar_mem = b ** d
        rbfs_mem  = b * d
        print(f"  b={b},d={d}: A* memory={astar_mem:,}  "
              f"RBFS memory={rbfs_mem}  "
              f"Ratio={round(astar_mem/rbfs_mem)}x")

    print("\n" + "=" * 62)
    print("  RBFS: memory-efficient A* for embedded sensors.")
    print("  Stores only current path — not full frontier.")
    print("=" * 62)
