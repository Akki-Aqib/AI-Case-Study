# ============================================================
#  TOPIC 13: DEPTH LIMITED SEARCH (DLS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Find evacuation paths only within a reachable
#            depth limit — avoid impractically long routes
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
# DLS: Find path within depth limit
# ------------------------------------------------------------------
def dls(graph, node, goal, depth_limit, visited=None, path=None):
    """
    DFS restricted to depth_limit hops.
    Returns path if found within limit, else None.
    Prevents exploring routes too long for real evacuation.
    """
    if visited is None: visited = set()
    if path    is None: path    = []

    visited.add(node)
    path = path + [node]

    if node == goal:
        return path

    if depth_limit == 0:
        return None

    for nb in graph.get(node, []):
        if nb not in visited:
            result = dls(graph, nb, goal, depth_limit - 1,
                         visited.copy(), path)
            if result:
                return result
    return None


# ------------------------------------------------------------------
# DLS: Find nearest exit within depth limit
# ------------------------------------------------------------------
def dls_nearest_exit(graph, start, exits, depth_limit):
    """
    Find the nearest reachable exit within depth_limit hops.
    """
    for ex in exits:
        result = dls(graph, start, ex, depth_limit)
        if result:
            return result, ex
    return None, None


# ------------------------------------------------------------------
# DLS: All exits reachable within limit
# ------------------------------------------------------------------
def dls_all_reachable_exits(graph, start, exits, depth_limit):
    reachable = {}
    for ex in exits:
        result = dls(graph, start, ex, depth_limit)
        if result:
            reachable[ex] = result
    return reachable


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — DEPTH LIMITED SEARCH (DLS)")
    print("=" * 62)

    print("\n[TEST 1] Effect of Depth Limit: G1 → E2")
    print("  (Shows which depth limit is needed to find the path)")
    for limit in range(1, 8):
        result = dls(graph, 'G1', 'E2', limit)
        if result:
            print(f"  Limit={limit}: FOUND  {' → '.join(result)}")
        else:
            print(f"  Limit={limit}: Not found within depth {limit}")

    print("\n[TEST 2] All Gates — Exits within Depth 4")
    print("  (Depth 4 = 4 hops = practical evacuation limit)")
    for gate in ['G1', 'G2', 'G3']:
        reachable = dls_all_reachable_exits(graph, gate, exits, 4)
        print(f"\n  From {gate}:")
        for ex, path in reachable.items():
            print(f"    → {ex}: {' → '.join(path)}")
        not_reachable = [e for e in exits if e not in reachable]
        for ex in not_reachable:
            print(f"    → {ex}: NOT reachable within depth 4")

    print("\n[TEST 3] DLS Nearest Exit within Depth 3")
    for start in ['G1', 'G2', 'G3', 'H1', 'H2', 'S1']:
        path, ex = dls_nearest_exit(graph, start, exits, 3)
        if path:
            print(f"  {start}: → {ex}  Path: {' → '.join(path)}")
        else:
            print(f"  {start}: No exit within depth 3")

    print("\n[TEST 4] Depth Limit Impact on Safety")
    print("  Depth 2: Only immediate halls accessible")
    print("  Depth 4: Most exits reachable")
    print("  Depth 6: All exits reachable (but may be too far)")
    for depth in [2, 3, 4, 5]:
        found = 0
        for gate in ['G1', 'G2', 'G3']:
            for ex in exits:
                if dls(graph, gate, ex, depth):
                    found += 1
        print(f"  Depth {depth}: {found}/9 gate-exit pairs reachable")

    print("\n" + "=" * 62)
    print("  DLS focuses search — avoids impractical long routes.")
    print("  Depth limit = maximum acceptable evacuation hops.")
    print("=" * 62)
