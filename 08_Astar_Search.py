# ============================================================
#  TOPIC 8: A* SEARCH
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Optimal evacuation routing combining actual cost
#            and heuristic estimate
#  Formula : f(n) = g(n) + h(n)
# ============================================================

import heapq

# ------------------------------------------------------------------
# Weighted Venue Graph
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

# Heuristic h(n) — estimated metres to nearest exit
heuristic_nearest = {
    'G1': 75, 'G2': 65, 'G3': 60,
    'C1': 55, 'C2': 55, 'C3': 45,
    'H1': 20, 'H2': 20,
    'S1': 10,
    'E1':  0, 'E2':  0, 'E3':  0
}

# Heuristic to E3 specifically
heuristic_to_E3 = {
    'G1': 80, 'G2': 105, 'G3': 65,
    'C1': 60, 'C2':  85, 'C3': 60,
    'H1': 25, 'H2':  65,
    'S1': 10,
    'E1': 45, 'E2':  50, 'E3':  0
}

exits = ['E1', 'E2', 'E3']


# ------------------------------------------------------------------
# A* Search: path to specific goal
# ------------------------------------------------------------------
def astar(graph, heuristic, start, goal):
    """
    f(n) = g(n) + h(n)
    g(n) = actual cost from start to n
    h(n) = heuristic estimate from n to goal
    Always expands node with lowest f(n).
    Optimal with admissible heuristic h(n) <= h*(n).
    """
    pq      = [(heuristic.get(start, 0), 0, start, [start])]
    visited = {}

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= g:
            continue
        visited[node] = g

        if node == goal:
            return g, path, len(visited)

        for neighbor, weight in graph.get(node, []):
            new_g = g + weight
            if visited.get(neighbor, float('inf')) > new_g:
                new_h = heuristic.get(neighbor, 0)
                heapq.heappush(pq,
                    (new_g + new_h, new_g, neighbor, path + [neighbor]))

    return float('inf'), None, len(visited)


# ------------------------------------------------------------------
# A* to nearest exit
# ------------------------------------------------------------------
def astar_nearest_exit(graph, heuristic, start, exits):
    pq      = [(heuristic.get(start, 0), 0, start, [start])]
    visited = {}

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= g:
            continue
        visited[node] = g

        if node in exits:
            return g, path, len(visited)

        for neighbor, weight in graph.get(node, []):
            new_g = g + weight
            if visited.get(neighbor, float('inf')) > new_g:
                new_h = heuristic.get(neighbor, 0)
                heapq.heappush(pq,
                    (new_g + new_h, new_g, neighbor, path + [neighbor]))

    return float('inf'), None, len(visited)


# ------------------------------------------------------------------
# UCS (no heuristic) — for comparison
# ------------------------------------------------------------------
def ucs(graph, start, goal):
    pq      = [(0, start, [start])]
    visited = {}
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost
        if node == goal:
            return cost, path, len(visited)
        for nb, w in graph.get(node, []):
            nc = cost + w
            if visited.get(nb, float('inf')) > nc:
                heapq.heappush(pq, (nc, nb, path + [nb]))
    return float('inf'), None, len(visited)


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 65)
    print("  CROWD CONTROL — A* SEARCH")
    print("  Formula: f(n) = g(n) + h(n)")
    print("=" * 65)

    print("\n[TEST 1] A* Nearest Exit from Each Location")
    for start in ['G1', 'G2', 'G3', 'H1', 'H2', 'S1']:
        cost, path, n = astar_nearest_exit(
            graph, heuristic_nearest, start, exits)
        if path:
            print(f"  {start}: → {path[-1]}  Cost={cost}m  "
                  f"Path: {' → '.join(path)}  Nodes: {n}")

    print("\n[TEST 2] A* vs UCS — Efficiency Comparison")
    print(f"  {'Route':12}  {'A* cost':>9}  {'A* nodes':>9}  "
          f"{'UCS cost':>9}  {'UCS nodes':>9}  {'Savings':>8}")
    for src, dst in [('G1','E1'),('G1','E2'),('G1','E3'),
                     ('G3','E1'),('G2','E3')]:
        ac, _, an = astar(graph, heuristic_nearest, src, dst)
        uc, _, un = ucs(graph, src, dst)
        saving = f"{round((1-an/un)*100)}%" if un else "N/A"
        print(f"  {src+'→'+dst:12}  {ac:>9}  {an:>9}  "
              f"{uc:>9}  {un:>9}  {saving:>8}")

    print("\n[TEST 3] f=g+h Step-by-Step: G1 → E3")
    path_nodes = ['G1', 'C1', 'H1', 'S1', 'E3']
    g = 0
    edges = {'G1->C1':20,'C1->H1':35,'H1->S1':15,'S1->E3':10}
    for i, node in enumerate(path_nodes):
        h = heuristic_to_E3.get(node, 0)
        if i > 0:
            key = f"{path_nodes[i-1]}->{node}"
            g  += edges.get(key, 0)
        print(f"  {node:4s}  g={g:3d}m  h={h:3d}m  f={g+h:3d}m")

    print("\n" + "=" * 65)
    print("  A* is OPTIMAL with admissible heuristic.")
    print("  More efficient than UCS — heuristic prunes search.")
    print("=" * 65)
