# ============================================================
#  TOPIC 9: MINIMAX ALGORITHM (ADVERSARIAL SEARCH)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Safety System (MAX) vs Adversarial Events like
#            fire/panic/blocked exits (MIN)
#            Find routing safest under worst-case scenario
# ============================================================

import math

# ------------------------------------------------------------------
# Terminal safety scores — higher = safer outcome
# ------------------------------------------------------------------
SAFETY_SCORES = {
    'plan_E1_clear':    85,
    'plan_E1_blocked':  20,
    'plan_E2_clear':    80,
    'plan_E2_panic':    35,
    'plan_E3_clear':    78,
    'plan_E3_blocked':  15,
    'plan_split_ok':    90,
    'plan_split_panic': 55,
}

# Game tree: Safety System chooses route, Adversary chooses disruption
game_tree = {
    'root': {
        'route_E1': {
            'no_disruption': 'plan_E1_clear',
            'block_E1':      'plan_E1_blocked'
        },
        'route_E2': {
            'no_disruption': 'plan_E2_clear',
            'panic_E2':      'plan_E2_panic'
        },
        'route_E3': {
            'no_disruption': 'plan_E3_clear',
            'block_E3':      'plan_E3_blocked'
        },
        'route_split': {
            'all_clear':     'plan_split_ok',
            'partial_panic': 'plan_split_panic'
        }
    }
}


# ------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning
# ------------------------------------------------------------------
def minimax(state, is_maximizing, alpha=-math.inf, beta=math.inf):
    """
    Recursive Minimax:
    - MAX (Safety System): chooses routing to MAXIMIZE safety score
    - MIN (Adversary)    : chooses disruption to MINIMIZE safety score
    Alpha-Beta pruning eliminates branches that won't affect result.
    """
    # Base case: leaf node — return safety score
    if isinstance(state, str):
        return SAFETY_SCORES.get(state, 0), state

    if is_maximizing:
        best_score  = -math.inf
        best_action = None
        for action, next_state in state.items():
            score, _ = minimax(next_state, False, alpha, beta)
            if score > best_score:
                best_score  = score
                best_action = action
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cut-off
        return best_score, best_action

    else:
        best_score  = math.inf
        best_action = None
        for action, next_state in state.items():
            score, _ = minimax(next_state, True, alpha, beta)
            if score < best_score:
                best_score  = score
                best_action = action
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return best_score, best_action


# ------------------------------------------------------------------
# Worst-case analysis for each route
# ------------------------------------------------------------------
def evaluate_all_routes(game_tree):
    results = {}
    for route, subtree in game_tree['root'].items():
        worst_score = math.inf
        worst_event = None
        for event, leaf in subtree.items():
            score = SAFETY_SCORES.get(leaf, 0)
            if score < worst_score:
                worst_score = score
                worst_event = event
        results[route] = {
            'worst_case_score': worst_score,
            'worst_event':      worst_event
        }
    return results


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 65)
    print("  CROWD CONTROL — MINIMAX ADVERSARIAL SEARCH")
    print("  Safety System (MAX) vs Adversarial Events (MIN)")
    print("=" * 65)

    print("\n[TEST 1] Minimax Optimal Decision")
    best_score, best_route = minimax(game_tree['root'], is_maximizing=True)
    print(f"  Optimal Route          : {best_route}")
    print(f"  Guaranteed Safety Score: {best_score}")
    print(f"  (Best outcome even under worst-case adversarial event)")

    print("\n[TEST 2] Worst-Case Score per Route")
    results = evaluate_all_routes(game_tree)
    print(f"  {'Route':>15}  {'Worst Score':>12}  Worst Event")
    for route, data in results.items():
        print(f"  {route:>15}  {data['worst_case_score']:>12}  "
              f"{data['worst_event']}")
    safest = max(results, key=lambda r: results[r]['worst_case_score'])
    print(f"\n  ✓ Minimax recommends: {safest} "
          f"(score={results[safest]['worst_case_score']})")

    print("\n[TEST 3] All Terminal Safety Scores")
    for scenario, score in sorted(SAFETY_SCORES.items(), key=lambda x: -x[1]):
        bar    = '█' * (score // 5)
        status = "SAFE" if score >= 70 else ("RISKY" if score >= 40 else "DANGER")
        print(f"  {scenario:25s}  {score:3d}  {bar:<18}  {status}")

    print("\n" + "=" * 65)
    print("  Minimax: best plan assuming adversary plays optimally.")
    print("  Time: O(b^d)  |  With Alpha-Beta: O(b^(d/2))")
    print("=" * 65)
