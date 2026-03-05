from netaddr import IPSet, IPRange, IPNetwork

import ipaddress


def normalize(ip_list: list[str]) -> list[object]:
    nets = []
    for ip in ip_list:
        ip = ip.strip()
        try:
            if '-' in ip:
                start, end = ip.split('-')
                cur = ipaddress.summarize_address_range(
                    ipaddress.IPv4Address(start.strip()),
                    ipaddress.IPv4Address(end.strip())
                )
                nets.extend(cur)
            else:
                cur = ipaddress.ip_network(ip, strict=False)
                nets.append(cur)
        except Exception as e:
            print(f"Invalid entry {ip}: {e}")
    return nets


def to_set(data):
    s = IPSet()
    for item in data:
        if "-" in item:
            start, end = item.split("-")
            s.add(IPRange(start.strip(), end.strip()))
        else:
            s.add(IPNetwork(item))
    return s


def compare_lists_netaddr(list_a, list_b):
    set_a = to_set(list_a)
    set_b = to_set(list_b)

    # Find the intersection (the actual addresses they share)
    overlap = set_a & set_b
    
    # Summary of relationship
    print(f"Total Shared IPs: {len(overlap)}")
    print(f"Overlapping Subnets: {overlap}")
    
    if set_a == set_b: return "IDENTICAL"
    if set_a.issuperset(set_b): return "SUPERSET"
    if set_a.issubset(set_b): return "SUBSET"
    return "OVERLAP" if len(overlap) > 0 else "DISJOINT"


def main():
    list_1 = ["10.0.0.0/24", "192.168.1.1"]
    list_2 = ["10.0.0.128-10.0.0.255", "192.168.1.0/30"]

    print(compare_lists_netaddr(list_1, list_2))


if __name__ == '__main__':
    main()
