from __future__ import annotations

from typing import Dict, List, Tuple


def p95_latency(filepath: str) -> Dict[str, int]:
    from collections import defaultdict
    import math

    services = defaultdict(list)
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2 and parts[1].isnumeric() and int(parts[1]) >= 0:
                services[parts[0]].append(int(parts[1]))

    result = {}
    for service, latencies in services.items():
        latencies.sort()
        result[service] = services[service][math.ceil(0.95 * len(latencies)) - 1]
    
    return result


def top_p95_services(filepath: str, k: int) -> List[Tuple[str, int]]:
    import heapq
    all_p95 = p95_latency(filepath)
    return heapq.nsmallest(k, all_p95.items(), key=lambda x: (-x[1], x[0]))
    