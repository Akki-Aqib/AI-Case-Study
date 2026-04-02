# ============================================================
#  TOPIC 15: FIRST ORDER LOGIC (FOL)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Rule-based automated reasoning for routing
#            decisions — transparent and auditable IF-THEN rules
# ============================================================


# ------------------------------------------------------------------
# FOL Rules — Priority Ordered
# ------------------------------------------------------------------
def fol_routing_decision(density, exit_open, fire_nearby,
                          panic_level, exit_distance):
    """
    Applies FOL IF-THEN rules in priority order.

    Rules:
    R1: IF fire_nearby AND exit_open    → evacuate_immediately
    R2: IF density = critical           → emergency_all_exits
    R3: IF panic = high AND exit_open   → direct_to_exit_fast
    R4: IF density = high AND exit_open → direct_to_exit
    R5: IF density = high AND NOT open  → redirect_alternate
    R6: IF exit_distance > 200          → use_stairwell
    R7: DEFAULT                         → normal_flow
    """
    # Rule 1: Fire overrides everything
    if fire_nearby and exit_open:
        return "evacuate_immediately", \
               "R1: Fire detected — immediate evacuation via open exit"

    # Rule 2: Critical density — open all exits
    if density == 'critical':
        return "emergency_all_exits", \
               "R2: Critical density — activate all exits simultaneously"

    # Rule 3: Panic + open exit
    if panic_level == 'high' and exit_open:
        return "direct_to_exit_fast", \
               "R3: Panic detected — fast-route crowd to exit"

    # Rule 4: High density + accessible exit
    if density == 'high' and exit_open:
        return "direct_to_exit", \
               "R4: High density — direct crowd to exit"

    # Rule 5: High density + blocked exit
    if density == 'high' and not exit_open:
        return "redirect_alternate_exit", \
               "R5: Exit blocked — redirect to alternate exit"

    # Rule 6: Far exit — use stairwell shortcut
    if exit_distance > 200:
        return "use_stairwell", \
               "R6: Distance > 200m — route via nearest stairwell"

    # Rule 7: Default — normal conditions
    return "normal_flow", \
           "R7: Normal conditions — standard crowd flow"


# ------------------------------------------------------------------
# FOL Zone Assessment — multi-signal reasoning
# ------------------------------------------------------------------
def fol_zone_assessment(zone_data):
    """
    Applies FOL rules to assess each zone and
    determine appropriate crowd management action.

    zone_data: dict with keys:
      density, exit_available, fire, panic, distance
    """
    decisions = {}

    for zone, data in zone_data.items():
        action, rule = fol_routing_decision(
            density      = data.get('density',   'normal'),
            exit_open    = data.get('exit_open',  True),
            fire_nearby  = data.get('fire',       False),
            panic_level  = data.get('panic',      'low'),
            exit_distance= data.get('distance',   100)
        )
        decisions[zone] = {
            'action': action,
            'rule':   rule
        }

    return decisions


# ------------------------------------------------------------------
# FOL Inference Engine — chained reasoning
# ------------------------------------------------------------------
def fol_infer(facts):
    """
    Simple forward-chaining FOL inference.
    Derives conclusions from known facts using rules.
    """
    conclusions = []

    # Rule chain: density + distance → routing strategy
    if facts.get('density') == 'high':
        conclusions.append("FACT: Zone is overcrowded")

        if facts.get('exit_open'):
            conclusions.append("INFER: Direct routing possible")
            if facts.get('distance', 100) <= 100:
                conclusions.append("CONCLUDE: Use direct exit route")
            else:
                conclusions.append("CONCLUDE: Use stairwell shortcut")
        else:
            conclusions.append("INFER: Primary exit unavailable")
            conclusions.append("CONCLUDE: Activate alternate exit")

    if facts.get('fire'):
        conclusions.append("FACT: Fire detected nearby")
        conclusions.append("CONCLUDE: Emergency evacuation — override all rules")

    if facts.get('panic') == 'high':
        conclusions.append("FACT: Panic situation detected")
        conclusions.append("CONCLUDE: Fast-track crowd — minimize bottlenecks")

    return conclusions


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 65)
    print("  CROWD CONTROL — FIRST ORDER LOGIC (FOL)")
    print("=" * 65)

    print("\n[TEST 1] All Rule Scenarios")
    test_scenarios = [
        # (density,    exit_open, fire,  panic,  dist,  label)
        ('high',      True,      True,  'low',   80,  "FIRE at E1"),
        ('critical',  True,      False, 'low',   80,  "Critical density"),
        ('high',      True,      False, 'high',  80,  "High density + panic"),
        ('high',      True,      False, 'low',   80,  "Standard high density"),
        ('high',      False,     False, 'low',   80,  "Exit blocked"),
        ('normal',    True,      False, 'low',  250,  "Far exit (250m)"),
        ('normal',    True,      False, 'low',   80,  "Normal conditions"),
    ]

    print(f"\n  {'Scenario':<25}  {'Decision':<28}  Rule")
    print("  " + "─" * 75)
    for density, exit_open, fire, panic, dist, label in test_scenarios:
        action, rule = fol_routing_decision(
            density, exit_open, fire, panic, dist)
        print(f"  {label:<25}  {action:<28}  {rule}")

    print("\n[TEST 2] Multi-Zone Assessment")
    zones = {
        'Zone_H1': {'density':'high',   'exit_open':True,  'fire':True,
                    'panic':'low',  'distance':80},
        'Zone_H2': {'density':'normal', 'exit_open':False, 'fire':False,
                    'panic':'low',  'distance':120},
        'Zone_S1': {'density':'high',   'exit_open':True,  'fire':False,
                    'panic':'high', 'distance':60},
        'Zone_C1': {'density':'normal', 'exit_open':True,  'fire':False,
                    'panic':'low',  'distance':250},
    }

    assessments = fol_zone_assessment(zones)
    print(f"\n  {'Zone':<12}  {'Action':<28}  Rule")
    print("  " + "─" * 70)
    for zone, data in assessments.items():
        print(f"  {zone:<12}  {data['action']:<28}  {data['rule']}")

    print("\n[TEST 3] FOL Forward-Chaining Inference")
    fact_sets = [
        {'density': 'high', 'exit_open': True,  'distance': 80},
        {'density': 'high', 'exit_open': False},
        {'density': 'high', 'fire': True, 'panic': 'high'},
    ]

    for i, facts in enumerate(fact_sets, 1):
        print(f"\n  Facts {i}: {facts}")
        conclusions = fol_infer(facts)
        for c in conclusions:
            print(f"    → {c}")

    print("\n" + "=" * 65)
    print("  FOL provides transparent, auditable routing decisions.")
    print("  Every decision can be explained by a logical rule.")
    print("  Critical for safety-certified deployment systems.")
    print("=" * 65)
