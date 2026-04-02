# ============================================================
#  TOPIC 10: ITERATIVE DEEPENING DFS (IDDFS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Memory-efficient pathfinding combining
#            BFS completeness + DFS memory efficiency
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

exits = ['E1', 'E2', 'E3']


# ------------------------------------------------------------------
# Depth Limited Search (DLS) — subroutine for IDDFS
# ------------------------------------------------------------------
def depth_limited_search(graph, node, goal, limit,
                          visited=None, path=None):
    """
    DFS with a hard depth limit.
    Returns path if found within limit, else None.
    """
    if visited is None: visited = set()
    if path    is None: path    = []

    visited.add(node)
    path = path + [node]

    if node == goal:
        return path

    if limit == 0:
        return None

    for nb in graph.get(node, []):
        if nb not in visited:
            result = depth_limited_search(
                graph, nb, goal, limit - 1,
                visited.copy(), path)
            if result:
                return result
    return None


# ------------------------------------------------------------------
# IDDFS — Main Algorithm
# ------------------------------------------------------------------
def iddfs(graph, start, goal, max_depth=10):
    """
    Iteratively increases depth limit from 0 to max_depth.
    First successful DLS gives the optimal (shortest) path.
    Combines:
      - BFS: completeness — finds path if one exists
      - DFS: memory efficiency — only stores current path
    """
    for depth in range(max_depth + 1):
        result = depth_limited_search(graph, start, goal, depth)
        if result:
            return result, depth
    return None, -1


# ------------------------------------------------------------------
# IDDFS to nearest exit
# ------------------------------------------------------------------
def iddfs_nearest_exit(graph, start, exits, max_depth=10):
    for depth in range(max_depth + 1):
        for ex in exits:
            result = depth_limited_search(graph, start, ex, depth)
            if result:
                return result, depth, ex
    return None, -1, None


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — ITERATIVE DEEPENING DFS (IDDFS)")
    print("=" * 62)

    print("\n[TEST 1] IDDFS Paths — Gate to Exit")
    for src, dst in [('G1','E1'), ('G3','E3'), ('G2','E2'), ('H1','E3')]:
        path, depth = iddfs(graph, src, dst)
        if path:
            print(f"  {src} → {dst}  |  Found at depth: {depth}  "
                  f"|  Path: {' → '.join(path)}")

    print("\n[TEST 2] IDDFS Depth-by-Depth: G1 → E2")
    print("  (Shows how IDDFS progressively searches deeper)")
    for d in range(1, 7):
        result = depth_limited_search(graph, 'G1', 'E2', d)
        if result:
            print(f"    Depth {d}: FOUND  {' → '.join(result)}")
        else:
            print(f"    Depth {d}: Not found within depth {d}")

    print("\n[TEST 3] IDDFS Nearest Exit from Each Gate")
    for gate in ['G1', 'G2', 'G3', 'H1', 'S1']:
        path, depth, ex = iddfs_nearest_exit(graph, gate, exits)
        if path:
            print(f"  {gate}: → {ex}  Depth: {depth}  "
                  f"Path: {' → '.join(path)}")

    print("\n[TEST 4] Memory Advantage of IDDFS")
    print("  At depth d with branching factor b:")
    for b, d in [(3, 6), (4, 8), (5, 10)]:
        bfs_mem   = b ** d
        iddfs_mem = b * d
        print(f"  b={b}, d={d}: BFS memory={bfs_mem:,}  "
              f"IDDFS memory={iddfs_mem}  "
              f"Ratio={round(bfs_mem/iddfs_mem)}x")

    print("\n" + "=" * 62)
    print("  IDDFS: BFS completeness + DFS memory efficiency.")
    print("  Memory: O(b*d)  vs BFS O(b^d)")
    print("=" * 62)
