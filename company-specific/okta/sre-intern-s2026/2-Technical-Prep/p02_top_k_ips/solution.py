from __future__ import annotations

from typing import List


def top_k_ips(filepath: str, k: int) -> List[str]:
    """
    Return top-k IPs by frequency (desc), tie by ip (asc).
    Invalid lines ignored as described in README.

    We know:
    timestamp ip endpoint, we need k most freq. ip addresses
    """
    import heapq
    ip_dict = {}
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and parts[1] != "":
                ip = parts[1].strip()
                ip_dict[ip] = ip_dict.get(ip, 0) + 1
    
    heap = []
    heapq.heapify(heap)
    for ip_addr, count in ip_dict.items():
        heapq.heappush(heap, (-count, ip_addr))
    
    result = []
    while len(result) < k:
        if heap:
            item = heapq.heappop(heap)
            result.append(item[1])
        else:
            break
    
    return result

