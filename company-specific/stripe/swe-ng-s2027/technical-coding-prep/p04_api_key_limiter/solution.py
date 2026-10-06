"""Starter for P04. Read README.md before implementing."""

from __future__ import annotations

from collections import deque

class RateLimiter:
    def __init__(self):
        self.config = {}
        self.api_requests = {}
        self.cache = {}

    def register_api_key(self, api_key: str, limit: int, seconds: int):
        if api_key in self.api_requests or limit <= 0 or seconds <= 0:
            return 'ERROR'
        self.api_requests[api_key] = []
        self.config[api_key] = {'limit': limit, 'window': seconds}
        return 'OK'

    # need to get the current in-window count without mutating
    # can run binary search on queue, finding lowest num
    # that is greater or equal to timestamp
    def get_status(self, timestamp, key_id):
        if key_id in self.api_requests and timestamp >= 0:
            lowerBound = timestamp - self.config[key_id]['window'] + 1
            queue = self.api_requests[key_id]
            l, r = 0, len(queue)-1
            while l <= r:
                mid = (l + r) // 2
                if queue[mid] < lowerBound:
                    l = mid + 1
                else:
                    r = mid - 1
            return f'{len(queue)-l}/{self.config[key_id]['limit']}'
        return 'ERROR'

    def change_limit(self, key_id: str, new_limit: int, new_window: int):
        if key_id not in self.api_requests or new_limit <= 0 or new_window <= 0:
            return 'ERROR'
        self.config[key_id] = {'limit': new_limit, 'window': new_window}
        return 'OK'

    def process_request(self, timestamp: int, request_id: str, api_key: str):
        if request_id in self.cache:
            return self.cache[request_id]
        if api_key in self.api_requests:
            lowerBound = timestamp - self.config[api_key]['window'] + 1
            index = 0
            stored = self.api_requests[api_key]
            while index < len(stored) and stored[index] < lowerBound:
                index += 1
            curr_size = len(stored) - index
            if curr_size < self.config[api_key]['limit']:
                self.api_requests[api_key].append(timestamp)
                self.cache[request_id] = 'ALLOW'
                return 'ALLOW'
            else:
                self.cache[request_id] = 'DENY'
                return 'DENY'
        return 'ERROR'

    def process_command(self, request: str):
        parts = request.strip().split()
        if len(parts) == 3:
            operation = parts[0].strip()
            if operation == 'STATUS':
                timestamp = parts[1].strip()
                key_id = parts[2].strip()
                if timestamp.isnumeric():
                    return self.get_status(int(timestamp), key_id)
        if len(parts) == 4:
            operation = parts[0].strip()
            if operation == 'REGISTER':
                key_id = parts[1].strip()
                limit = parts[2].strip()
                window_sec = parts[3].strip()
                if limit.isnumeric() and window_sec.isnumeric():
                    return self.register_api_key(key_id, int(limit), int(window_sec))
            elif operation == 'REQUEST':
                timestamp = parts[1].strip()
                req_id = parts[2].strip()
                key_id = parts[3].strip()
                if timestamp.isnumeric() and int(timestamp) >= 0:
                    return self.process_request(int(timestamp), req_id, key_id)
            elif operation == 'SET':
                key_id = parts[1].strip()
                new_limit = parts[2].strip()
                new_window_sec = parts[3].strip()
                if new_limit.isnumeric() and new_window_sec.isnumeric():
                    return self.change_limit(key_id, int(new_limit), int(new_window_sec))
        return 'ERROR'

def evaluate_requests(commands: list[str]) -> list[str]:
    """Execute rate-limiter commands and return one response per command."""
    responses = []
    rateLimiter = RateLimiter()
    for command in commands:
        responses.append(rateLimiter.process_command(command))
    return responses

