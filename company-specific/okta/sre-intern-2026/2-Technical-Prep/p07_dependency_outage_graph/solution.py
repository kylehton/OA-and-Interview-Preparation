from __future__ import annotations

from typing import List


def impacted_services(filepath: str, failed: str) -> List[str]:
    from collections import defaultdict, deque

    service_dict = defaultdict(list)

    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split(" -> ")
            if len(parts) == 2:
                pre = parts[0].strip()
                post = parts[1].strip()
                service_dict[post].append(pre)
        
    result = []
    seen = set()
    queue = deque()
    queue.append(failed)
    while queue:
        if queue[0] in service_dict:
            for item in service_dict[queue[0]]:
                if item not in seen and item != failed:
                    queue.append(item)
                    seen.add(item)
                    result.append(item)
        queue.popleft()
    
    result.sort()
    return result


def has_cycle(filepath: str) -> bool:
    from collections import defaultdict

    graph = defaultdict(list)
    services = set()

    with open(filepath) as f:
        for line in f:
            parts = line.strip().split(" -> ")
            if len(parts) == 2:
                dependent = parts[0].strip()
                prereq = parts[1].strip()
                graph[dependent].append(prereq)
                services.add(dependent)
                services.add(prereq)

    visited = set()
    rec_stack = set()

    def dfs(node):
        if node in rec_stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if dfs(neighbor):
                return True

        rec_stack.remove(node)
        return False

    for service in services:
        if service not in visited:
            if dfs(service):
                return True

    return False

