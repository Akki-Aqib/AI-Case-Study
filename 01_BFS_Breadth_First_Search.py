# ============================================================
#  TOPIC 1: BREADTH FIRST SEARCH (BFS)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Find shortest evacuation path (fewest hops)
#            from any zone to the nearest emergency exit
# ============================================================

from collections import deque

# ------------------------------------------------------------------
# Venue Graph - Adjacency List
# Nodes: G=Gate, C=Corridor, H=Hall, S=Stairwell, E=Exit
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
# BFS: Find shortest path from start to a specific goal
# ------------------------------------------------------------------
def bfs_path(graph, start, goal):
    """
    BFS traversal to find the shortest hop path
    from 'start' node to 'goal' node.
    Returns the path as a list of nodes, or None if unreachable.
    """
    queue   = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


# ------------------------------------------------------------------
# BFS: Find nearest exit from a given start location
# ------------------------------------------------------------------
def bfs_nearest_exit(graph, start, exits):
    """
    BFS to find the NEAREST exit (fewest hops) from 'start'.
    Explores level by level and stops at the first exit found.
    """
    queue   = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node in exits:
            return path, len(path) - 1

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None, -1


# ------------------------------------------------------------------
# BFS: Full level-by-level traversal
# ------------------------------------------------------------------
def bfs_traversal(graph, start):
    """
    Standard BFS traversal showing nodes explored level by level.
    """
    queue       = deque([start])
    visited     = set([start])
    level       = 0
    level_nodes = [start]

    print(f"  Level {level}: {level_nodes}")

    while queue:
        next_level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    next_level.append(neighbor)
        if next_level:
            level += 1
            print(f"  Level {level}: {next_level}")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("  CROWD CONTROL — BREADTH FIRST SEARCH (BFS)")
    print("=" * 60)

    print("\n[TEST 1] BFS Path: G1 → E2")
    path = bfs_path(graph, 'G1', 'E2')
    if path:
        print(f"  Path Found : {' → '.join(path)}")
        print(f"  Hops       : {len(path) - 1}")

    print("\n[TEST 2] BFS Path: G3 → E1")
    path = bfs_path(graph, 'G3', 'E1')
    if path:
        print(f"  Path Found : {' → '.join(path)}")
        print(f"  Hops       : {len(path) - 1}")

    print("\n[TEST 3] Nearest Exit from Hall H2")
    path, hops = bfs_nearest_exit(graph, 'H2', exits)
    if path:
        print(f"  Nearest Exit : {path[-1]}")
        print(f"  Path         : {' → '.join(path)}")
        print(f"  Hops         : {hops}")

    print("\n[TEST 4] Nearest Exit from Stairwell S1")
    path, hops = bfs_nearest_exit(graph, 'S1', exits)
    if path:
        print(f"  Nearest Exit : {path[-1]}")
        print(f"  Path         : {' → '.join(path)}")
        print(f"  Hops         : {hops}")

    print("\n[TEST 5] BFS Level-by-Level Traversal from G1")
    bfs_traversal(graph, 'G1')

    print("\n[TEST 6] Nearest Exit for Every Gate")
    for gate in ['G1', 'G2', 'G3']:
        path, hops = bfs_nearest_exit(graph, gate, exits)
        print(f"  {gate} → {path[-1]}  |  Path: {' → '.join(path)}  |  Hops: {hops}")

    print("\n" + "=" * 60)
    print("  BFS guarantees the SHORTEST HOP path.")
    print("  Time Complexity  : O(V + E)")
    print("  Space Complexity : O(V)")
    print("=" * 60)
