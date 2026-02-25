from __future__ import annotations

from typing import Dict, List, Tuple


def route_stats(filepath: str) -> Dict[str, Dict[str, int]]:
    # given lines in a filepath, each line is an http request
    # method path status. we need to key-value after users/ and generalize to {id},
    # then add a count of requests statuses per generalized method
    from collections import defaultdict
    method_dict = defaultdict(lambda: {'2xx': 0, '4xx': 0, '5xx': 0})
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                path = parts[1]
                status = parts[2]
                if status.isdigit():
                    string_parts = path.split('/')
                    new_str = ""
                    valid = True
                    for i in range(1, len(string_parts)):
                        if i > 0 and string_parts[i].isnumeric():
                            new_str += "/{id}"
                        else:
                            new_str += "/" + string_parts[i]
                    status_type = status[0]
                    if status_type == '2':
                        method_dict[new_str]['2xx'] += 1
                    elif status_type == '4':
                        method_dict[new_str]['4xx'] += 1
                    elif status_type == '5':
                        method_dict[new_str]['5xx'] += 1
    return method_dict


def top_routes_by_5xx(filepath: str, k: int) -> List[Tuple[str, int]]:
    import heapq
    normalized = route_stats(filepath)
    print(normalized)
    sorted_routes = sorted(normalized.items(), key=lambda x: (-(x[1]['5xx']), x[0]))
    print(sorted_routes)
    result = []
    for i in range(k):
        result.append((sorted_routes[i][0], sorted_routes[i][1]['5xx']))
    return result
