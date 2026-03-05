import ipaddress
from collections import defaultdict

import ip, service


def compare_normalized_rules(r1, r2):
    src_rel = ip.compare_lists_netaddr(r1['src'], r2['src'])
    dst_rel = ip.compare_lists_netaddr(r1['dst'], r2['dst'])
    svc_rel = service.get_service_relation(r1['svc'], r2['svc'])

    rels = {"src": src_rel, "dst": dst_rel, "svc": svc_rel}
    if "DISJOINT" in rels.values(): return "DISJOINT"
    
    res_set = set(rels.values())
    if res_set == {"IDENTICAL"}: return "IDENTICAL"
    if res_set <= {"SUBSET", "IDENTICAL"}: return "SUBSET" # RULE 1 IS SUBSET OF RULE 2
    if res_set <= {"SUPERSET", "IDENTICAL"}: return "SUPERSET" # RULE 1 IS SUPERSET OF RULE 2
    
    return "OVERLAP"

# Example: Rule 1 looks different but is actually a subset of Rule 2
r1 = {'src': ['10.0.0.1-10.0.1.2', '10.0.0.0/25', '10.0.0.128/25'], 'dst': ['1.1.1.1/32'], 'svc': ['TCP 80', 'TCP 81']}
r2 = {'src': ['10.0.0.0/24'], 'dst': ['1.1.1.0/24'], 'svc': ['TCP 80-443']}

print(f"Rule Relation: {compare_normalized_rules(r1, r2)}")




def multiple(new_rule, existing_rules):
    res = defaultdict(list)
    for i, existing_rule in enumerate(existing_rules):
        cur_relation = compare_normalized_rules(new_rule, existing_rule)
        res[cur_relation].append(i)
    return res
