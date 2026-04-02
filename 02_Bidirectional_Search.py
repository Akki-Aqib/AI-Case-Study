# ============================================================
#  TOPIC 2: BIDIRECTIONAL SEARCH
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Faster pathfinding by searching simultaneously
#            from both source (gate) and destination (exit)
# ============================================================

from collections import deque

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


# ------------------------------------------------------------------
# Helper: Reconstruct full path from meeting point
# ------------------------------------------------------------------
def reconstruct_path(fwd_parent, bwd_parent, meeting_node):
    fwd_path = []
    node = meeting_node
    while node is not None:
        fwd_path.append(node)
        node = fwd_parent[node]
    fwd_path.reverse()

    bwd_path = []
    node = bwd_parent[meeting_node]
    while node is not None:
        bwd_path.append(node)
        node = bwd_parent[node]

    return fwd_path + bwd_path


# ------------------------------------------------------------------
# Bidirectional BFS
# ------------------------------------------------------------------
def bidirectional_search(graph, start, goal):
    """
    Launches two BFS frontiers simultaneously:
      - Forward  frontier: expands from 'start'
      - Backward frontier: expands from 'goal'
    Terminates when the two frontiers meet.
    Returns (path, nodes_explored).
    """
    if start == goal:
        return [start], 1

    fwd_parent = {start: None}
    bwd_parent = {goal:  None}
    fwd_queue  = deque([start])
    bwd_queue  = deque([goal])
    nodes_explored = 0

    while fwd_queue and bwd_queue:

        # Expand forward frontier
        fwd_node = fwd_queue.popleft()
        nodes_explored += 1
        for nb in graph.get(fwd_node, []):
            if nb not in fwd_parent:
                fwd_parent[nb] = fwd_node
                fwd_queue.append(nb)
                if nb in bwd_parent:
                    path = reconstruct_path(fwd_parent, bwd_parent, nb)
                    return path, nodes_explored

        # Expand backward frontier
        bwd_node = bwd_queue.popleft()
        nodes_explored += 1
        for nb in graph.get(bwd_node, []):
            if nb not in bwd_parent:
                bwd_parent[nb] = bwd_node
                bwd_queue.append(nb)
                if nb in fwd_parent:
                    path = reconstruct_path(fwd_parent, bwd_parent, nb)
                    return path, nodes_explored

    return None, nodes_explored


# ------------------------------------------------------------------
# Standard BFS for comparison
# ------------------------------------------------------------------
def bfs_path(graph, start, goal):
    queue   = deque([[start]])
    visited = set([start])
    count   = 0
    while queue:
        path = queue.popleft()
        node = path[-1]
        count += 1
        if node == goal:
            return path, count
        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return None, count


# ------------------------------------------------------------------
# Reachability check
# ------------------------------------------------------------------
def bidir_reachable(graph, src, dst):
    visited_fwd = set([src])
    visited_bwd = set([dst])
    fq = deque([src])
    bq = deque([dst])

    while fq and bq:
        nxt = set()
        for node in list(fq):
            fq.popleft()
            for nb in graph.get(node, []):
                if nb not in visited_fwd:
                    visited_fwd.add(nb)
                    nxt.add(nb)
                    fq.append(nb)
        if visited_fwd & visited_bwd:
            return True

        nxt2 = set()
        for node in list(bq):
            bq.popleft()
            for nb in graph.get(node, []):
                if nb not in visited_bwd:
                    visited_bwd.add(nb)
                    nxt2.add(nb)
                    bq.append(nb)
        if visited_fwd & visited_bwd:
            return True

    return False


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 62)
    print("  CROWD CONTROL — BIDIRECTIONAL SEARCH")
    print("=" * 62)

    test_cases = [('G1', 'E2'), ('G3', 'E1'), ('G2', 'E3'), ('S1', 'E1')]

    for src, dst in test_cases:
        print(f"\n[PATH] {src} → {dst}")
        bi_path, bi_count = bidirectional_search(graph, src, dst)
        bfs_p,   bfs_cnt  = bfs_path(graph, src, dst)
        if bi_path:
            print(f"  BiDir Path           : {' → '.join(bi_path)}")
            print(f"  BFS   Path           : {' → '.join(bfs_p)}")
            print(f"  BiDir nodes explored : {bi_count}")
            print(f"  BFS   nodes explored : {bfs_cnt}")
            saving = round((1 - bi_count / bfs_cnt) * 100, 1) if bfs_cnt else 0
            print(f"  Search reduction     : {saving}% fewer nodes")

    print("\n[REACHABILITY CHECKS]")
    for a, b in [('G1', 'E3'), ('G2', 'E2'), ('G3', 'E1')]:
        result = bidir_reachable(graph, a, b)
        print(f"  {a} ↔ {b} : {'Connected ✓' if result else 'Not Connected ✗'}")

    print("\n" + "=" * 62)
    print("  Bidirectional Search explores ~HALF the nodes of BFS.")
    print("  Speedup : O(b^d) → O(b^(d/2))")
    print("=" * 62)
