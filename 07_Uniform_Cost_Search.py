# ============================================================
#  TOPIC 7: UNIFORM COST SEARCH (UCS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Find minimum COST (distance in metres) evacuation
#            route — not just fewest hops
#  Formula : Expand node with lowest cumulative g(n) = Σ w(edges)
# ============================================================

import heapq

# ------------------------------------------------------------------
# Weighted Venue Graph {node: [(neighbor, distance_metres)]}
# ------------------------------------------------------------------
graph = {
    'G1': [('C1', 20)],
    'G2': [('C2', 25)],
    'G3': [('C3', 15)],
    'C1': [('G1', 20), ('H1', 35), ('C2', 40)],
    'C2': [('G2', 25), ('C1', 40), ('H2', 50), ('C3', 30)],
    'C3': [('G3', 15), ('C2', 30), ('H2', 25)],
    'H1': [('C1', 35), ('E1', 20), ('S1', 15)],
    'H2': [('C2', 50), ('C3', 25), ('E2', 20)],
    'S1': [('H1', 15), ('H2', 30), ('E3', 10)],
    'E1': [('H1', 20)],
    'E2': [('H2', 20)],
    'E3': [('S1', 10)]
}

exits = ['E1', 'E2', 'E3']


# ------------------------------------------------------------------
# UCS: Minimum cost path to specific goal
# ------------------------------------------------------------------
def ucs(graph, start, goal):
    """
    Expands node with lowest cumulative cost g(n).
    Guarantees OPTIMAL (minimum distance) solution.
    Priority queue: (cumulative_cost, node, path)
    """
    pq      = [(0, start, [start])]
    visited = {}

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        if node == goal:
            return cost, path, len(visited)

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if visited.get(neighbor, float('inf')) > new_cost:
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return float('inf'), None, len(visited)


# ------------------------------------------------------------------
# UCS: Find cheapest path to any exit
# ------------------------------------------------------------------
def ucs_nearest_exit(graph, start, exits):
    pq      = [(0, start, [start])]
    visited = {}

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        if node in exits:
            return cost, path, len(visited)

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if visited.get(neighbor, float('inf')) > new_cost:
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return float('inf'), None, len(visited)


# ------------------------------------------------------------------
# UCS: Find costs to ALL exits
# ------------------------------------------------------------------
def ucs_all_exits(graph, start, exits):
    pq      = [(0, start, [start])]
    visited = {}
    results = {}

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        if node in exits:
            results[node] = (cost, path)

        if len(results) == len(exits):
            break

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if visited.get(neighbor, float('inf')) > new_cost:
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return results


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — UNIFORM COST SEARCH (UCS)")
    print("  g(n) = Σ w(edges)  |  Expand minimum g(n)")
    print("=" * 62)

    print("\n[TEST 1] UCS Minimum Cost Paths")
    for src, dst in [('G1','E1'), ('G1','E2'), ('G2','E3'),
                     ('G3','E1'), ('H2','E3')]:
        cost, path, n = ucs(graph, src, dst)
        if path:
            print(f"  {src} → {dst}  |  Cost: {cost}m  "
                  f"|  Path: {' → '.join(path)}  |  Nodes: {n}")

    print("\n[TEST 2] Cheapest Exit from Each Gate")
    for gate in ['G1', 'G2', 'G3']:
        cost, path, n = ucs_nearest_exit(graph, gate, exits)
        print(f"  {gate}: Best Exit={path[-1]}  Cost={cost}m  "
              f"Path: {' → '.join(path)}")

    print("\n[TEST 3] All Exit Costs from Hall H1")
    results = ucs_all_exits(graph, 'H1', exits)
    for ex in sorted(results):
        cost, path = results[ex]
        print(f"  → {ex}  Cost: {cost}m  Path: {' → '.join(path)}")

    print("\n[TEST 4] Cost Table: All Locations → All Exits")
    print(f"  {'':5}", end="")
    for ex in exits:
        print(f"  {ex:>8}", end="")
    print()
    for loc in ['G1','G2','G3','H1','H2','S1']:
        print(f"  {loc:5}", end="")
        for ex in exits:
            cost, _, _ = ucs(graph, loc, ex)
            print(f"  {str(cost)+'m':>8}", end="")
        print()

    print("\n" + "=" * 62)
    print("  UCS guarantees MINIMUM COST path.")
    print("  Complete and optimal for non-negative weights.")
    print("=" * 62)
