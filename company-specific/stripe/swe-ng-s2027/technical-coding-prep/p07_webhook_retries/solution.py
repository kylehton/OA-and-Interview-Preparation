"""Starter for P07. Read README.md before implementing."""

from __future__ import annotations
# webhook needs: storage of all existing endpoints
# endpoint needs: storage of attempts keyed by event_id to update + use for retries
    
class WebhookSystem:
    def __init__(self, max_attempts: int):
        self.endpoints = {}
        self.attempts = set()
        self.events = {} # keyed by (event_id, endpoint_id), stores (timestamp, details)
        self.completed = set()
        self.dlq = []
        self.max_attempts = max_attempts

    def process_endpoints(self, endpoints: list[str]) -> None:
        for endpoint in endpoints:
            parts = endpoint.strip().split(',')
            if len(parts) == 3:
                endpoint_id, base_delay, max_delay = parts
                endpoint_id = endpoint_id.strip()
                if len(endpoint_id) != 0 and endpoint_id not in self.endpoints:
                    if base_delay.strip().isnumeric() and max_delay.strip().isnumeric():
                        base_delay, max_delay = int(base_delay), int(max_delay)
                        if base_delay > 0 and max_delay > 0 and max_delay >= base_delay:
                            self.endpoints[endpoint_id] = (base_delay, max_delay)

    def validate_attempt(self, attempt: str):
        parts = attempt.strip().split(',')
        if 5 <= len(parts) <= 6:
            timestamp, attempt_id, event_id, endpoint_id, status_code = parts[:5]
            retry_after = None
            if len(parts) == 6:
                if status_code.strip() == '429' and parts[5].strip().isnumeric():
                    retry_after = int(parts[5].strip())
                else:
                    return None
            timestamp, status_code = timestamp.strip(), status_code.strip()
            attempt_id, event_id, endpoint_id = attempt_id.strip(), event_id.strip(), endpoint_id.strip()
            if timestamp.isnumeric() and int(timestamp) >= 0:
                timestamp = int(timestamp)
                if len(event_id) != 0 and len(endpoint_id) != 0 and len(attempt_id) != 0:
                    if endpoint_id in self.endpoints:
                        if status_code.isnumeric() and (100 <= int(status_code) <= 599):
                            status_code = int(status_code)
                            if retry_after is None:
                                return (timestamp, attempt_id, event_id, endpoint_id, status_code)
                            else:
                                return (timestamp, attempt_id, event_id, endpoint_id, status_code, retry_after)
        return None
    
    def process_attempts(self, attempts: list[str]):
        for attempt in attempts:
            parsedAttempt = self.validate_attempt(attempt)
            if parsedAttempt is not None:
                timestamp, attempt_id, event_id, endpoint_id, status_code = parsedAttempt[:5]
                retry_after = None
                if len(parsedAttempt) == 6:
                    retry_after = int(parsedAttempt[5])
                if attempt_id not in self.attempts:
                    self.attempts.add(attempt_id) 
                    key = (event_id, endpoint_id)
                    if str(status_code)[0] != '2' and key not in self.completed:
                        if key not in self.events:
                            self.events[key] = []
                        failure = (timestamp, (event_id, endpoint_id, retry_after))
                        self.events[key].append(failure)
                    else:
                        if key in self.events:
                            del self.events[key]
                        self.completed.add(key)

    def get_dlq(self) -> list[str]:
        self.dlq.sort(key=lambda x: (x[0], x[1]))
        result = []
        for endpoint in self.dlq:
            result.append('DEAD'+','+','.join(endpoint))
        return result
        
    def get_retries(self) -> list[str]:
        total_failures = []
        for event_list in self.events.values():
            event_list.sort(key=lambda x: x[0])
            failure_num = len(event_list)
            
            latest_event = event_list[-1]
            timestamp, event = latest_event
            event_id, endpoint_id, retry_delay = event
            if failure_num >= self.max_attempts:
                self.dlq.append([event_id, endpoint_id, str(failure_num)])
            else:
                base_delay, max_delay = self.endpoints[endpoint_id]
                delay = min(base_delay * (2 ** (len(event_list) - 1)), max_delay)
                if retry_delay is not None:
                    delay = max(delay, retry_delay)
                failure = [timestamp, event_id, endpoint_id, str(delay+timestamp), str(failure_num)]
                total_failures.append(failure)

        failure_strings = []
        total_failures.sort(key=lambda x: (int(x[3]), x[1], x[2]))
        for failure in total_failures:
            string = 'RETRY'+','+','.join(failure[1:])
            failure_strings.append(string)
        return failure_strings

    def get_result(self):
        retries = self.get_retries()
        dlq = self.get_dlq()
        return retries + dlq


def plan_deliveries(
    endpoints: list[str], attempts: list[str], max_attempts: int
) -> list[str]:
    """Return retry rows followed by dead-letter rows."""
    webhookSystem = WebhookSystem(max_attempts)
    webhookSystem.process_endpoints(endpoints)
    webhookSystem.process_attempts(attempts)
    return webhookSystem.get_result()

