from collections import defaultdict

def parse_svc(s):
    """Parses 'TCP 80-100' into ('TCP', 80, 100)."""
    parts = s.split()
    proto = parts[0].upper()
    ports = parts[1]
    start, end = map(int, ports.split('-')) if '-' in ports else (int(ports), int(ports))
    return proto, start, end

def is_subset(list_a, list_b):
    """Checks if every range in list_a is fully covered by ranges in list_b."""
    for p1, s1, e1 in list_a:
        covered = False
        for p2, s2, e2 in list_b:
            if p1 == p2 and s1 >= s2 and e1 <= e2:
                covered = True
                break
        if not covered: return False
    return True

def has_overlap(list_a, list_b):
    """Checks if any range in list_a intersects with any in list_b."""
    for p1, s1, e1 in list_a:
        for p2, s2, e2 in list_b:
            if p1 == p2 and max(s1, s2) <= min(e1, e2):
                return True
    return False

def get_service_relation(list_1, list_2):
    # 1. Parse and Group
    svc1 = [parse_svc(s) for s in list_1]
    svc2 = [parse_svc(s) for s in list_2]

    # 2. Determine Relationship
    in_2 = is_subset(svc1, svc2)
    in_1 = is_subset(svc2, svc1)

    if in_2 and in_1: return "IDENTICAL"
    if in_2: return "SUBSET"
    if in_1: return "SUPERSET"
    
    if has_overlap(svc1, svc2):
        return "OVERLAP"
    
    return "DISJOINT"

services_a = ["TCP 80-100", "UDP 53"]
services_b = ["TCP 70-150", "UDP 53", "TCP 443"]

print(f"Relation: {get_service_relation(services_a, services_b)}")
