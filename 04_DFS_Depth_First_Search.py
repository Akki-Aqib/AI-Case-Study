# ============================================================
#  TOPIC 4: DEPTH FIRST SEARCH (DFS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Explore all evacuation paths, detect bottlenecks,
#            find all possible routes in deep corridor networks
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
# DFS Recursive
# ------------------------------------------------------------------
def dfs_recursive(graph, node, visited=None, order=None):
    """
    Recursive DFS. Explores each branch completely before
    backtracking. Returns visit order.
    """
    if visited is None: visited = set()
    if order   is None: order   = []

    visited.add(node)
    order.append(node)

    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order


# ------------------------------------------------------------------
# DFS Iterative
# ------------------------------------------------------------------
def dfs_iterative(graph, start):
    """
    Iterative DFS using explicit stack.
    Avoids Python recursion limit for large graphs.
    """
    stack   = [start]
    visited = set()
    order   = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order


# ------------------------------------------------------------------
# DFS: Find ALL paths from start to goal
# ------------------------------------------------------------------
def dfs_all_paths(graph, start, goal, path=None, all_paths=None):
    """
    DFS to discover every possible route from start to goal.
    """
    if path      is None: path      = []
    if all_paths is None: all_paths = []

    path = path + [start]

    if start == goal:
        all_paths.append(path)
        return all_paths

    for neighbor in graph.get(start, []):
        if neighbor not in path:
            dfs_all_paths(graph, neighbor, goal, path, all_paths)

    return all_paths


# ------------------------------------------------------------------
# DFS: Find ONE path
# ------------------------------------------------------------------
def dfs_find_path(graph, start, goal, visited=None, path=None):
    if visited is None: visited = set()
    if path    is None: path    = []

    visited.add(start)
    path = path + [start]

    if start == goal:
        return path

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result = dfs_find_path(graph, neighbor, goal, visited, path)
            if result:
                return result

    return None


# ------------------------------------------------------------------
# DFS: Reachable exits
# ------------------------------------------------------------------
def dfs_reachable_exits(graph, start, exits):
    stack    = [start]
    visited  = set()
    reachable = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node in exits:
            reachable.append(node)
        for nb in graph.get(node, []):
            if nb not in visited:
                stack.append(nb)

    return reachable


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — DEPTH FIRST SEARCH (DFS)")
    print("=" * 62)

    print("\n[TEST 1] Recursive DFS from G1")
    print(f"  Order: {' → '.join(dfs_recursive(graph, 'G1'))}")

    print("\n[TEST 2] Iterative DFS from G2")
    print(f"  Order: {' → '.join(dfs_iterative(graph, 'G2'))}")

    print("\n[TEST 3] DFS Single Path: G3 → E1")
    path = dfs_find_path(graph, 'G3', 'E1')
    if path:
        print(f"  Path : {' → '.join(path)}  |  Hops: {len(path)-1}")

    print("\n[TEST 4] ALL Paths: H1 → Each Exit")
    for ex in exits:
        all_paths = dfs_all_paths(graph, 'H1', ex)
        print(f"  H1 → {ex}: {len(all_paths)} path(s)")
        for i, p in enumerate(all_paths, 1):
            print(f"    Path {i}: {' → '.join(p)}")

    print("\n[TEST 5] Reachable Exits from Each Zone")
    for zone in ['G1', 'G2', 'G3', 'H1', 'H2', 'S1']:
        r = dfs_reachable_exits(graph, zone, exits)
        print(f"  {zone} can reach: {r}")

    print("\n" + "=" * 62)
    print("  DFS explores deep paths before backtracking.")
    print("  NOT guaranteed to find the shortest path.")
    print("  Time Complexity : O(V + E)")
    print("=" * 62)
