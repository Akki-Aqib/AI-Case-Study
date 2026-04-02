# ============================================================
#  TOPIC 12: CONSTRAINT SATISFACTION PROBLEM (CSP)
#  Subject : Artificial Intelligence Case Study
#  Topic   : Crowd Control in Large Events
#  Problem : Resolve conflicts between multiple sensor inputs
#            (pressure sensors, cameras, zone alerts)
#            and determine final routing decision
# ============================================================

exits = ['E1', 'E2', 'E3']


# ------------------------------------------------------------------
# Full CSP Resolver
# ------------------------------------------------------------------
def resolve_routing_csp(sensor_data, camera_data, alert_data):
    """
    Applies constraint rules to resolve conflicting signals.

    Constraints (priority order):
    C1: Fire alert       → nearest safe exit
    C2: Panic            → least congested exit
    C3: Exit blocked     → redirect to alternate
    C4: Exit overloaded  → redirect to clear exit
    C5: No conflict      → use sensor recommendation
    """
    decisions = {}

    for zone, recommended_exit in sensor_data.items():
        exit_status = camera_data.get(recommended_exit, 'clear')
        zone_alert  = alert_data.get(zone, None)

        # Constraint 1: Fire
        if zone_alert == 'fire':
            for ex in exits:
                if camera_data.get(ex, 'clear') == 'clear':
                    decisions[zone] = (ex,
                        'C1: FIRE — redirected to nearest safe exit')
                    break
            continue

        # Constraint 2: Panic
        if zone_alert == 'panic':
            available = [e for e in exits
                         if camera_data.get(e,'clear') != 'blocked']
            best = available[0] if available else recommended_exit
            decisions[zone] = (best,
                'C2: PANIC — redirected to least congested exit')
            continue

        # Constraint 3: Blocked exit
        if exit_status == 'blocked':
            alternates = [e for e in exits
                          if e != recommended_exit
                          and camera_data.get(e,'clear') != 'blocked']
            if alternates:
                decisions[zone] = (alternates[0],
                    f'C3: {recommended_exit} blocked — '
                    f'redirected to {alternates[0]}')
            else:
                decisions[zone] = (recommended_exit,
                    'C3: All exits blocked — shelter in place')
            continue

        # Constraint 4: Overloaded exit
        if exit_status == 'overloaded':
            alternates = [e for e in exits
                          if e != recommended_exit
                          and camera_data.get(e,'clear') == 'clear']
            if alternates:
                decisions[zone] = (alternates[0],
                    f'C4: {recommended_exit} overloaded — '
                    f'redirected to {alternates[0]}')
            else:
                decisions[zone] = (recommended_exit,
                    'C4: Proceeding despite overload')
            continue

        # Constraint 5: No conflict
        decisions[zone] = (recommended_exit,
            'C5: No conflict — normal routing')

    return decisions


# ------------------------------------------------------------------
# Quick CSP (simplified)
# ------------------------------------------------------------------
def quick_csp(density_sensor, camera_status):
    """
    Simple 2-input CSP for quick routing decision.
    """
    if density_sensor == 'high' and camera_status == 'clear':
        return 'direct_to_exit'
    if density_sensor == 'high' and camera_status == 'blocked':
        return 'redirect_alternate_exit'
    if density_sensor == 'critical':
        return 'emergency_all_exits'
    return 'normal_flow'


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 65)
    print("  CROWD CONTROL — CONSTRAINT SATISFACTION PROBLEM (CSP)")
    print("=" * 65)

    # Scenario 1
    print("\n[SCENARIO 1] Mixed Conflicts")
    sensor = {'Zone_H1': 'E1', 'Zone_H2': 'E2', 'Zone_S1': 'E3'}
    camera = {'E1': 'blocked', 'E2': 'clear', 'E3': 'overloaded'}
    alerts = {'Zone_H1': None, 'Zone_H2': 'panic', 'Zone_S1': None}

    print(f"  Sensors : {sensor}")
    print(f"  Camera  : {camera}")
    print(f"  Alerts  : {alerts}")
    print("\n  CSP Decisions:")
    for zone, (ex, reason) in resolve_routing_csp(
            sensor, camera, alerts).items():
        print(f"    {zone:12s} → {ex}  |  {reason}")

    # Scenario 2
    print("\n[SCENARIO 2] Fire Emergency")
    sensor2 = {'Zone_G1': 'E1', 'Zone_G2': 'E1', 'Zone_G3': 'E1'}
    camera2 = {'E1': 'blocked', 'E2': 'clear', 'E3': 'clear'}
    alerts2 = {'Zone_G1': 'fire', 'Zone_G2': 'fire', 'Zone_G3': None}

    print(f"  Sensors : {sensor2}")
    print(f"  Camera  : {camera2}")
    print(f"  Alerts  : {alerts2}")
    print("\n  CSP Decisions:")
    for zone, (ex, reason) in resolve_routing_csp(
            sensor2, camera2, alerts2).items():
        print(f"    {zone:12s} → {ex}  |  {reason}")

    # Scenario 3: Quick CSP
    print("\n[SCENARIO 3] Quick CSP — All Combinations")
    print(f"  {'Density':10}  {'Camera':12}  Decision")
    print("  " + "-" * 45)
    for density in ['normal', 'high', 'critical']:
        for cam in ['clear', 'blocked']:
            decision = quick_csp(density, cam)
            print(f"  {density:10}  {cam:12}  {decision}")

    print("\n" + "=" * 65)
    print("  CSP resolves conflicts from multiple sensor inputs.")
    print("  Rules applied in priority order — highest first.")
    print("=" * 65)
