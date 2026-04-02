# ============================================================
#  TOPIC 5: GREEDY BEST FIRST SEARCH (GBFS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Route crowds using heuristic (estimated distance
#            to exit) — always expand most promising node first
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

# Heuristic h(n) — estimated hops to nearest exit
heuristic = {
    'G1': 5, 'G2': 5, 'G3': 5,
    'C1': 3, 'C2': 4, 'C3': 3,
    'H1': 2, 'H2': 2,
    'S1': 1,
    'E1': 0, 'E2': 0, 'E3': 0
}

exits = ['E1', 'E2', 'E3']


# ------------------------------------------------------------------
# GBFS: Path to specific goal
# ------------------------------------------------------------------
def greedy_bfs(graph, heuristic, start, goal):
    """
    GBFS expands the node with LOWEST h(n) first.
    Fast but NOT guaranteed to find shortest/optimal path.
    Priority queue: (h(n), node, path)
    """
    pq      = [(heuristic[start], start, [start])]
    visited = set()

    while pq:
        h, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path, len(visited)

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq,
                    (heuristic[neighbor], neighbor, path + [neighbor]))

    return None, len(visited)


# ------------------------------------------------------------------
# GBFS: Nearest exit
# ------------------------------------------------------------------
def greedy_nearest_exit(graph, heuristic, start, exits):
    """
    GBFS routing to nearest exit using heuristic guidance.
    """
    pq      = [(heuristic[start], start, [start])]
    visited = set()

    while pq:
        h, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node in exits:
            return path, len(visited)

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq,
                    (heuristic[neighbor], neighbor, path + [neighbor]))

    return None, len(visited)


# ------------------------------------------------------------------
# GBFS: Full exploration order
# ------------------------------------------------------------------
def greedy_explore(graph, heuristic, start):
    pq      = [(heuristic[start], start)]
    visited = set()
    order   = []

    while pq:
        h, node = heapq.heappop(pq)
        if node not in visited:
            visited.add(node)
            order.append((node, h))
            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (heuristic[neighbor], neighbor))

    return order


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — GREEDY BEST FIRST SEARCH (GBFS)")
    print("=" * 62)

    print("\n[TEST 1] GBFS Paths to Specific Exits")
    for src, dst in [('G1','E2'), ('G3','E1'), ('G2','E3'), ('H2','E1')]:
        path, n = greedy_bfs(graph, heuristic, src, dst)
        if path:
            print(f"  {src} → {dst}  |  Path: {' → '.join(path)}"
                  f"  |  Hops: {len(path)-1}  |  Nodes explored: {n}")

    print("\n[TEST 2] GBFS — Nearest Exit from Each Location")
    for start in ['G1', 'G2', 'G3', 'H1', 'H2', 'S1']:
        path, n = greedy_nearest_exit(graph, heuristic, start, exits)
        if path:
            print(f"  From {start}: → {path[-1]}  |  "
                  f"Path: {' → '.join(path)}  |  Nodes: {n}")

    print("\n[TEST 3] GBFS Exploration Order from G1 (h values)")
    for node, h in greedy_explore(graph, heuristic, 'G1'):
        bar = '▓' * h + '░' * (5 - h)
        print(f"    {node:4s}  h={h}  [{bar}]")

    print("\n" + "=" * 62)
    print("  GBFS always expands lowest h(n) — fastest to exit estimate.")
    print("  Fast but may miss globally optimal path.")
    print("  Time Complexity : O(b^m)")
    print("=" * 62)
